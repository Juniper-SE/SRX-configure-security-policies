import logging
import datetime

from nornir_pyez.plugins.tasks import pyez_config, pyez_diff, pyez_commit
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from rich import print

nr = InitNornir(config_file="config.yaml")

def configure_addressbook(task):

    # pass in variables from inventory file
    data = {}
    data['addressbook'] = task.host['addressbook']
    print(data)

    # execute our task by templating our variables through a Jinja2 template to produce config
    response = task.run(
        task=pyez_config,
        severity_level=logging.DEBUG,
        template_path='templates/addressbook.j2',
        template_vars=data,
        data_format='set'
    )
    if response:
        diff = task.run(pyez_diff)
        print_result(diff)
    if diff:
        commit = task.run(task=pyez_commit)
        print_result(commit)


def configure_policies(task):

    # pass in variables from inventory file
    data = {}
    data['secpolicies'] = task.host['secpolicies']
    print(data)

    # execute our task by templating our variables through a Jinja2 template to produce config
    # push and commit
    response = task.run(
        task=pyez_config,
        severity_level=logging.DEBUG,
        template_path='templates/policies.j2',
        template_vars=data,
        data_format='set'
    )
    if response:
        diff = task.run(pyez_diff)
        print_result(diff)
    if diff:
        commit = task.run(task=pyez_commit)
        print_result(commit)


if __name__ == "__main__":
    start_time = datetime.datetime.now()

    # create our address-book entry
    print(f'Configuring our address book now')
    response = nr.run(task=configure_addressbook)
    print_result(response)

    print(f'Configuring our security policies now')
    # create our security policies
    response = nr.run(task=configure_policies)
    print_result(response)

    # print time delta to screen
    print(f"Nornir took: {datetime.datetime.now() - start_time} seconds to execute")
