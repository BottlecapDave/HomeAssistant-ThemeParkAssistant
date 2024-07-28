from homeassistant.core import callback
from homeassistant.components.sensor import (SensorEntity)
from homeassistant.helpers.update_coordinator import (
  CoordinatorEntity
)
from homeassistant.helpers.entity import generate_entity_id

from ..const import EVENT_NEW_RECOMMENDED_ATTRACTION, EVENT_REMAINING_ATTRACTIONS_UPDATED
from ..api_client.theme_park_attraction import ThemeParkAttraction
from ..coordinators.theme_park_attraction_times import ThemeParkAttractionTimesCoordinatorResult
from ..utils.recommendations import get_next_recommended_attraction

class ThemeParkAssistantNextRecommendedAttraction(CoordinatorEntity, SensorEntity):

  def __init__(self, hass, coordinator, theme_park_id: str, theme_park_name: str):
    CoordinatorEntity.__init__(self, coordinator)
    self._hass = hass
    self._theme_park_id = theme_park_id
    self._theme_park_name = theme_park_name
    self._attributes = {}
    self._remaining_attractions = []
    self.entity_id = generate_entity_id("sensor.{}", self.unique_id, hass=hass)
    self._recommended_attraction: ThemeParkAttraction | None = None
    self._state = None

  @property
  def unique_id(self):
    """The id of the sensor."""
    return f"next_recommended_attraction_{self._theme_park_name}"
    
  @property
  def name(self):
    """Name of the sensor."""
    return f"Next Recommended Attraction ({self._theme_park_name})"

  @property
  def extra_state_attributes(self):
    """Attributes of the sensor."""
    return self._attributes
  
  @property
  def native_value(self):
    return self._state

  async def async_added_to_hass(self):
    """Call when entity about to be added to hass."""
    # If not None, we got an initial value.
    await super().async_added_to_hass()
    self._hass.bus.async_listen(EVENT_REMAINING_ATTRACTIONS_UPDATED, self._async_handle_event)

  @callback
  def _handle_coordinator_update(self) -> None:
    """Calculate the next recommended attraction"""
    self._calculate_next_recommended_attraction()
    super()._handle_coordinator_update()

  @callback
  async def _async_handle_event(self, event) -> None:
    if (event.data is not None and "theme_park_id" in event.data and event.data["theme_park_id"] == self._theme_park_id and "remaining_attractions" in event.data):
      self._remaining_attractions = event.data["remaining_attractions"]
      self._calculate_next_recommended_attraction()
      self.async_write_ha_state()

  def _calculate_next_recommended_attraction(self) -> None:
    result: ThemeParkAttractionTimesCoordinatorResult = self.coordinator.data if self.coordinator is not None and self.coordinator.data is not None else None

    if result is not None and result.data is not None:
      new_recommended_attraction = get_next_recommended_attraction(self._remaining_attractions, result.data)

      if new_recommended_attraction is not None and (self._recommended_attraction is None or new_recommended_attraction.id != self._recommended_attraction.id):
        self._hass.async_fire(EVENT_NEW_RECOMMENDED_ATTRACTION, {
          "theme_park_id": self._theme_park_id,
          "attraction_id": new_recommended_attraction.id,
          "attraction_name": new_recommended_attraction.name,
          "is_show": False,
          "minutes": new_recommended_attraction.stand_by_wait_time_in_minutes
        })
      
      self._recommended_attraction = new_recommended_attraction
      self._state = self._recommended_attraction.name if self._recommended_attraction is not None else None
      self._attributes = {
        "attraction_id": self._recommended_attraction.id if self._recommended_attraction is not None else None,
      }