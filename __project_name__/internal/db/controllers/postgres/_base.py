from sqlalchemy.orm import Session


class CRUDBase:
    associative_tables = {}

    def __init__(self, db: Session, model):
        self.model = model
        self.db = db

    def get_total_amount(self):
        try:
            num_of_rows = self.db.query(self.model).count()
            return num_of_rows
        except:
            self.db.rollback()
            raise

    def get_all(self, reverse=False):
        if reverse:
            by_id = self.model.id.desc()
        else:
            by_id = self.model.id

        try:
            data = self.db.query(self.model).order_by(by_id).all()
            return data
        except:
            self.db.rollback()
            raise

    def get(self, id: int):
        try:
            return self.db.query(self.model).filter_by(id=id).first()
        except:
            self.db.rollback()
            raise

    def get_by(self, **query_param):
        try:
            return self.db.query(self.model).filter_by(**query_param).all()
        except:
            self.db.rollback()
            raise

    def get_part(self, page, per_page, reverse=False, order_by_rank: bool = False):
        if order_by_rank:
            order = self.model.rank
        else:
            order = self.model.id

        if reverse:
            order = order.desc()

        try:
            part = (
                self.db.query(self.model)
                .order_by(order)
                .limit(per_page)
                .offset(page * per_page)
                .all()
            )
            return part
        except:
            self.db.rollback()
            raise

    def create(self, create_scheme):
        new_obj = self.model()
        try:
            for field in create_scheme.__dict__:
                value = getattr(create_scheme, field)
                if isinstance(value, (int, str, float, bool)):
                    setattr(new_obj, field, value)
                if isinstance(value, list):
                    db_model = self.associative_tables[field]
                    if not value:
                        setattr(new_obj, field, [])
                        continue
                    if isinstance(value[0], int):
                        objcts = (
                            self.db.query(db_model).filter(db_model.id.in_(value)).all()
                        )
                    else:
                        objcts = (
                            self.db.query(db_model)
                            .filter(db_model.name.in_(value))
                            .all()
                        )
                    setattr(new_obj, field, objcts)

            self.db.add(new_obj)
            self.db.commit()
            self.db.refresh(new_obj)
            return new_obj
        except:
            self.db.rollback()
            raise

    def update_field(self, field: str, obj_to_update, update_value):
        try:
            setattr(obj_to_update, field, update_value)
            self.db.commit()
            self.db.refresh(obj_to_update)
            return obj_to_update
        except:
            self.db.rollback()
            raise

    def update(self, obj_to_update, update_scheme):
        try:
            for field in update_scheme.__dict__:
                value = getattr(update_scheme, field)
                if isinstance(value, (int, str, float, bool)):
                    setattr(obj_to_update, field, value)
                if isinstance(value, list):
                    db_model = self.associative_tables[field]
                    if not value:
                        setattr(obj_to_update, field, [])
                        continue
                    if isinstance(value[0], int):
                        objcts = (
                            self.db.query(db_model).filter(db_model.id.in_(value)).all()
                        )
                    else:
                        objcts = (
                            self.db.query(db_model)
                            .filter(db_model.name.in_(value))
                            .all()
                        )
                    setattr(obj_to_update, field, objcts)
            self.db.commit()
            self.db.refresh(obj_to_update)
            return obj_to_update
        except:
            self.db.rollback()
            raise

    def delete(self, id: int):
        try:
            to_delete = self.db.query(self.model).filter(self.model.id == id).first()
            if to_delete:
                self.db.delete(to_delete)
                self.db.commit()
                return to_delete
        except:
            self.db.rollback()
            raise

    def delete_all(self):
        try:
            to_delete = self.db.query(self.model).all()
            for item in to_delete:
                self.db.delete(item)
            self.db.commit()
        except:
            self.db.rollback()
            raise
