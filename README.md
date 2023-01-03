# Emu M-Bus Center

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![pre-commit][pre-commit-shield]][pre-commit]
[![Black][black-shield]][black]
[![Validate with Hassfest][hassfest-badge]][hassfest]

[![hacs][hacsbadge]][hacs]
[![Project Maintenance][maintenance-shield]][user_profile]

[![Discord][discord-shield]][discord]
[![Community Forum][forum-shield]][forum]

**This component will set up the following platforms.**

| Platform | Description                          |
| -------- | ------------------------------------ |
| `sensor` | Show info from Emu M-Bus Center API. |

## Installation

### Automated (suggested):

Just click here: [![Open in HACS.][my-hacs-badge]][open-in-hacs]

### Manual:

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `emu_m_bus_center`.
4. Download _all_ the files from the `custom_components/emu_m_bus_center/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant
7. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Emu M-Bus Center"

Using your HA configuration directory (folder) as a starting point you should now also have this:

```text
custom_components/emu_m_bus_center/__init__.py
custom_components/emu_m_bus_center/config_flow.py
custom_components/emu_m_bus_center/manifest.json
custom_components/emu_m_bus_center/sensor.py
```

## Configuration

Add an entry in your `configuration.yaml` like this:

```yaml
sensor:
  - platform: emu_m_bus_center
    ip_address: "IpOfYourSensor"
    unique_id:
      - "name_of_sensor_1": "id_of_sensor_1"
      - "name_of_sensor_2": "id_of_sensor_2"
      - "name_of_sensor_3": "id_of_sensor_3"
```

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

## Credits

This project was generated from [@oncleben31](https://github.com/oncleben31)'s [Home Assistant Custom Component Cookiecutter](https://github.com/oncleben31/cookiecutter-homeassistant-custom-component) template.

Code template was mainly taken from [@Ludeeus](https://github.com/ludeeus)'s [integration_blueprint][integration_blueprint] template

---

[integration_blueprint]: https://github.com/custom-components/integration_blueprint
[black]: https://github.com/psf/black
[black-shield]: https://img.shields.io/badge/code%20style-black-000000.svg
[commits-shield]: https://img.shields.io/github/commit-activity/y/redlukas/emu_mbus_center.svg
[commits]: https://github.com/redlukas/emu_mbus_center/commits/main
[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg
[discord]: https://discord.gg/Qa5fW2R
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/redlukas/emu_mbus_center.svg
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40redlukas-blue.svg
[pre-commit]: https://github.com/pre-commit/pre-commit
[pre-commit-shield]: https://img.shields.io/badge/pre--commit-enabled-brightgreen
[releases-shield]: https://img.shields.io/github/release/redlukas/emu_mbus_center.svg
[releases]: https://github.com/redlukas/emu_mbus_center/releases
[user_profile]: https://github.com/redlukas
[hassfest-badge]: https://github.com/redlukas/emu_mbus_center/workflows/Validate%20with%20Hassfest/badge.svg
[hassfest]: https://developers.home-assistant.io/blog/2020/04/16/hassfest/
[open-in-hacs]: https://my.home-assistant.io/redirect/hacs_repository/?owner=redlukas&repository=emu_mbus_center&category=integration
[my-hacs-badge]: https://my.home-assistant.io/badges/hacs_repository.svg
