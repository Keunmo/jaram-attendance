import os

from .base import *
from jaram_atd.util import get_server_info_value

SETTING_PRD_DIC = get_server_info_value("production")
SECRET_KEY = SETTING_PRD_DIC["SECRET_KEY"]

DEBUG = False

ALLOWED_HOSTS = ["34.85.10.140", "attendance.jaram.net"]

DATABASES = {
    'default': SETTING_PRD_DIC['DATABASES']["default"]
}

