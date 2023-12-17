import os
from struct import Struct

from msgspec.inspect import Field


class RuntimeConf(Struct):

    def __setattr__(self, key, value):
        print()


class Settings(RuntimeConf):
    BOT_TOKEN: str = os.getenv("BOT_TOKEN")
    BOT_USERNAME: str = os.getenv("BOT_USERNAME")
