import voluptuous as vol
import logging

from homeassistant.core import callback
from homeassistant.config_entries import (ConfigFlow, OptionsFlow)
from homeassistant.helpers import selector

from .const import (
  CONFIG_MAIN_MINIMUM_SHOW_TIME_IN_MINUTES,
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
    vol.Required(CONFIG_MAIN_MINIMUM_SHOW_TIME_IN_MINUTES): int
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
  
  @staticmethod
  @callback
  def async_get_options_flow(entry):
    return OptionsFlowHandler(entry)
  
class OptionsFlowHandler(OptionsFlow):
  """Handles options flow for the component."""

  def __init__(self, entry) -> None:
    self._entry = entry

  async def async_step_init(self, user_input):
    """Manage the options for the custom component."""

    if CONFIG_MAIN_THEME_PARK_ID in self._entry.data:
      config = dict(self._entry.data)
      if self._entry.options is not None:
        config.update(self._entry.options)

      schema = await __async_setup_schema__()

      return self.async_show_form(
        step_id="user",
        data_schema=self.add_suggested_values_to_schema(
          schema,
          {
            CONFIG_MAIN_MINIMUM_SHOW_TIME_IN_MINUTES: config[CONFIG_MAIN_MINIMUM_SHOW_TIME_IN_MINUTES] if CONFIG_MAIN_MINIMUM_SHOW_TIME_IN_MINUTES in config else 0
          }
        )
      )

    return self.async_abort(reason="not_supported")

  async def async_step_user(self, user_input):
    """Manage the options for the custom component."""

    if user_input is not None:
      config = dict(self._entry.data)
      config.update(user_input)

      return self.async_create_entry(title="", data=config)

    return self.async_abort(reason="not_supported")