from abc import ABCMeta, abstractmethod


class ModelService(metaclass=ABCMeta):
    @abstractmethod
    async def get_response(self, uid: str) -> str:
        ...
