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
[addressbook.j2](files/docs/addressbook.j2.rst) | Jinja2 template for address books
[app.py](files/docs/app.py.rst) | Execute our script with `nornir`
[config.yaml](files/docs/config.yaml.rst) | Nornir's configuration file
[defaults.yaml](files/docs/defaults.yaml.rst) | Nornir's default variables file
[groups.yaml](files/docs/groups.yaml.rst) | Where we store our goodies
[inventory.yaml](files/docs/inventory.yaml.rst) | Our inventory file
[nornir.log](files/docs/nornir.log.rst) | Nornir's logging file
[policies.j2](files/docs/policies.j2.rst) | Jinja2 template for security policies

## 📝 `Dependencies`

Refer to the Poetry Lock file located at [poetry.lock](poetry.lock) for detailed descriptions on each package installed.

## 🚀 `Executing the script`

This project provides two unique methods of executing the playbook:

Name | Description
---- | -----------
[Docker](files/docs/execute_with_docker.rst) | Executing with Docker
[Python](files/docs/execute_with_python.rst) | Executing with Python
