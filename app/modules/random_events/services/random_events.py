import random
from datetime import datetime

import pytz

from app.modules.random_events.consts import RANDOM_EVENTS
from app.modules.random_events.entity.random_events import RandomEvent
from app.modules.random_events.services.base import EventService


class RandomEventsService(EventService):
    def __init__(self):
        self._events = RANDOM_EVENTS

    def roll_event(self, probability: float = 5.0) -> RandomEvent | None:
        max_probability = 100
        if not 0 <= probability <= max_probability:
            msg = 'Probability must be between 0 and 100'
            raise ValueError(msg)

        random.seed(datetime.timestamp(datetime.now(tz=pytz.UTC)))

        if (random.randint(0, 100) - (100 - probability)) > 0:
            event: RandomEvent = random.choice(self._events)
            return event

        return None
