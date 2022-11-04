# Description

This is a [Cabot Check Plugin](https://cabotapp.com/dev/writing-check-plugins.html) for running a [nim-waku](https://github.com/status-im/nim-waku) canary.

# Installation

The simplest way is to just use:
```sh
pip install git+git://github.com/status-im/cabot-check-nim-waku.git
```
Edit `conf/production.env` in your Cabot clone to include the plugin:
```
CABOT_PLUGINS_ENABLED=cabot_check_nim_waku,<other plugins>
```

# Configuration

This plugin requries one environment variable:
```sh
NIM_WAKU_CANARY_PATH=<path_to_nim_waku_canary_binary>
```

# API

The plugin exposes the standard check API under:
```
/plugins/cabot_check_nim_waku/api/nim_waku_checks/
```
Which accepts the standard `GET`/`POST`/`OPTIONS` methods.
