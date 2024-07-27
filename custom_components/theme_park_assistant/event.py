import logging

from .entities.theme_park_times import ThemeParkAssistantThemeParkTimes

from .const import (
  CONFIG_MAIN_THEME_PARK_ID,
  CONFIG_MAIN_THEME_PARK_NAME,
)

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
  _LOGGER.debug('Setting up event sensors')

  entities = []

  theme_park_id = config[CONFIG_MAIN_THEME_PARK_ID]
  theme_park_name = config[CONFIG_MAIN_THEME_PARK_NAME]

  entities.append(ThemeParkAssistantThemeParkTimes(hass, theme_park_id, theme_park_name))

  async_add_entities(entities)