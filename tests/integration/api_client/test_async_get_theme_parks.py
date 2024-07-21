import pytest

from integration import get_test_context
from custom_components.theme_park_assistant.api_client import ThemeParkWikiApiClient

@pytest.mark.asyncio
async def test_when_get_theme_parks_is_called_then_theme_parks_returned():
    # Arrange
    context = get_test_context()
    client = ThemeParkWikiApiClient()

    # Act
    result = await client.async_get_theme_parks()

    # Assert
    assert result is not None
    assert len(result) > 0

    for theme_park in result:
        assert theme_park.destination_id is not None and theme_park.destination_id != ""
        assert theme_park.destination_name is not None and theme_park.destination_name != ""
        assert theme_park.destination_slug is not None and theme_park.destination_slug != ""
        assert theme_park.id is not None and theme_park.id != ""
        assert theme_park.name is not None and theme_park.name != ""