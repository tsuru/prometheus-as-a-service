# Copyright 2018 tsuru authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import os
import flask
from flask import Response
app = flask.Flask(__name__)

path1_count = 0
path2_count = 0

@app.route("/")
def hello():
    return "Hello world from tsuru"

@app.route("/metrics")
def metrics():
    global path1_count
    global path2_count
    metrics = """api_http_requests_total{{method="GET", handler="/path1"}} {}\napi_http_requests_total{{method="GET", handler="/path2"}} {}""".format(str(path1_count),str(path2_count))
    print(metrics)
    return Response(metrics, mimetype='text/plain')

@app.route("/path1")
def path1():
    global path1_count
    path1_count += 1
    return "Path1 count = {}".format(path1_count)

@app.route("/path2")
def path2():
    global path2_count
    path2_count += 1
    return "Path2 count = {}".format(path2_count)

if __name__ == "__main__":
    app.debug = True
    app.run(port=int(os.environ.get("PORT", "5000")), host="0.0.0.0")