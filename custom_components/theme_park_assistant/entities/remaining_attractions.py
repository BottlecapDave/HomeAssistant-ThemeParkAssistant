from homeassistant.core import callback
from homeassistant.components.todo import (TodoListEntity, TodoItem, TodoListEntityFeature, TodoItemStatus)
from homeassistant.helpers.update_coordinator import (
  CoordinatorEntity
)
from homeassistant.helpers.entity import generate_entity_id

from ..coordinators.theme_park_attraction_times import ThemeParkAttractionTimesCoordinatorResult
from ..const import EVENT_REMAINING_ATTRACTIONS_UPDATED

class ThemeParkAssistantRemainingAttractions(CoordinatorEntity, TodoListEntity):

  _attr_supported_features = (
    TodoListEntityFeature.DELETE_TODO_ITEM
  )

  def __init__(self, hass, coordinator, theme_park_id: str, theme_park_name: str):
    CoordinatorEntity.__init__(self, coordinator)
    self._hass = hass
    self._theme_park_id = theme_park_id
    self._theme_park_name = theme_park_name
    self._attributes = {}
    self._attr_todo_items = []
    self.entity_id = generate_entity_id("todo.{}", self.unique_id, hass=hass)

  @property
  def unique_id(self):
    """The id of the sensor."""
    return f"remaining_attractions_{self._theme_park_name}"
    
  @property
  def name(self):
    """Name of the sensor."""
    return f"Remaining Attractions ({self._theme_park_name})"

  @property
  def extra_state_attributes(self):
    """Attributes of the sensor."""
    return self._attributes
  
  @callback
  async def async_reset_remaining_attractions(self):
    """Reset the todo list with the attractions for the park"""
    result: ThemeParkAttractionTimesCoordinatorResult = self.coordinator.data if self.coordinator is not None and self.coordinator.data is not None else None

    if result is not None and result.data is not None:
      self._attr_todo_items = []
      for attraction in result.data:
        if (attraction.status not in ("REFURBISHMENT")):
          self._attr_todo_items.append(TodoItem(summary=attraction.name, uid=attraction.id, status=TodoItemStatus.NEEDS_ACTION))

    await self._async_sync_todo_items()

  async def async_delete_todo_items(self, uids: list[str]) -> None:
    """Delete a To-do item."""

    new_todo_list = []
    for todo in self._attr_todo_items:
      if todo.uid not in uids:
        new_todo_list.append(todo)

    self._attr_todo_items = new_todo_list
    await self._async_sync_todo_items()

  async def _async_sync_todo_items(self):
    self._hass.bus.async_fire(EVENT_REMAINING_ATTRACTIONS_UPDATED, 
      { 
        "theme_park_id": self._theme_park_id,
        "remaining_attractions": list(map(lambda todo: { "id": todo.uid, "name": todo.summary }, self._attr_todo_items))
      })

    self.async_write_ha_state()