import logging
import json
import aiohttp

from homeassistant.util.dt import (parse_datetime)

from .theme_park import ThemePark
from .theme_park_attraction import ThemeParkAttraction
from .theme_park_attraction_show_time import ThemeParkAttractionShowTime

_LOGGER = logging.getLogger(__name__)

class ApiException(Exception): ...

class ServerException(ApiException): ...

class RequestException(ApiException): ...

class ThemeParkWikiApiClient:

  def __init__(self):
    self._base_url = 'https://api.themeparks.wiki/v1/'

  async def async_get_theme_parks(self) -> list[ThemePark]:
    """Get all time entries"""
    results = []

    async with aiohttp.ClientSession() as client:
      headers = {}
      url = f'{self._base_url}/destinations'
      async with client.get(url, headers=headers) as response:
        data = await self.__async_read_response__(response, url)
        if data is not None and "destinations" in data:
          for destination in data["destinations"]:
            destination_name = destination["name"]
            if "parks" not in destination:
              raise SystemError(f"Failed to find parks for destination '{destination_name}'")

            results.extend(list(map(lambda d: ThemePark(
              d["id"],
              d["name"],
              destination["id"],
              destination_name,
              destination["slug"],
            ), destination["parks"])))

    return results
  
  async def async_get_theme_park_attractions(self, theme_park_id: str) -> list[ThemeParkAttraction]:
    """Get all time entries"""
    results: list[ThemeParkAttraction] = []

    async with aiohttp.ClientSession() as client:
      headers = {}
      url = f'{self._base_url}/entity/{theme_park_id}/live'
      async with client.get(url, headers=headers) as response:
        data = await self.__async_read_response__(response, url)
        if data is not None and "liveData" in data:
          results.extend(list(map(lambda d: ThemeParkAttraction(
            d["id"],
            d["name"],
            d["entityType"],
            d["status"],
            list(map(lambda show_time: ThemeParkAttractionShowTime(parse_datetime(show_time["startTime"]), parse_datetime(show_time["endTime"])), d["showtimes"])) if "showtimes" in d else None,
            d["queue"]["STANDBY"]["waitTime"] if "queue" in d and "STANDBY" in d["queue"] and "waitTime" in d["queue"]["STANDBY"] else None,
            d["queue"]["SINGLE_RIDER"]["waitTime"] if "queue" in d and "SINGLE_RIDER" in d["queue"] and "waitTime" in d["queue"]["SINGLE_RIDER"] else None,
            parse_datetime(d["lastUpdated"])
          ), data["liveData"])))

    return results

  async def __async_read_response__(self, response, url):
    """Reads the response, logging any json errors"""

    text = await response.text()

    if response.status >= 400:
      if response.status >= 500:
        msg = f'DO NOT REPORT - ThemeParks.wiki server error ({url}): {response.status}; {text}'
        _LOGGER.debug(msg)
        raise ServerException(msg)
      elif response.status not in [401, 403, 404]:
        msg = f'Failed to send request ({url}): {response.status}; {text}'
        _LOGGER.debug(msg)
        raise RequestException(msg)
      return None

    try:
      return json.loads(text)
    except:
      raise ApiException(f'Failed to extract response json: {url}; {text}')
