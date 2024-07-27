from datetime import datetime
from math import floor
from ..api_client.theme_park_attraction import ThemeParkAttraction

def get_next_recommended_attraction(remaining_attractions: list, all_attractions: list[ThemeParkAttraction]):
  if all_attractions is None or remaining_attractions is None:
    return None

  best_attraction: ThemeParkAttraction | None = None
  for remaining_attraction in remaining_attractions:
    for attraction in all_attractions:
      if (attraction.id == remaining_attraction["id"] and 
          attraction.entity_type == "ATTRACTION" and 
          attraction.stand_by_wait_time_in_minutes is not None and 
          (best_attraction is None or attraction.stand_by_wait_time_in_minutes < best_attraction.stand_by_wait_time_in_minutes)):
        best_attraction = attraction
        break

  return best_attraction

class RecommendedShow:
  def __init__(self, show: ThemeParkAttraction, minutes_to_show: int):
    self.show = show
    self.minutes_to_show = minutes_to_show

def get_next_recommended_show(current: datetime, remaining_shows: list, all_attractions: list[ThemeParkAttraction], minimum_minutes: int):
  if all_attractions is None or remaining_shows is None:
    return None

  best_show: ThemeParkAttraction | None = None
  best_show_time_in_minutes: int | None = None
  for remaining_attraction in remaining_shows:
    for attraction in all_attractions:
      if (attraction.id == remaining_attraction["id"] and 
          attraction.entity_type == "SHOW"):
        
        next_time: datetime | None = None
        for time in attraction.show_times:
          if time.start_time > current and (next_time is None or time.start_time < next_time):
            next_time = time.start_time

        show_time_in_minutes = floor((next_time - current).total_seconds() / 60) if next_time is not None else None
        if (show_time_in_minutes is not None and 
            show_time_in_minutes >= minimum_minutes and
            (best_show_time_in_minutes is None or show_time_in_minutes < best_show_time_in_minutes)):
          best_show_time_in_minutes = show_time_in_minutes
          best_show = attraction

        break

  return RecommendedShow(best_show, best_show_time_in_minutes) if best_show is not None else None