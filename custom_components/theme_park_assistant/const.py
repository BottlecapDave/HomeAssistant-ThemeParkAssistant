import voluptuous as vol
import homeassistant.helpers.config_validation as cv

DOMAIN = "theme_park_assistant"

CONFIG_MAIN_THEME_PARK_ID = "theme_park_id"
CONFIG_MAIN_THEME_PARK_NAME = "theme_park_name"
CONFIG_MAIN_MINIMUM_SHOW_TIME_IN_MINUTES = "minimum_show_time_in_minutes"

DATA_API_CLIENT = "api_client"

DATA_THEME_PARK_ATTRACTION_TIMES_COORDINATOR = "theme_park_attraction_times_coordinator"
DATA_THEME_PARK_ATTRACTION_TIMES = "theme_park_attraction_times"

COORDINATOR_REFRESH_IN_SECONDS = 60
REFRESH_RATE_IN_MINUTES_ATTRACTION_TIMES = 5

EVENT_REMAINING_ATTRACTIONS_UPDATED = "theme_park_assistant_remaining_attractions_updated"
EVENT_THEME_PARK_TIMES_UPDATED = "theme_park_assistant_theme_park_times_updated"
EVENT_NEW_RECOMMENDED_ATTRACTION = "theme_park_assistant_new_recommended_attraction"