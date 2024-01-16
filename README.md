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

| Platform | Description                                                                                                                                                                                                                                                                                                        |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `hub`    | Each M-Bus Center is represented in HA as a Hub.<br>Each Hub will have zero or more Devices (each corresponding to one Meter you have connected to the M-Bus Center).<br>Each Device has some amount of Entities depending on the type of meter the Device represents. All of those entities are of type 'sensor'. |

## Overview

This Integration will help you pull data from an [Emu M-Bus Center](https://www.emuag.ch/en/products/m-bus-data-logger/) into Home Assistant.
This Work is done independently and is in no way affiliated, endorsed or funded by EMU.
I bought all my own hardware. Due to that, the Integration is currently only tested with the EMU M-Bus Center 250 with EMU Allrounder 3/75 Meters.
If someone from EMU wants to get in touch with me, open an issue on this Repo with your info.

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

Using your HA configuration directory (folder) as a starting point you should now also have this:

```text
custom_components/emu_m_bus_center/
├── config_flow.py
├── const.py
├── device_types
│   ├── devices.py
│   ├── emu_1_40_v4_15val.py
│   ├── emu_allrounder_v16_15val.py
│   ├── emu_allrounder_v16_17val.py
│   ├── emu_professional_v16_31val.py
│   └── emu_professional_v16_32val.py
├── emu_client.py
├── __init__.py
├── manifest.json
├── sensor.py
└── translations
    ├── de.json
    ├── en.json
    └── sk.json
```

## Configuration

No matter which way you installed the Integration, you need to restart Home Assistant before configuring the integration.

Go to the `Settings -> Devices & Services -> Integrations` tab of your Home Assistant instance.
Click `ADD INTEGRATION` and search for "Emu M-Bus Center".
The Configuration flow will start when you click install.
It will ask you for the IP address and Name of your M-Bus Center.
Then it will scan your Center for available Sensors and add them to Home Assistant.
If you do not want the default names for the meters, go to Integrations one more time, look for the Integration you just installed and click on the "x Devices".
You will find a list of the sensors that were found. If you click on a single sensor, you'll get a dialog with a pencil in the upper right corner.
Click that pencil and enter the Name you desire in the popup. By default, the name will be in the format `$SENSOR_NAME ($SITE_NAME)`.
Use the Web interface of your M-Bus Center as described below to match sensor/site name to the M-Bus Address you set on the meter itself.

## How to find the ID of your meter

1. Go to the Web interface of your Meter and load the overview. There you go to "Meter configuration".
   ![overview][overviewimg]
2. The IDs will be listed in the leftmost column.
   ![meters][metersimg]

## Tested devices

The integration has been tested on the following devices:

### Centers

| Manufacturer | Product          | Firmware Version |
| ------------ | ---------------- | ---------------- |
| EMU          | M-Bus Center 250 | 1.10.1.0.r0      |

EMU say that the EMU M-Center employs the same REST API as the M-Bus Center. I am therefore optimistic that this integration will work with the M-Center, but cannot confirm it.

### Meters

| Manufacturer | Product                     | Firmware Version<br>(as reported on meter's Display) | Firmware Version<br>(as reported by API) | Status          |
| ------------ | --------------------------- | ---------------------------------------------------- | ---------------------------------------- | --------------- |
| EMU          | Allrounder 3/75 M-Bus       | 1.4                                                  | 16                                       | Fully tested    |
| EMU          | Professional 3/75 M-Bus     | 1.4                                                  | 16                                       | Somewhat tested |
| EMU          | Professional II 3/100 M-Bus | 1.4                                                  | 16                                       | Experimental    |
| EMU          | 1/40                        | ???                                                  | 4                                        | Experimental    |

If you use one of the Meters that are marked as "Experimental", please open an issue and let me know if it works for you.

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

## Credits

This project was generated from [@oncleben31](https://github.com/oncleben31)'s [Home Assistant Custom Component Cookiecutter](https://github.com/oncleben31/cookiecutter-homeassistant-custom-component) template.

Code template was mainly taken from [@Ludeeus](https://github.com/ludeeus)'s [integration_blueprint][integration_blueprint] template

For the config flow, the initialization and update of the sensors I looked at many existing repos, chief among them [@CubicPill](https://github.com/CubicPill)'s [China Southern Power Grid Statistics](https://github.com/CubicPill/china_southern_power_grid_stat)

---

[integration_blueprint]: https://github.com/custom-components/integration_blueprint
[black]: https://github.com/psf/black
[black-shield]: https://img.shields.io/badge/code%20style-black-000000.svg
[commits-shield]: https://img.shields.io/github/commit-activity/y/redlukas/emu_mbus_center.svg
[commits]: https://github.com/redlukas/emu_mbus_center/commits/main
[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Default-green.svg
[discord]: https://discord.gg/Qa5fW2R
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=flat&logo=discord
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
[overviewimg]: ./images/overview.png
[metersimg]: ./images/meters.png
