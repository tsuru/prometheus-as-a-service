# Copyright 2018 tsuru authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import os

import flask
from flask import request
import logging
import sys
import requests
import re
import json
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

app = flask.Flask(__name__)

@app.route("/")
def hello():
    return "Prometheus As A Service"

@app.route("/resources", methods=["POST"])
def add_instance():
    # Variables
    name = request.form.get("name")
    description = request.form.get("description")
    tags = request.form.get("tag")
    team = request.form.get("team")
    plan = request.form.get("plan")
    pool='<pool-name>'
    app_name_prefix='prometheus-as-a-service-'
    token=os.environ['TSURU_TOKEN']
    app_name=app_name_prefix+name

    # Create the app
    data={"name" : app_name, "description" : description, "platform" : "static", "pool" : pool, "teamOwner" : team}
    headers={"Authorization" : "bearer {}".format(token)}
    r = requests.post("http://<tsuru-api-endpoint>/1.0/apps", data=data, headers=headers)

    app_url = json.loads(r.text)

    if re.match("20.", str(r.status_code)) is None:
        return r.reason, 500
    else:
        resposta="Prometheus instance {} created ".format(app_name)
        print(resposta)

    # Deploy the app with prometheus image
    data={"image" : "docker.artifactory.globoi.com/isidio/prometheus", "origin" : "image"}
    r = requests.post("http://<tsuru-api-endpoint>/1.0/apps/{}/deploy".format(app_name), data=data, headers=headers)

    if re.match("20.", str(r.status_code)) is None:
        return r.reason, 500
    else:
        resposta="Prometheus instance {} deployed.\n Access your prometheus instance: {}".format(app_name, app_url)
        print(resposta)
        return resposta, 200

@app.route("/resources/<name>/bind-app", methods=["POST"])
def bind_app(name):
    app_name_prefix='prometheus-as-a-service-'
    app_name=app_name_prefix+name
    
    app_host = request.form.get("app-host")
    token=os.environ['TSURU_TOKEN']
    envs = {"SOMEVAR": "somevalue"} # Returns the variable to be set in the app

    # Set the TARGET to be scrapped like an env
    data={ "Envs.0.Name" : "TARGET_ENDPOINT", "Envs.0.Value" : app_host, "NoRestart" : "false" }
    headers={"Authorization" : "bearer {}".format(token)}
    r = requests.post("http://<tsuru-api-endpoint>/1.0/apps/{}/env".format(app_name), data=data, headers=headers)

    return json.dumps(envs), 201

@app.route("/resources/<name>/bind", methods=["POST", "DELETE"])
def access_control(name):
    app_host = request.form.get("app-host")
    unit_host = request.form.get("unit-host")
    # use unit-host and app-host, according to the access control tool, and
    # the request method.
    return "", 201

@app.route("/resources/<name>/status", methods=["GET"])
def status(name):
    # check the status of the instance named "name"
    return "", 204

@app.route("/resources/<name>/bind-app", methods=["DELETE"])
def unbind_app(name):
    app_host = request.form.get("app-host")
    # use name and app-host to remove the bind
    return "", 200

app.run(port=int(os.environ.get("PORT", "8888")), host="0.0.0.0")