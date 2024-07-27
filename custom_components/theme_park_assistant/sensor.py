import logging

from .const import (
  CONFIG_MAIN_MINIMUM_SHOW_TIME_IN_MINUTES,
  CONFIG_MAIN_THEME_PARK_ID,
  CONFIG_MAIN_THEME_PARK_NAME,
  DATA_THEME_PARK_ATTRACTION_TIMES_COORDINATOR,
  DOMAIN,
)
from .entities.next_recommended_attraction import ThemeParkAssistantNextRecommendedAttraction
from .entities.next_recommended_attraction_minutes import ThemeParkAssistantNextRecommendedAttractionMinutes
from .entities.next_recommended_show import ThemeParkAssistantNextRecommendedShow
from .entities.next_recommended_show_minutes import ThemeParkAssistantNextRecommendedShowMinutes

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
  """Setup sensors based on our entry"""

  config = dict(entry.data)

  if entry.options:
    config.update(entry.options)

  if CONFIG_MAIN_THEME_PARK_ID in entry.data:
    await async_setup_main_sensors(hass, config, async_add_entities)

  return True

async def async_setup_main_sensors(hass, config, async_add_entities):
  _LOGGER.debug('Setting up sensors')

  entities = []

  theme_park_id = config[CONFIG_MAIN_THEME_PARK_ID]
  theme_park_name = config[CONFIG_MAIN_THEME_PARK_NAME]
  minimum_minutes = config[CONFIG_MAIN_MINIMUM_SHOW_TIME_IN_MINUTES] if CONFIG_MAIN_MINIMUM_SHOW_TIME_IN_MINUTES in config else 0

  coordinator = hass.data[DOMAIN][theme_park_id][DATA_THEME_PARK_ATTRACTION_TIMES_COORDINATOR]
  entities.append(ThemeParkAssistantNextRecommendedAttraction(hass, coordinator, theme_park_id, theme_park_name))
  entities.append(ThemeParkAssistantNextRecommendedAttractionMinutes(hass, coordinator, theme_park_id, theme_park_name))
  entities.append(ThemeParkAssistantNextRecommendedShow(hass, coordinator, theme_park_id, theme_park_name, minimum_minutes))
  entities.append(ThemeParkAssistantNextRecommendedShowMinutes(hass, coordinator, theme_park_id, theme_park_name, minimum_minutes))

  async_add_entities(entities)