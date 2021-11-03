======
app.py
======

---------------------------
Configure security policies
---------------------------

We will be using Nornir to configure our firewalls with their security address books and policies.

-----------------
About our example
-----------------

In this example we will be creating a new address book object and then referencing that object in a new security policy.


.. code-block:: yaml

    [edit security]
    +  address-book {
    +      global {
    +          address WAN 74.51.192.0/24;
    +      }
    +  }

    [edit security policies]
        from-zone LAN to-zone DMZ { ... }
    +    from-zone WAN to-zone DMZ {
    +        policy WAN-DMZ {
    +            match {
    +                source-address WAN;
    +                destination-address any;
    +                application any;
    +            }
    +            then {
    +                permit;
    +                log {
    +                    session-close;
    +                }
    +            }
    +        }
    +    }

We will executing our automation in a declarative manner, which is to say that we will declare how we want our firewall to be configured in a data format (YAML) and have it ran through a templating engine (Jinja2). The resulting output will be a series of `set commands` needed to provision the firewall according to our intent.

As we are working within an automation framework, we will need to provide this data in a fashion that will be understood by Nornir. Because of this, we will start here at the `app.py` file used to execute our script, but please note that we will be bouncing between the additional files when appropriate.

You may find this document, and all of its kinfolk within the `files/docs/` directory.

--------------
Code breakdown
--------------

.. code-block:: python

    import logging
    import datetime

    from nornir_pyez.plugins.tasks import pyez_config, pyez_diff, pyez_commit
    from nornir import InitNornir
    from nornir_utils.plugins.functions import print_result
    from rich import print


Importing functionality into our scripts
  - `logging` allows us to create basic log files locally
  - `datetime` enables us to speedtest our script's execution
  - `pyez_config` lets us manage the configuration on a device with PyEZ
  - `pyez_diff` will handle the config diff process
  - `pyez_commit` performs the actual configuration commit process
  - `InitNornir` is the main method of Nornir, contains all the functionality
  - `print_result` helps us see the output of our task in the terminal
  - `print` will replace the functionality of Python's default print method


.. code-block:: python

    nr = InitNornir(config_file="config.yaml")


We need to initialize the Nornir framework before we can hope to execute any of its functionality. We do this by creating a new object called `nr`, and store within it the `InitNornir()` method imported above, but not before telling it where to find our configuration file. In our example, our configuration file is named `config.yaml` and stored within the same directory as our script.

.. code-block:: python

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


We need to import some functionality into our script:
  - `asyncio` will enable our script to be executed in an async, non-io blocking manner
  - `AsyncNetconfDriver` is our primary method of interacting with Scrapli's transport system
  - `enable_basic_logging` will write simple logs to the localhost


.. code-block:: python

    # Enable logging. Create a log file in the current directory.
    enable_basic_logging(file=True, level="debug")


We want to turn on logging right out the gate, so we call the imported `enable_basic_logging` method after passing in two parameters: `file` and `level`


.. code-block:: python

    GALVESTON = {
        "host": "192.168.105.137",
        "auth_username": "scrapli",
        "auth_password": "juniper123",
        "auth_strict_key": False,
        "transport": "asyncssh"
    }

    SANANTONIO = {
        "host": "192.168.105.146",
        "auth_username": "scrapli",
        "auth_password": "juniper123",
        "auth_strict_key": False,
        "transport": "asyncssh"
    }

    DEVICES = [GALVESTON, SANANTONIO]

    CONFIG = """
    <config>
        <configuration>
            <interfaces>
                <interface>
                    <name>ge-0/0/1</name>
                    <unit>
                        <name>0</name>
                        <family>
                            <inet>
                                <address>
                                    <name>192.168.110.22/24</name>
                                </address>
                            </inet>
                        </family>
                    </unit>
                </interface>
            </interfaces>
        </configuration>
    </config>
    """


We take this opportunity to create some objects that define our parameters.
  - define two network devices, `GALVESTON` and `SANANTONIO`
  - create a new list called `DEVICES` and place these two devices in there
  - our configuration change is stored as CONFIG, written in XML


.. code-block:: python

    async def edit_configuration(device):
        conn = AsyncNetconfDriver(**device)
        await conn.open()
        result = await conn.edit_config(config=CONFIG, target="candidate")
        await conn.close()
        return result


Here we define our asynchronous function that will handle the connections to our network devices.
  - we create an object called `conn` that will store our connection parameters into the `AsyncNetconfDriver`
  - our connections are opened and we `await` for the responses
  - the configuration is pushed to our devices, with the response stored as `result`
  - connections to our devices need to be closed, so we again use the `conn` object but this time with the `close` method
  - `result` is returned to the `main` function (defined below)


.. code-block:: python

    async def main():
        coroutines = [edit_configuration(device) for device in DEVICES]
        results = await asyncio.gather(*coroutines)


The beginning of our primary function has a bit going on for itself.
  - loop over the `DEVICES` list object and run each `device` through our `edit_configuration` function
  - we store these in a list object called `coroutines`
  - asyncio executes the `gather` method and we pass in the `coroutines` object into it
  - the responses received are stored in an object called `results`


.. code-block:: python

        for each in results:
            print(each.host)
            print(each.result)


Remember that our `results` object is a list of responses from our network devices. Let's open that up and write each into a seperate file.
  - loop over the `results` object
  - print the result object back to the screen


.. code-block:: python

    if __name__ == "__main__":
        asyncio.get_event_loop().run_until_complete(main())


Here we instantiate our main function by passing it through async.io's `get_event_loop`