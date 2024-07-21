import voluptuous as vol
import homeassistant.helpers.config_validation as cv

DOMAIN = "theme_park_assistant"

CONFIG_MAIN_THEME_PARK_ID = "theme_park_id"

DATA_API_CLIENT = "api_client"

DATA_THEME_PARK_ATTRACTION_TIMES_COORDINATOR = "theme_park_attraction_times_coordinator"
DATA_THEME_PARK_ATTRACTION_TIMES = "theme_park_attraction_times"

COORDINATOR_REFRESH_IN_SECONDS = 60
REFRESH_RATE_IN_MINUTES_ATTRACTION_TIMES = 5