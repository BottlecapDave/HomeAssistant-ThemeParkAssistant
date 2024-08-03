# Events

The following events are raised by the integration. These events power various entities and can also be used within automations.

## Remaining Attractions Updated

`theme_park_assistant_remaining_attractions_updated`

This is fired when the remaining attractions todo list is updated.

| Attribute | Type | Description |
|-----------|------|-------------|
| `theme_park_id` | `string` | The id of the theme park the event is for |
| `remaining_attractions` | `array` | The collection of remaining attractions |

For each attraction, the following attributes are available

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | `string` | The id of the attraction |
| `name` | `string` | The name of the attraction |

## Theme Park Times Updated

`theme_park_assistant_theme_park_times_updated`

This is fired when the theme park times are updated. This aims to fire every 5 minutes.

| Attribute | Type | Description |
|-----------|------|-------------|
| `theme_park_id` | `string` | The id of the theme park the event is for |
| `times` | `array` | The collection of attractions and their times |

For each attraction, the following attributes are available

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | `string` | The id of the attraction |
| `name` | `string` | The name of the attraction |
| `entity_type` | `string` | The type of attraction |
| `status` | `string` | The current status of the attraction |
| `show_times` | `array` | The collection of show times for the attraction. This will only be populated for `entity_type` of value `SHOW` |
| `stand_by_wait_time_in_minutes` | `integer` | The number of minutes for the stand by queue. This will only be populated for `entity_type` of value `ATTRACTION` |
| `single_rider_wait_time_in_minutes` | `integer` | The number of minutes for the single rider. This will only be populated for `entity_type` of value `ATTRACTION` |
| `last_updated` | `datetime` | The datetime the times were last updated |

For each show time, the following attribute are available

| Attribute | Type | Description |
|-----------|------|-------------|
| `start_time` | `datetime` | The start time of the show |
| `end_time` | `datetime` | The end time of the show |

## New Recommended Attraction/Show

`theme_park_assistant_new_recommended_attraction`

This is fired when a new recommended attraction or show is selected.

| Attribute | Type | Description |
|-----------|------|-------------|
| `theme_park_id` | `string` | The id of the theme park the event is for |
| `attraction_id` | `string` | The id of the recommended attraction |
| `attraction_name` | `string` | The name of the recommended attraction |
| `is_show` | `boolean` | Determines if the recommended attraction is a show |
| `minutes` | `integer` | The number of minutes for the recommended attraction |