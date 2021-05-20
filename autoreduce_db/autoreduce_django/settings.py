"""
Django settings for autoreduce_db project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import configparser
import os
from pathlib import Path

# Read the utilities .ini file that contains service credentials
CONFIG_ROOT = os.environ.get("AUTOREDUCTION_USERDIR", str(Path("~/.autoreduce").expanduser()))
INI_FILE = os.environ.get("AUTOREDUCTION_CREDENTIALS", os.path.join(f"{CONFIG_ROOT}/credentials.ini"))
CONFIG = configparser.ConfigParser()
CONFIG.read(INI_FILE)

DEV_DB_ROOT = Path(CONFIG_ROOT, "dev")
DEV_DB_ROOT.mkdir(parents=True, exist_ok=True)


def get_str(section, key):
    """Gets the value of a key"""
    return str(CONFIG.get(section, key))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-pd8%8fgsg*fo#0jvi9@0eh*+i(+vtaou2q@588cjr3=x5+$-r7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [  # Minimal apps required to setup JUST the ORM - (increases ORM setup speed)
    'autoreduce_db.reduction_viewer',
    'autoreduce_db.instrument',
]

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

if "RUNNING_VIA_PYTEST" in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
elif "AUTOREDUCTION_PRODUCTION" in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': get_str('DATABASE', 'name'),
            'USER': get_str('DATABASE', 'user'),
            'PASSWORD': get_str('DATABASE', 'password'),
            'HOST': get_str('DATABASE', 'host'),
            'PORT': get_str('DATABASE', 'port'),
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        }
    }

else:  # the default development DB backend
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(DEV_DB_ROOT, "sqlite3.db"),
        }
    }