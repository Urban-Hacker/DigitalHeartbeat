# Digital Heartbeat

A simple lightweight and minimalist status page written in pure python with no dependencies.

## Features

* Lightweight report page. Pure HTML and CSS.
* Javascript 100% optional and only used if you need automatic refresh.
* No complicated intermediate states. Either a command is successful and return 0 or it fails and will trigger a failure on the status page.
* It is possible to group services in subsections and custumize the header and the error messages that will be shown if something fails.

## How to setup

Check the config.py to customize the configuration.

## Planned features

* A minimalist API to allow to use the results in other system
* Having historical data (last 10 status report or something similar)
