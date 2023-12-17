from abc import abstractmethod, ABCMeta

from app.modules.random_events.typings import EventT


class EventService(metaclass=ABCMeta):
    @abstractmethod
    def roll_event(self, probality: float) -> EventT:
        ...
