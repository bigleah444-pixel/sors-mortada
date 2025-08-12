import os
from typing import Set

from telethon.tl.types import ChatBannedRights
from validators.url import url


class Config(object):
    LOGGER = True
    # MUST NEEDED VARS
    PORT = os.environ.get("PORT", None)

    # Get the values for following 2 from my.telegram.org
    APP_ID = int(os.environ.get("APP_ID", 6))
    API_HASH = os.environ.get("API_HASH") or None

    # Database url heroku sets it automatically else get this from elephantsql
    DB_URI = os.environ.get("DATABASE_URL", None)

    # Get this value by running python3 stringsetup.py or https://repl.it/@zedthonn/stringsession
    STRING_SESSION = os.environ.get("STRING_SESSION", None)

    # get this value from http://www.timezoneconverter.com/cgi-bin/findzone.tzc
    TZ = os.environ.get("TZ", "Asia/Baghdad")
