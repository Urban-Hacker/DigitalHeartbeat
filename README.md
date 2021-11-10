# A Simple Digital Heartbeat

A simple lightweight and minimalist status page written in pure python with no dependencies.

A demo page can be found here: https://urban-hacker.github.io/SimpleDigitalHeartbeat/index.html

## Features

* Lightweight report page. Pure HTML and CSS. No javascripts.
* Embeds everything it needs to not require any dependencies from outside (no CDN javascript/css libs, etc).
* No complicated intermediate states. Either a command is successful and return 0 or it fails and will trigger a failure on the status page.
* It easy to group tests in subsections
* You can also custumize the header and the error messages that will be shown if anything fails.

## How to setup

Check the config.py to customize the configuration. Run status.py. The report will be called status.html.

## How the status is determined?

Tests are grouped in sections. Every tests are executed and depending on their results there can be different outcomes:
* Tests are binary (either it is a success or a failure). There are no intermediate state. 
* If no errors are found, this will flag the subsection as green indicating a success.
* If one error is found, this will flag the subsection as yellow indicating a warning.
* If more than one error, the subsection will be flagged as red indicating a major failure.

The overall result of the page is determined in the same way. Success if there are no failures, warning for one and an alert if more.

The global results will be kept and used in the Status History section.

## Advanced usage

By default, 91 previous aggregated results are kept. If you run the script every 10 minutes it means on average you will have the history of the previous 15 hours.
If you need more or less, it is possible to change this number.
You can also add custom sections with only text to add optional information eg: scheduled maintenance.

## Planned features

* A minimalist API to allow to extend features.
