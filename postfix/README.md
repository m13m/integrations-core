# Postfix Check

![Postfix Graph][1]

## Overview

This check monitors the size of all your Postfix queues.

## Setup

Find below instructions to install and configure the check when running the Agent on a host. See the [Autodiscovery Integration Templates documentation][2] to learn how to apply those instructions to a containerized environment.

### Installation

The Postfix check is included in the [Datadog Agent][3] package, so you don't need to install anything else on your Postfix servers.

## Configuration
This check can be configured to use the `find` command which requires granting the dd-agent user sudo access to get a count of messages in the `incoming`, `active`, and `deferred` mail queues.

Optionally, you can configure the agent to use a built in `postqueue -p` command to get a count of messages in the `active`, `hold`, and `deferred` mail queues. `postqueue` is exectued with set-group ID privileges without the need for sudo.

**WARNING**: Using `postqueue` to monitor the mail queues will not report a count of messages for the `incoming` queue.

### Using sudo
Edit the file `postfix.d/conf.yaml`, in the `conf.d/` folder at the root of your [Agent's configuration directory][4]. See the [sample postfix.d/conf.yaml][5] for all available configuration options:

```
init_config:
  postfix_user: postfix

instances:
  # add one instance for each postfix service you want to track
  - directory: /var/spool/postfix
    queues:
      - incoming
      - active
      - deferred
#   tags:
#     - optional_tag1
#     - optional_tag2
```

For each mail queue in `queues`, the Agent forks a `find` on its directory.
It uses `sudo` to do this with the privileges of the Postfix user, so you must
add the following lines to `/etc/sudoers` for the Agent's user, `dd-agent`,
assuming Postfix runs as `postfix`:
```
dd-agent ALL=(postfix) NOPASSWD:/usr/bin/find /var/spool/postfix/incoming -type f
dd-agent ALL=(postfix) NOPASSWD:/usr/bin/find /var/spool/postfix/active -type f
dd-agent ALL=(postfix) NOPASSWD:/usr/bin/find /var/spool/postfix/deferred -type f
```

### Using postqueue
Edit the `postfix.d/conf.yaml` file, in the `conf.d/` folder at the root of your [Agent's configuration directory][4]:

```
init_config:
  postqueue: true

instances:
  # The config_directory option only applies when `postqueue: true`.
  # The config_directory is the location of the Postfix configuration directory
  # where main.cf lives.
  - config_directory: /etc/postfix
#   tags:
#     - optional_tag
#     - optional_tag0
```
For each `config_directory` in `instances`, the Agent forks a `postqueue -c` for the Postfix configuration directory.

Postfix has internal access controls that limit activities on the mail queue. By default, Postfix allows `anyone` to view the queue. On production systems where the Postfix installation may be configured with stricter access controls, you may need to grant the dd-agent user access to view the mail queue.

```
postconf -e "authorized_mailq_users = dd-agent"
```
http://www.postfix.org/postqueue.1.html
```
authorized_mailq_users (static:anyone)
```
List of users who are authorized to view the queue.

[Restart the Agent][6] to start sending Postfix metrics to Datadog.

#### Log collection

**Available for Agent >6.0**

Postfix sends logs to the syslog daemon, which then writes logs to the file system.

The naming convention and log file destinations are configurable:

```
/etc/syslog.conf:
    mail.err                                    /dev/console
    mail.debug                                  /var/log/maillog
```

1. Collecting logs is disabled by default in the Datadog Agent, enable it in your `datadog.yaml` file:

    ```yaml
      logs_enabled: true
    ```

2. Add the following configuration block to your `postfix.d/conf.yaml` file. Change the `path` and `service` parameter values based on your environment. See the [sample postfix.d/conf.yaml][6] for all available configuration options.

    ```yaml
      logs:
        - type: file
          path: /var/log/mail.log
          source: postfix
          service: myapp
    ```

3. [Restart the Agent][7].

### Validation

[Run the Agent's status subcommand][9] and look for `postfix` under the Checks section.

## Data Collected
### Metrics
See [metadata.csv][10] for a list of metrics provided by this check.

### Events
The Postfix check does not include any events.

### Service Checks
The Postfix check does not include any service checks.

## Troubleshooting
Need help? Contact [Datadog support][11].

## Further Reading

Additional helpful documentation, links, and articles:

* [Monitor Postfix queue performance][7]


[1]: https://raw.githubusercontent.com/DataDog/integrations-core/master/postfix/images/postfixgraph.png
[2]: https://docs.datadoghq.com/agent/autodiscovery/integrations
[3]: https://app.datadoghq.com/account/settings#agent
[4]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/?tab=agentv6#agent-configuration-directory
[5]: https://github.com/DataDog/integrations-core/blob/master/postfix/datadog_checks/postfix/data/conf.yaml.example
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6#start-stop-and-restart-the-agent
[7]: https://www.datadoghq.com/blog/monitor-postfix-queues
[9]: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6#agent-status-and-information
[10]: https://github.com/DataDog/integrations-core/blob/master/postfix/metadata.csv
[11]: https://docs.datadoghq.com/help
