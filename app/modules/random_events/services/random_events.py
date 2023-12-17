import random
from datetime import datetime

from app.modules.random_events.consts import RANDOM_EVENTS
from app.modules.random_events.entity.random_events import RandomEvent
from app.modules.random_events.services.base import EventService


class RandomEventsService(EventService):
    def __init__(self):
        self._events = RANDOM_EVENTS

    def roll_event(self, probability: float = 15.0) -> RandomEvent | None:
        if not 0 <= probability <= 100:
            raise ValueError('Probability must be between 0 and 100')

        random.seed(datetime.timestamp(datetime.now()))

        if (random.randint(0, 100) - (100 - probability)) > 0:
            event: RandomEvent = random.choice(self._events)
            return event
