#!/bin/bash

# configure and start the splunk forwarder
/opt/splunkforwarder/bin/splunk add forward-server $SPLUNK_FORWARD_SERVER --accept-license --no-prompt
/opt/splunkforwarder/bin/splunk add monitor "/var/log"
/opt/splunkforwarder/bin/splunk start

# run the clickhouse entrypoint script
/bin/bash /entrypoint.sh