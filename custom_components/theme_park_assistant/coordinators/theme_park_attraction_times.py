from datetime import datetime, timedelta
import logging

from homeassistant.util.dt import (now)
from homeassistant.helpers.update_coordinator import (
  DataUpdateCoordinator
)

from ..const import (
  COORDINATOR_REFRESH_IN_SECONDS,
  DATA_THEME_PARK_ATTRACTION_TIMES,
  DATA_THEME_PARK_ATTRACTION_TIMES_COORDINATOR,
  DOMAIN,
  REFRESH_RATE_IN_MINUTES_ATTRACTION_TIMES,
)

from ..api_client import (ThemeParkWikiApiClient, ApiException)
from ..api_client.theme_park_attraction import ThemeParkAttraction
from . import BaseCoordinatorResult

_LOGGER = logging.getLogger(__name__)

class ThemeParkAttractionTimesCoordinatorResult(BaseCoordinatorResult):
  data: list[ThemeParkAttraction]

  def __init__(self, last_retrieved: datetime, request_attempts: int, data: list[ThemeParkAttraction]):
    super().__init__(last_retrieved, request_attempts, REFRESH_RATE_IN_MINUTES_ATTRACTION_TIMES)
    self.data = data

async def _async_get_theme_park_attraction_times(
  current_date: datetime,
  client: ThemeParkWikiApiClient,
  theme_park_id: str,
  previous_consumption: ThemeParkAttractionTimesCoordinatorResult | None
):
  if previous_consumption is None or current_date >= previous_consumption.next_refresh:
    
    try:
      data = await client.async_get_theme_park_attractions(theme_park_id)
      if data is not None:
        _LOGGER.debug(f'Retrieved theme park attraction times for {theme_park_id}')
        return ThemeParkAttractionTimesCoordinatorResult(current_date, 1, data)
    except Exception as e:
      if isinstance(e, ApiException) == False:
        raise

      result: ThemeParkAttractionTimesCoordinatorResult = None
      if previous_consumption is not None:
        result = ThemeParkAttractionTimesCoordinatorResult(
          previous_consumption.last_retrieved,
          previous_consumption.request_attempts + 1,
          previous_consumption.data
        )
        _LOGGER.warning(f'Failed to retrieve theme park attraction times data - using cached version. Next attempt at {result.next_refresh}')
      else:
        result = ThemeParkAttractionTimesCoordinatorResult(
          # We want to force into our fallback mode
          current_date - timedelta(minutes=REFRESH_RATE_IN_MINUTES_ATTRACTION_TIMES),
          2,
          None
        )
        _LOGGER.warning(f'Failed to retrieve theme park attraction times data. Next attempt at {result.next_refresh}')
      
      return result
  
  return previous_consumption

async def async_create_theme_park_attraction_times_coordinator(hass, client: ThemeParkWikiApiClient, theme_park_id: str):
  """Create theme park attraction times coordinator"""

  # Reset data as we might have new information
  hass.data[DOMAIN][theme_park_id][DATA_THEME_PARK_ATTRACTION_TIMES] = None

  async def async_update_data():
    """Fetch data from API endpoint."""
    current: datetime = now()
    previous_consumption = hass.data[DOMAIN][theme_park_id][DATA_THEME_PARK_ATTRACTION_TIMES] if DATA_THEME_PARK_ATTRACTION_TIMES in hass.data[DOMAIN][theme_park_id] else None
    hass.data[DOMAIN][theme_park_id][DATA_THEME_PARK_ATTRACTION_TIMES] = await _async_get_theme_park_attraction_times(
      current,
      client,
      theme_park_id,
      previous_consumption
    )
    
    return hass.data[DOMAIN][theme_park_id][DATA_THEME_PARK_ATTRACTION_TIMES]

  coordinator = DataUpdateCoordinator(
    hass,
    _LOGGER,
    name=f"theme_park_attraction_times_{theme_park_id}",
    update_method=async_update_data,
    update_interval=timedelta(seconds=COORDINATOR_REFRESH_IN_SECONDS),
    always_update=True
  )

  hass.data[DOMAIN][theme_park_id][DATA_THEME_PARK_ATTRACTION_TIMES_COORDINATOR] = coordinator

  return coordinator