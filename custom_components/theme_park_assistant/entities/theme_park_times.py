import logging

from homeassistant.core import HomeAssistant, callback

from homeassistant.components.event import (
    EventEntity,
    EventExtraStoredData,
)
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.entity import generate_entity_id

from ..const import EVENT_THEME_PARK_TIMES_UPDATED
from ..utils.attributes import dict_to_typed_dict

_LOGGER = logging.getLogger(__name__)

class ThemeParkAssistantThemeParkTimes(EventEntity, RestoreEntity):
  """Sensor for the park times"""

  _unrecorded_attributes = frozenset({ 'times' })

  def __init__(self, hass: HomeAssistant, theme_park_id: str, theme_park_name: str):
    """Init sensor."""
    self._hass = hass
    self._theme_park_id = theme_park_id
    self._theme_park_name = theme_park_name
    self._attributes = {}
    self._attr_todo_items = []
    self.entity_id = generate_entity_id("event.{}", self.unique_id, hass=hass)
    self._state = None
    self._last_updated = None

    self._attr_event_types = [EVENT_THEME_PARK_TIMES_UPDATED]

  @property
  def unique_id(self):
    """The id of the sensor."""
    return f"theme_park_times_{self._theme_park_name}"
    
  @property
  def name(self):
    """Name of the sensor."""
    return f"Theme Park Times ({self._theme_park_name})"

  async def async_added_to_hass(self):
    """Call when entity about to be added to hass."""
    # If not None, we got an initial value.
    await super().async_added_to_hass()
    
    self._hass.bus.async_listen(self._attr_event_types[0], self._async_handle_event)

  async def async_get_last_event_data(self):
    data = await super().async_get_last_event_data()
    return EventExtraStoredData.from_dict({
      "last_event_type": data.last_event_type,
      "last_event_attributes": dict_to_typed_dict(data.last_event_attributes),
    })

  @callback
  def _async_handle_event(self, event) -> None:
    if (event.data is not None and "theme_park_id" in event.data and event.data["theme_park_id"] == self._theme_park_id):
      self._trigger_event(event.event_type, event.data)
      self.async_write_ha_state()