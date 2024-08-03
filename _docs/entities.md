# Entities

The following entities are available when setting up your account.

## Next Recommended Attraction Minutes

`sensor.next_recommended_attraction_minutes_{{PARK_NAME}}`

This sensor will present the minutes for the queue of the next recommended attraction. This will be the attraction in your [Recommended Attractions](#recommended-attractions) that have the lowest available stand by wait time.

!!! note

    This will update every 5 minutes

| Attribute Name  | type | Note |
|-----------------|------|------|
| `attraction_id` | `string` | The id of the attraction that is recommended |

## Next Recommended Attraction

`sensor.next_recommended_attraction_{{PARK_NAME}}`

This sensor will present the name of the next recommended attraction. This will be the attraction in your [Recommended Attractions](#recommended-attractions) that have the lowest available stand by wait time.

!!! note

    This will update every 5 minutes

| Attribute Name  | type | Note |
|-----------------|------|------|
| `attraction_id` | `string` | The id of the attraction that is recommended |

## Next Recommended Show Minutes

`sensor.next_recommended_show_minutes_{{PARK_NAME}}`

This sensor will present the minutes for the queue of the next recommended show. This will be the show in your [Recommended Attractions](#recommended-attractions) that has the shortest time to the next show time.

!!! note

    This will update every 5 minutes

| Attribute Name  | type | Note |
|-----------------|------|------|
| `attraction_id` | `string` | The id of the show that is recommended |

## Next Recommended Show

`sensor.next_recommended_show_{{PARK_NAME}}`

This sensor will present the name of the next recommended show. This will be the show in your [Recommended Attractions](#recommended-attractions) that has the shortest time to the next show time.

!!! note

    This will update every 5 minutes

| Attribute Name  | type | Note |
|-----------------|------|------|
| `attraction_id` | `string` | The id of the show that is recommended |

## Recommended Attractions

`todo.remaining_attractions_{{PARK_NAME}}`

This sensor will present the todo list of remaining attractions that will be used when calculating the next recommended attractions/shows. You should use the [reset service](./services.md#reset_remaining_attractions) to populate this list.

## Theme Park Times

`event.theme_park_times_{{PARK_NAME}}`

This event will display the timestamp of when the [Theme Park Times](./events.md#remaining-attractions-updated) were last updated.