import os

from .base import *
from jaram_atd.util import get_server_info_value

SETTING_PRD_DIC = get_server_info_value("development")
SECRET_KEY = SETTING_PRD_DIC["SECRET_KEY"]

DEBUG = False

INSTALLED_APPS += []

MIDDLEWARE += []

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
]

DATABASES = {
    'default': SETTING_PRD_DIC['DATABASES']["default"]
}

