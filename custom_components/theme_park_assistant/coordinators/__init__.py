from datetime import datetime
import logging

from ..utils.requests import calculate_next_refresh

_LOGGER = logging.getLogger(__name__)

class BaseCoordinatorResult:
  last_retrieved: datetime
  next_refresh: datetime
  request_attempts: int
  refresh_rate_in_minutes: float

  def __init__(self, last_retrieved: datetime, request_attempts: int, refresh_rate_in_minutes: float):
    self.last_retrieved = last_retrieved
    self.request_attempts = request_attempts
    self.next_refresh = calculate_next_refresh(last_retrieved, request_attempts, refresh_rate_in_minutes)
    _LOGGER.debug(f'last_retrieved: {last_retrieved}; request_attempts: {request_attempts}; refresh_rate_in_minutes: {refresh_rate_in_minutes}; next_refresh: {self.next_refresh}')