from abc import ABCMeta, abstractmethod


class EventService(metaclass=ABCMeta):
    @abstractmethod
    def roll_event(self, probality: float): ...
