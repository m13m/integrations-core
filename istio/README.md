# Istio check

## Overview

Use the Datadog Agent to monitor how well Istio is performing.

* Collect metrics on what apps are making what kinds of requests
* Look at how applications are using bandwidth
* Understand istio's resource consumption

## Setup

Find below instructions to install and configure the check when running the Agent on a host. See the [Autodiscovery Integration Templates documentation][1] to learn how to apply those instructions to a containerized environment.

### Installation

Istio is included in the Datadog Agent. So, just [install the Agent][2] on your istio servers or in your cluster and point it at Istio.

### Configuration

#### Connect the Agent

Edit the `istio.d/conf.yaml` file, in the `conf.d/` folder at the root of your [Agent's configuration directory][3], to connect it to Istio. See the [sample istio.d/conf.yaml][4] for all available configuration options:

```
init_config:

instances:
  - istio_mesh_endpoint: http://istio-telemetry.istio-system:42422/metrics
    mixer_endpoint: http://istio-telemetry.istio-system:15014/metrics
    galley_endpoint: http://istio-galley.istio-system:15014/metrics
    pilot_endpoint: http://istio-pilot.istio-system:15014/metrics
    citadel_endpoint: http://istio-citadel.istio-system:15014/metrics
    send_histograms_buckets: true
```

Each of the endpoints are optional, but at least one must be configured. See the [istio documentation][5] to learn more about the prometheus adapter.

### Validation

[Run the Agent's `info` subcommand][6] and look for `istio` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][7] for a list of metrics provided by this check.

### Events
The Istio check does not include any events.

### Service Checks
The Istio check does not include any service checks.

## Troubleshooting
Need help? Contact [Datadog support][8].

## Further Reading
Additional helpful documentation, links, and articles:

- [Monitor your Istio service mesh with Datadog][9]

[1]: https://docs.datadoghq.com/agent/autodiscovery/integrations
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/?tab=agentv6#agent-configuration-directory
[4]: https://github.com/DataDog/integrations-core/blob/master/istio/datadog_checks/istio/data/conf.yaml.example
[5]: https://istio.io/docs/tasks/telemetry/metrics/querying-metrics
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6#agent-status-and-information
[7]: https://github.com/DataDog/integrations-core/blob/master/istio/metadata.csv
[8]: https://docs.datadoghq.com/help
[9]: https://www.datadoghq.com/blog/monitor-istio-with-datadog
