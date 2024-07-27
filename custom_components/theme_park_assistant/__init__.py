import logging
import asyncio

from homeassistant.exceptions import ConfigEntryNotReady

from .const import (
  DOMAIN,

  CONFIG_MAIN_THEME_PARK_ID,

  DATA_API_CLIENT,
)

from .api_client import ThemeParkWikiApiClient
from .coordinators.theme_park_attraction_times import async_create_theme_park_attraction_times_coordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["event", "sensor", "todo"]

async def async_setup_entry(hass, entry):
  """This is called from the config flow."""
  hass.data.setdefault(DOMAIN, {})

  config = dict(entry.data)

  if entry.options:
    config.update(entry.options)

  if CONFIG_MAIN_THEME_PARK_ID in config:
    await async_setup_dependencies(hass, config)

    # Forward our entry to setup our default sensors
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
  
  entry.async_on_unload(entry.add_update_listener(options_update_listener))

  return True

async def async_setup_dependencies(hass, config):
  """Setup the coordinator and api client which will be shared by various entities"""
  theme_park_id = config[CONFIG_MAIN_THEME_PARK_ID]
  if hass.data[DOMAIN] is None:
    hass.data[DOMAIN] = dict({
      theme_park_id: {}
    })

  if theme_park_id not in hass.data[DOMAIN]:
    hass.data[DOMAIN][theme_park_id] = dict({})

  hass.data[DOMAIN][theme_park_id][DATA_API_CLIENT] = ThemeParkWikiApiClient()

  await async_create_theme_park_attraction_times_coordinator(hass, hass.data[DOMAIN][theme_park_id][DATA_API_CLIENT], theme_park_id)

async def options_update_listener(hass, entry):
  """Handle options update."""
  await hass.config_entries.async_reload(entry.entry_id)

async def async_unload_entry(hass, entry):
    """Unload a config entry."""
    unload_ok = True
    if CONFIG_MAIN_THEME_PARK_ID in entry.data:
      unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    return unload_ok