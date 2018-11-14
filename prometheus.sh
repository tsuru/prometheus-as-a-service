#!/bin/sh
# Copyright 2018 tsuru authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

if [[ "$TARGET_ENDPOINT" != "" ]]; then sed -i s/localhost:9090/$TARGET_ENDPOINT/g /etc/prometheus/prometheus.yml; fi
/bin/prometheus $1 $2 $3 $4
