from typing import Optional


class ExceptionBase(Exception):
    detail_default: str

    def __init__(self, detail: Optional[str] = None):
        if self.detail_default is None:
            raise NotImplementedError("detail_default is not implemented")
        self.detail = self.detail_default or detail
