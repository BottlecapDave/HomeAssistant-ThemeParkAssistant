from datetime import datetime

from .theme_park_attraction_show_time import ThemeParkAttractionShowTime

class ThemeParkAttraction:

  def __init__(self,
               id: str,
               name: str,
               entity_type: str,
               status: str,
               show_times: list[ThemeParkAttractionShowTime] | None,
               stand_by_wait_time_in_minutes: int | None,
               single_rider_wait_time_in_minutes: int | None,
               last_updated: datetime
  ):
    self.id = id
    self.name = name
    self.entity_type = entity_type
    self.status = status
    self.show_times = show_times
    self.stand_by_wait_time_in_minutes = stand_by_wait_time_in_minutes
    self.single_rider_wait_time_in_minutes = single_rider_wait_time_in_minutes
    self.last_updated = last_updated

  def to_json(self):
    return {
      "id": self.id,
      "name": self.name,
      "entity_type": self.entity_type,
      "status": self.status,
      "show_times": list(map(lambda show_time: show_time.to_json(), self.show_times)) if self.show_times is not None else None,
      "stand_by_wait_time_in_minutes": self.stand_by_wait_time_in_minutes,
      "single_rider_wait_time_in_minutes": self.single_rider_wait_time_in_minutes,
      "last_updated": self.last_updated,
    }