# TgBotTemplate

<!--
[![Docker Pulls](https://img.shields.io/docker/pulls/viers/rumblerunner.svg)](https://hub.docker.com/r/viers/rumblerunner/)
[![Build and publish](https://github.com/KrusnikViers/RumbleRunner/actions/workflows/github-actions.yml/badge.svg)](https://github.com/KrusnikViers/RumbleRunner/actions/)
[![Coverage - Codecov](https://codecov.io/gh/KrusnikViers/RumbleRunner/branch/master/graph/badge.svg)](https://codecov.io/gh/KrusnikViers/RumbleRunner)
[![Maintainability](https://api.codeclimate.com/v1/badges/ea5b891843b7f3655b71/maintainability)](https://codeclimate.com/github/KrusnikViers/RumbleRunner/maintainability)
-->

## Before the start

Every Telegram bot needs token from the @BotFather. When registering a token, keep in mind:

* For participating in groups, Group mode should be enabled;
* To see group message history, Group privacy mode should be disabled.

Options must be passed via configuration.ini file. By default, bot will be looking for `configuration.ini` file in the
root directory (same level with this README file), or you can specify other path using `--config` parameter.

## How to build custom bot on top

See comments in `__init__.py` files in `app/bot` directory (ideally, this is only directory you should be working with).
Of course, you are free to take a look/change code in the rest of the project, however, template is configured so that
only `app/bot` should be changed. Some functions/definitions for you to use are exposed in app/public module.

* Define your data models in `app/bot/models` module.
* Generate DB migrations for new models in `app/bot/migrations` (using `scripts/update_migrations.py`)
* Place your handlers logic in `app/bot/core` module.
* Add your handlers to the appropriate file in `app/bot/routing` module.

## How to run as a developer

Project root directory should be added to `PYTHONPATH`. There are few scripts in `/scripts` directory, that are useful
for the development:

* `update_migrations.py`: autogenerate migrations from the updated models. Requires configuration.
* `run_tests.py`: launch python tests.
* `run_bot.py`: launch bot itself. Requires configuration.

## How to run via Docker

Path to db directory is optional.

```
docker run --restart always --name <instance name> -d \
 -v <path to configuration>:/instance/configuration.ini \
 -v <path to the db directory>:/instance/storage \
 <docker image name>
```

