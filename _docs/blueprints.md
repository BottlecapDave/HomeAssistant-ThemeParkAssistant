# Blueprints

[Blueprints](https://www.home-assistant.io/docs/automation/using_blueprints/) are an excellent way to get you up and running with the integration quickly. They can also be used as a guide for setting up new automations which you can tailor to your needs. 

## Rates

### Alert when recommended attraction or show updates

[Install blueprint](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2FBottlecapDave%2FHomeAssistant-ThemeParkAssistant%2Fblob%2Fdevelop%2F_docs%2Fblueprints%2Ftheme_park_assistant_attraction_updated.yaml) | [Source](./blueprints/theme_park_assistant_attraction_updated.yaml)

This blueprint will run every time the recommended attraction of show updates and has been designed to be added in conjunction with actionable notifications via the HA mobile app. Below is an example of how this could be setup

```yaml
- id: 7f8f50d5-788c-484e-9e84-157edb1e9253
  alias: Theme Park Assistant - Recommended Attraction Updated
  use_blueprint:
    path: BottlecapDave/theme_park_assistant_attraction_updated.yaml
    input:
      todo_list: todo.remaining_attractions_disney_california_adventure_park
      actions:
      - service: notify.mobile_app_my_phone
        data:
          message: '{{ message }}'
          data:
            actions:
            - action: '{{ action_complete }}'
              title: Remove
            - action: '{{ action_ignore }}'
              title: Ignore
```