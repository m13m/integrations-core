# Agent Check: Varnish

![Varnish default dashboard][1]

## Overview

This check collects varnish metrics regarding:

* Clients: connections and requests
* Cache performance: hits, evictions, etc
* Threads: creations, failures, and threads queued
* Backends: successful, failed, and retried connections

It also submits service checks for the health of each backend.

## Setup

Find below instructions to install and configure the check when running the Agent on a host. See the [Autodiscovery Integration Templates documentation][2] to learn how to apply those instructions to a containerized environment.

### Installation

The Varnish check is included in the [Datadog Agent][3] package. No additional installation is needed on your server.

### Configuration

1. Edit the `varnish.d/conf.yaml` file, in the `conf.d/` folder at the root of your [Agent's configuration directory][4] to start collecting your Varnish [metrics](#metric-collection) and [logs](#log-collection). See the [sample varnish.d/conf.yaml][5] for all available configuration options.

2. [Restart the Agent][6].

#### Prepare Varnish

If you're running Varnish 4.1+, add the `dd-agent` system user to the Varnish group using:

```
sudo usermod -G varnish -a dd-agent
```

#### Metric collection

* Add this configuration block to your `varnish.d/conf.yaml` file to start gathering your [Varnish metrics](#metrics):

  ```
  init_config:

  instances:
    - varnishstat: /usr/bin/varnishstat        # or wherever varnishstat lives
      varnishadm: <PATH_TO_VARNISHADM_BIN>     # to submit service checks for the health of each backend
  #   secretfile: <PATH_TO_VARNISH_SECRETFILE> # if you configured varnishadm and your secret file isn't /etc/varnish/secret
  #   tags:
  #     - instance:production
  ```

  If you don't set `varnishadm`, the Agent won't check backend health. If you do set it, the Agent needs privileges to execute the binary with root privileges. Add the following to your `/etc/sudoers` file:

  ```
  dd-agent ALL=(ALL) NOPASSWD:/usr/bin/varnishadm
  ```

  See the [sample varnish.yaml][5] for all available configuration options.

* [Restart the Agent][6] to start sending Varnish metrics and service checks to Datadog.

##### Autodiscovery

Configuration of the Varnish check using Autodiscovery in containerized environments is not supported. Collecting metrics in this type of environment may be possible by pushing metrics to DogStatsD using a StatsD plugin. The following 3rd party plugins are available:

* [libvmod-statsd][7]
* [prometheus_varnish_exporter][8]

#### Log collection

**Available for Agent >6.0**

1. To enable Varnish logging uncomment the following in `/etc/default/varnishncsa`:

    ```
      VARNISHNCSA_ENABLED=1
    ```

2. Add the following at the end of the same file:

    ```
      LOG_FORMAT="{\"date_access\": \"%{%Y-%m-%dT%H:%M:%S%z}t\", \"network.client.ip\":\"%h\", \"http.auth\" : \"%u\", \"varnish.x_forwarded_for\" : \"%{X-Forwarded-For}i\", \"varnish.hit_miss\":  \"%{Varnish:hitmiss}x\", \"network.bytes_written\": %b, \"http.response_time\": %D, \"http.status_code\": \"%s\", \"http.url\": \"%r\", \"http.ident\": \"%{host}i\", \"http.method\": \"%m\", \"varnish.time_first_byte\" : %{Varnish:time_firstbyte}x, \"varnish.handling\" : \"%{Varnish:handling}x\", \"http.referer\": \"%{Referer}i\", \"http.useragent\": \"%{User-agent}i\" }"

      DAEMON_OPTS="$DAEMON_OPTS -c -a -F '${LOG_FORMAT}'"
    ```

3. Restart Varnishncsa to apply the changes.


4. Collecting logs is disabled by default in the Datadog Agent, enable it in your `datadog.yaml` file:

    ```yaml
      logs_enabled: true
    ```

5. Add this configuration block to your `varnish.d/conf.yaml` file to start collecting your Varnish logs:

    ```yaml
      logs:
        - type: file
          path: /var/log/varnish/varnishncsa.log
          source: varnish
          sourcecategory: http_web_access
          service: varnish
    ```
    Change the `path` and `service` parameter value and configure them for your environment.
    See the [sample varnish.yaml][5] for all available configuration options.

6. [Restart the Agent][6].

### Validation

[Run the Agent's status subcommand][10] and look for `varnish` under the Checks section.

## Data Collected
### Metrics
See [metadata.csv][11] for a list of metrics provided by this check.

### Events
The Varnish check does not include any events.

### Service Checks
**varnish.backend_healthy**:<br>
The Agent submits this service check if you configure `varnishadm`. It submits a service check for each Varnish backend, tagging each with `backend:<backend_name>`.

## Troubleshooting
Need help? Contact [Datadog support][12].

## Further Reading
Additional helpful documentation, links, and articles:

* [Top Varnish performance metrics][13]
* [How to collect Varnish metrics][14]
* [Monitor Varnish using Datadog][15]


[1]: https://raw.githubusercontent.com/DataDog/integrations-core/master/varnish/images/varnish.png
[2]: https://docs.datadoghq.com/agent/autodiscovery/integrations
[3]: https://app.datadoghq.com/account/settings#agent
[4]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/?tab=agentv6#agent-configuration-directory
[5]: https://github.com/DataDog/integrations-core/blob/master/varnish/datadog_checks/varnish/data/conf.yaml.example
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6#start-stop-and-restart-the-agent
[7]: https://github.com/jib/libvmod-statsd
[8]: https://github.com/jonnenauha/prometheus_varnish_exporter
[10]: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6#agent-status-and-information
[11]: https://github.com/DataDog/integrations-core/blob/master/varnish/metadata.csv
[12]: https://docs.datadoghq.com/help
[13]: https://www.datadoghq.com/blog/top-varnish-performance-metrics
[14]: https://www.datadoghq.com/blog/how-to-collect-varnish-metrics
[15]: https://www.datadoghq.com/blog/monitor-varnish-using-datadog
