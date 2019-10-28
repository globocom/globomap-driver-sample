# Globomap Driver Sample
Sample project for creating drivers for Globomap, including all the necessary logic for sending data. The data is inserted in API of [Globo Loader API](https://github.com/globocom/globomap-loader-api).

## Plugin environment variables configuration
All of the environment variables below must be set for the plugin to work properly. More variables may be necessary for your project, such as URLs and credentials of the data source you wish to consume. All variables are declared in [settings.py](globomap_driver_sample/settings.py).

| Variable                       |  Description                 | Example                                    |
|--------------------------------|------------------------------|--------------------------------------------|
| GLOBOMAP_LOADER_API_URL        | GloboMap Loader API endpoint | http://api.globomap.loader.domain.com:8080 |
| GLOBOMAP_LOADER_API_USER       | GloboMap Loader API user     | user                                       |
| GLOBOMAP_LOADER_API_PASSWORD   | GloboMap Loader API password | password                                   |
| SENTRY_DSN                     | Destination Sentry server.   | https://user:password@sentry.io/test       |
| SCHEDULER_FREQUENCY_EXEC       | Frequency of execution       | 0-6\|0-23                                  |
| ZBX_PASSIVE_MONITOR_SCHEDULER  | Zabbix monitor               | passive_abc_monitor_scheduler              |

## Cloning to your own driver project
To start working on your own Globomap Driver, use `make clone package=<package_name> project=<project-name>`. This will create the "project-name" repository in the same level as this project's repository.

## Formatting the data
In the [driver.py](globomap_driver_sample/driver.py) file, you can retrieve data from any source you need and format it into a payload. There, you can use the given internal methods to do so, as well as to make requests to retrieve said data. Remember to change all instances of "sample" in it to names that make sense for your service and the data it's mapping.
