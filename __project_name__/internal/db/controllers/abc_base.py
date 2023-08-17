from abc import abstractmethod, ABC


class AbstractBaseController(ABC):

    @abstractmethod
    async def get_one():
        pass

    @abstractmethod
    async def check_if_exists():
        pass

    @abstractmethod
    async def get_many():
        pass

    @abstractmethod
    async def get_all():
        pass

    @abstractmethod
    async def create():
        pass

    @abstractmethod
    async def update():
        pass

    @abstractmethod
    async def delete():
        pass

    @abstractmethod
    async def delete_all():
        pass

