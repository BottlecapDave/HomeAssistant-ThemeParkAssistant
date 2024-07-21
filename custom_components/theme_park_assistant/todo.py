import logging
import voluptuous as vol

from homeassistant.helpers import entity_platform

from .const import (
  CONFIG_MAIN_THEME_PARK_ID,
  CONFIG_MAIN_THEME_PARK_NAME,
  DATA_THEME_PARK_ATTRACTION_TIMES_COORDINATOR,
  DOMAIN,
)

from .entities.remaining_attractions import ThemeParkAssistantRemainingAttractions

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
  _LOGGER.debug('Setting up todo sensors')

  platform = entity_platform.async_get_current_platform()
  platform.async_register_entity_service(
    "reset_remaining_attractions",
    vol.All(
      vol.Schema(
        {
        },
        extra=vol.ALLOW_EXTRA,
      ),
    ),
    "async_reset_remaining_attractions"
  )

  entities = []

  theme_park_id = config[CONFIG_MAIN_THEME_PARK_ID]
  theme_park_name = config[CONFIG_MAIN_THEME_PARK_NAME]

  coordinator = hass.data[DOMAIN][theme_park_id][DATA_THEME_PARK_ATTRACTION_TIMES_COORDINATOR]
  entities.append(ThemeParkAssistantRemainingAttractions(hass, coordinator, theme_park_id, theme_park_name))

  async_add_entities(entities)