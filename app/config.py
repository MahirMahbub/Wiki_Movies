""" App Configuration File"""
import os
from typing import List


class AppConfig:
    # App name
    APP_NAME = "EDN-Campaign"

    # Environments (these are already in .env file, again initializing here because of Windows Machine)
    ENV_LOCAL = os.getenv("ENV_LOCAL", "local")
    ENV_STAGING = os.getenv("ENV_STAGING", "staging")
    ENV_PRODUCTION = os.getenv("ENV_PRODUCTION", "production")

    # Set app environment here
    APP_ENVIRONMENT = os.getenv("APP_ENV", ENV_LOCAL)

    # Set App Host and Port
    PORT = 8000
    APP_HOST_NAME = '127.0.0.1'
    APP_HOST_PORT = int(os.getenv("APP_HOST_PORT", PORT))

    # DB Configurations
    DB_HOST = ""
    DB_PORT = ""
    DB_NAME = ""
    DB_USER_NAME = ""
    DB_PASSWORD = ""

    # Now setup DB URL here using above value
    DB_URL = ""
