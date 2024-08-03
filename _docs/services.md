# Services

## reset_remaining_attractions

Resets the remaining attractions list with all attractions for the associated park.

| Attribute                | Optional | Description                                                                                                           |
| ------------------------ | -------- | ------------------------------- |
| `target.entity_id`       | `no`     | The name of the sensor to reset |

### Automation Example

Below is an example of resetting the remaining attractions todo list every day at 08:00.

!!! info

    This is probably not how this service should be used, but is for demonstration purposes only

```yaml
automations:
  - id: 2446efb1-730a-4447-a7b9-add5f778a334
    alias: Theme Park Assistant - Reset Disney California Adventure
    trigger:
    - platform: time
      at: '08:00:00'
    condition: []
    action:
    - service: theme_park_assistant.reset_remaining_attractions
      data: {}
      target:
        entity_id:
          - todo.remaining_attractions_disney_california_adventure_park
```

## clear_remaining_attractions

Clears all attractions from the todo list.

| Attribute                | Optional | Description                                                                                                           |
| ------------------------ | -------- | ------------------------------- |
| `target.entity_id`       | `no`     | The name of the sensor to clear |

### Automation Example

Below is an example of resetting the remaining attractions todo list every day at 00:01.

```yaml
automations:
  - id: 2446efb1-730a-4447-a7b9-add5f778a334
    alias: Theme Park Assistant - Clear Disney California Adventure
    trigger:
    - platform: time
      at: '00:01:00'
    condition: []
    action:
    - service: theme_park_assistant.clear_remaining_attractions
      data: {}
      target:
        entity_id:
          - todo.remaining_attractions_disney_california_adventure_park
```
