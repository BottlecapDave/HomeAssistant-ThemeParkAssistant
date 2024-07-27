import pytest

from homeassistant.util.dt import (now)

from integration import get_test_context
from custom_components.theme_park_assistant.api_client import ThemeParkWikiApiClient

@pytest.mark.asyncio
async def test_when_get_theme_park_attractions_is_called_then_data_is_returned():
    # Arrange
    context = get_test_context()
    client = ThemeParkWikiApiClient()

    theme_park_id = "bc4005c5-8c7e-41d7-b349-cdddf1796427" # Universal Studios Hollywood

    # Act
    result = await client.async_get_theme_park_attractions(theme_park_id)

    # Assert
    assert result is not None
    assert len(result) > 0

    for attraction in result:
        assert attraction.id is not None and attraction.id != ""
        assert attraction.status is not None and attraction.status in ("OPERATING", "DOWN", "CLOSED", "REFURBISHMENT")
        assert attraction.entity_type is not None and attraction.entity_type in ("SHOW", "ATTRACTION")
        assert attraction.last_updated is not None and attraction.last_updated < now()
        assert attraction.name is not None and attraction.name != ""

        if attraction.entity_type == "SHOW":
            assert attraction.show_times is not None and len(attraction.show_times) >= 0
        else:
            assert attraction.show_times is None

        assert attraction.single_rider_wait_time_in_minutes is None or isinstance(attraction.single_rider_wait_time_in_minutes, int)
        assert attraction.stand_by_wait_time_in_minutes is None or isinstance(attraction.stand_by_wait_time_in_minutes, int)