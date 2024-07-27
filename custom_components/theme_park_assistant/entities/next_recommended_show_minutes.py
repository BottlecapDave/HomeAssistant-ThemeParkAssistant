from homeassistant.core import callback
from homeassistant.components.sensor import (SensorEntity)
from homeassistant.helpers.update_coordinator import (
  CoordinatorEntity
)
from homeassistant.helpers.entity import generate_entity_id
from homeassistant.const import (
    UnitOfTime,
)
from homeassistant.util.dt import (utcnow)

from ..const import EVENT_REMAINING_ATTRACTIONS_UPDATED
from ..coordinators.theme_park_attraction_times import ThemeParkAttractionTimesCoordinatorResult
from ..utils.recommendations import RecommendedShow, get_next_recommended_show

class ThemeParkAssistantNextRecommendedShowMinutes(CoordinatorEntity, SensorEntity):

  def __init__(self, hass, coordinator, theme_park_id: str, theme_park_name: str, minimum_minutes: int):
    CoordinatorEntity.__init__(self, coordinator)
    self._hass = hass
    self._theme_park_id = theme_park_id
    self._theme_park_name = theme_park_name
    self._attributes = {}
    self._remaining_attractions = []
    self.entity_id = generate_entity_id("sensor.{}", self.unique_id, hass=hass)
    self._recommended_attraction: RecommendedShow | None = None
    self._state = None
    self._minimum_minutes = minimum_minutes

  @property
  def unique_id(self):
    """The id of the sensor."""
    return f"next_recommended_show_minutes_{self._theme_park_name}"
    
  @property
  def name(self):
    """Name of the sensor."""
    return f"Next Recommended Show Minutes ({self._theme_park_name})"
  
  @property
  def unit_of_measurement(self):
    """Attributes of the sensor."""
    return UnitOfTime.MINUTES

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
      current = utcnow()
      self._recommended_attraction = get_next_recommended_show(current, self._remaining_attractions, result.data, self._minimum_minutes)
      
      self._state = self._recommended_attraction.minutes_to_show if self._recommended_attraction is not None else None
      self._attributes = {
        "attraction_id": self._recommended_attraction.show.id if self._recommended_attraction is not None else None,
      }