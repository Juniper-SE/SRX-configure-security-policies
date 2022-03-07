"""Configure SRX security objects with Nornir.
(c) 2022 Calvin Remsburg <cremsburg.dev@gmail.com>
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
  http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import logging
import datetime

from nornir_pyez.plugins.tasks import pyez_config, pyez_diff, pyez_commit
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from rich import print as richprint

nr = InitNornir(config_file="config.yaml")


def configure_addressbook(task):
    """Configure our Address Book objects."""

    # #######################################################################
    # Create a new empty dictionary, then pass in our `addressbook` object
    #   found within the inventory file
    # Print our resulting object to the screen.
    # #######################################################################
    data = {}
    data["addressbook"] = task.host["addressbook"]
    richprint(data)

    # #######################################################################
    # Execute our task by passing our variables through a Jinja2 template.
    # The output of our templating will be a configuration in set CLI format.
    # Results from our task will be stored in an object named `address_book`.
    # #######################################################################
    address_book = task.run(
        task=pyez_config,
        severity_level=logging.DEBUG,
        template_path="templates/addressbook.j2",
        template_vars=data,
        data_format="set",
    )

    # #######################################################################
    # If the result is truthy, we'll perform a diff operation and print.
    # We will commit the configuration only if a diff exists.
    # #######################################################################
    if address_book:
        diff = task.run(pyez_diff)
        print_result(diff)
    if diff:
        commit = task.run(task=pyez_commit)
        print_result(commit)


def configure_policies(task):
    """Configure our Security Policies."""

    # #######################################################################
    # Create a new empty dictionary, then pass in our `security_policies`
    #  object found within the inventory file
    # Print our resulting object to the screen.
    # #######################################################################
    data = {}
    data["security_policies"] = task.host["security_policies"]
    richprint(data)

    # #######################################################################
    # Execute our task by passing our variables through a Jinja2 template.
    # The output of our templating will be a configuration in set CLI format.
    # Results from our task will be stored in an object named `sec_policies`.
    # #######################################################################
    sec_policies = task.run(
        task=pyez_config,
        severity_level=logging.DEBUG,
        template_path="templates/policies.j2",
        template_vars=data,
        data_format="set",
    )

    # #######################################################################
    # If the result is truthy, we'll perform a diff operation and print.
    # We will commit the configuration only if a diff exists.
    # #######################################################################
    if sec_policies:
        diff = task.run(pyez_diff)
        print_result(diff)
    if diff:
        commit = task.run(task=pyez_commit)
        print_result(commit)


def configure_interfaces(task):
    """Configure our interfaces."""

    # #######################################################################
    # Create a new empty dictionary, then pass in our `security_zones` object
    #   found within the inventory file
    # Print our resulting object to the screen.
    # #######################################################################
    data = {}
    data["interfaces"] = task.host["interfaces"]
    richprint(data)

    # #######################################################################
    # Execute our task by passing our variables through a Jinja2 template.
    # The output of our templating will be a configuration in set CLI format.
    # Results from our task will be stored in an object named `interfaces`.
    # #######################################################################
    interfaces = task.run(
        task=pyez_config,
        severity_level=logging.DEBUG,
        template_path="templates/interfaces.j2",
        template_vars=data,
        data_format="set",
    )

    # #######################################################################
    # If the result is truthy, we'll perform a diff operation and print.
    # We will commit the configuration only if a diff exists.
    # #######################################################################
    if interfaces:
        diff = task.run(pyez_diff)
        print_result(diff)
    if diff:
        commit = task.run(task=pyez_commit)
        print_result(commit)


def configure_security_zones(task):
    """Configure our Security Zones."""

    # #######################################################################
    # Create a new empty dictionary, then pass in our `security_zones` object
    #   found within the inventory file
    # Print our resulting object to the screen.
    # #######################################################################
    data = {}
    data["security_zones"] = task.host["security_zones"]
    richprint(data)

    # #######################################################################
    # Execute our task by passing our variables through a Jinja2 template.
    # The output of our templating will be a configuration in set CLI format.
    # Results from our task will be stored in an object named `sec_policies`.
    # #######################################################################
    security_zones = task.run(
        task=pyez_config,
        severity_level=logging.DEBUG,
        template_path="templates/security_zones.j2",
        template_vars=data,
        data_format="set",
    )

    # #######################################################################
    # If the result is truthy, we'll perform a diff operation and print.
    # We will commit the configuration only if a diff exists.
    # #######################################################################
    if security_zones:
        diff = task.run(pyez_diff)
        print_result(diff)
    if diff:
        commit = task.run(task=pyez_commit)
        print_result(commit)


if __name__ == "__main__":
    # #######################################################################
    # Create a snapshot of our time. This will be used later to derive
    #   information on how long the task took to complete.
    # #######################################################################
    start_time = datetime.datetime.now()

    # #######################################################################
    # Pass in our tasks into Nornir.
    #   - `configure_interfaces`
    #   - `configure_addressbook`
    #   - `configure_policies`
    #   - `configure_security_zones`
    # Print the result to the console.
    # #######################################################################
    print("Configuring our interfaces now.")
    response = nr.run(task=configure_interfaces)
    print_result(response)

    print("Configuring our security zones now.")
    response = nr.run(task=configure_security_zones)
    print_result(response)

    print("Configuring our address book now.")
    response = nr.run(task=configure_addressbook)
    print_result(response)

    print("Configuring our security policies now.")
    response = nr.run(task=configure_policies)
    print_result(response)

    # #######################################################################
    # Subtract the current time from our `start_time` object and print
    #   the information to the screen.
    # #######################################################################
    print(f"Task executed in {datetime.datetime.now() - start_time} seconds.")
