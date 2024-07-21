import voluptuous as vol
import logging

from homeassistant.config_entries import (ConfigFlow)
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers import selector

from .const import (
  CONFIG_MAIN_THEME_PARK_NAME,
  DOMAIN,
  
  CONFIG_MAIN_THEME_PARK_ID,
)

from .api_client import ThemeParkWikiApiClient
from .api_client.theme_park import ThemePark

_LOGGER = logging.getLogger(__name__)

async def __async_setup_schema__():
  api_client = ThemeParkWikiApiClient()
  theme_parks = await api_client.async_get_theme_parks()
  theme_parks.sort(key=lambda theme_park: theme_park.name)

  theme_park_options = list(map(lambda theme_park: selector.SelectOptionDict(value=theme_park.id, label=f'{theme_park.name} ({theme_park.destination_name})'),
                                theme_parks))

  return vol.Schema({
    vol.Required(CONFIG_MAIN_THEME_PARK_ID): selector.SelectSelector(
        selector.SelectSelectorConfig(
            options=theme_park_options,
            mode=selector.SelectSelectorMode.DROPDOWN,
        )
    ),
  })


class ThemeParkAssistantConfigFlow(ConfigFlow, domain=DOMAIN): 
  """Config flow."""

  VERSION = 1

  async def async_setup_theme_park(self, user_input):
    """Setup the initial account based on the provided user input"""
    errors = {}

    api_client = ThemeParkWikiApiClient()
    theme_parks = await api_client.async_get_theme_parks()
    
    theme_park: ThemePark = None
    for theme_park in theme_parks:
      if theme_park.id == user_input[CONFIG_MAIN_THEME_PARK_ID]:
        theme_park = theme_park
        break

    if theme_park is not None:
      errors[CONFIG_MAIN_THEME_PARK_ID] = "theme_park_not_found"

    user_input[CONFIG_MAIN_THEME_PARK_NAME] = theme_park.name

    # Setup our basic sensors
    return self.async_create_entry(
      title=f"{theme_park.name} ({theme_park.destination_name})", 
      data=user_input
    )

  async def async_step_user(self, user_input):
    """Setup based on user config"""

    if user_input is not None:
      # We are setting up our initial stage
      if CONFIG_MAIN_THEME_PARK_ID in user_input:
        return await self.async_setup_theme_park(user_input)
      
    schema = await __async_setup_schema__()

    return self.async_show_form(
      step_id="user", data_schema=schema
    )