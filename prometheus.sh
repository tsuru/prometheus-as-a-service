#!/bin/sh

if [[ "$TARGET_ENDPOINT" != "" ]]; then sed -i s/localhost:9090/$TARGET_ENDPOINT/g /etc/prometheus/prometheus.yml; fi
/bin/prometheus $1 $2 $3 $4
