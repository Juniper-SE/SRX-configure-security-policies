# Configure security policies with Nornir

[![N|Solid](https://upload.wikimedia.org/wikipedia/commons/3/31/Juniper_Networks_logo.svg)](https://junos-ansible-modules.readthedocs.io/en/stable/)

## Overview

This example will show how to configure security policies on Juniper's SRX firewalls with Nornir

In addition to the Python script, this project also ships with additional tools to help you along your way. You will find a Dockerfile for running the project in an isolated environment, and an Invoke `tasks.py` file for those of us that hate typing out everything all the time.

## ⚙️ `How it works`

Configuration parameters are stored as YAML, then ran through a Jinja2 template to produce the device's configuration. The is then pushed to the device using the NETCONF API on board.

Let's take a second to review the documentation in the `files/docs/` directory.

Name | Description
---- | -----------
[app.py](files/docs/app.py.rst) | Configure the security policies on our firewalls with `nornir`

## 📝 `Dependencies`

Refer to the Poetry Lock file located at [poetry.lock](poetry.lock) for detailed descriptions on each package installed.

## 🚀 `Executing the script`

This project provides two unique methods of executing the playbook:

[Executing with Docker](files/docs/execute_with_docker.rst) | Execute with Docker

[Executing with Python](files/docs/execute_with_python.rst) | Execute with Python
