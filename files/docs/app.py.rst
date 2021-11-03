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

We will executing our automation in a declarative manner, which is to say that we will declare how we want our firewall to be configured in a data format (YAML) and have it ran through a templating engine (Jinja2). The resulting output will be a series of :code:`set commands` needed to provision the firewall according to our intent.

As we are working within an automation framework, we will need to provide this data in a fashion that will be understood by Nornir. Because of this, we will start here at the :code:`app.py` file used to execute our script, but please note that we will be bouncing between the additional files when appropriate.

You may find this document, and all of its kinfolk within the :code:`files/docs/` directory.

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
  - :code:`logging` allows us to create basic log files locally
  - :code:`datetime` enables us to speedtest our script's execution
  - :code:`pyez_config` lets us manage the configuration on a device with PyEZ
  - :code:`pyez_diff` will handle the config diff process
  - :code:`pyez_commit` performs the actual configuration commit process
  - :code:`InitNornir` is the main method of Nornir, contains all the functionality
  - :code:`print_result` helps us see the output of our task in the terminal
  - :code:`print` will replace the functionality of Python's default print method


.. code-block:: python

    nr = InitNornir(config_file="config.yaml")


We need to initialize the Nornir framework before we can hope to execute any of its functionality.

We accomplish this by creating a new object called :code:`nr`, and store within it the :code:`InitNornir()` method imported above, but not before telling it where to find our configuration file.

In our example, our configuration file is named :code:`config.yaml` and stored within the same directory as our script.


.. code-block:: python

    def configure_addressbook(task):

        data = {}
        data['addressbook'] = task.host['addressbook']
        print(data)

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


We will create a function dedicated to the address book configuration; our :code:`main()` function will be calling upon this function later on in the script.

Our fuction is declared with a :code:`task` parameter passed into it, this will be provided by the :code:`nr.run()` method. You can think of this :code:`task` as being related to a unique device within our inventory, it provides access to the device's information and the variables assigned to it.

We want to make the device's variables a bit easier to access, so we create a new empty object called :code:`data`, and then stuff our :code:`addressbook` object into it. This :code:`addressbook` object was declared in our :code:`groups.yaml` file, but could have been derived from our :code:`inventory.yaml` or :code:`hosts.yaml` file.

The object is then printed to the screen for everyone to see what we are about to pass into our templating engine.

We execute our task by calling :code:`task.run()` method, passing in a few sets of information. The response from the task is stored in an object called :code:`response`, which will be used in just a moment.

The data passed into our :code:`task.run()` method requires attention:
  - :code:`task=pyez_config` tells Nornir we want to use the functionality of our imported method :code:`pyez_config`
  - :code:`severity_level=logging.DEBUG` sets the appropriate level of logging 
  - :code:`template_path='templates/addressbook.j2'` points to the path of our :code:`addressbook.j2` template file
  - :code:`template_vars=data` is how we declare which object to pass into the template file
  - :code:`data_format='set'` enables us to tell PyEZ which format to expect from our output configuration file

Finally, we want the function to check if there was response from the device, and if so, check to see if there was a configuration diff; the diff is then printed to the screen after being stored to a new object called :code:`diff`.

When :code:`diff` is discovered as :code:`True`, a configuration commit is performed by :code:`pyez_commit`. The output is stored in a new object called :code:`commit` and then printed to the screen with Nornir's :code:`print_result` method.


.. code-block:: python

    def configure_policies(task):


Quite literally the same exact function as our :code:`configure_addressbook`, but passing a different template file into Jinja2. This isn't ideal, but hopefully it explains the different steps used to acheive our configuration state.


.. code-block:: python

    if __name__ == "__main__":
        start_time = datetime.datetime.now()

        print(f'Configuring our address book now')
        response = nr.run(task=configure_addressbook)
        print_result(response)

        response = nr.run(task=configure_policies)
        print_result(response)

        print(f"Nornir took: {datetime.datetime.now() - start_time} seconds to execute")


Our script's main function.

We start off by creating a snapshot of time with :code:`start_time = datetime.datetime.now()`; this object will be used later when we perform the same task at the end and subtract the two from each other.

Tell the user that we are beginning the address book configuration, then run our :code:`configure_addressbook` function within Nornir's :code:`nr.run()` method. The output will be stored in a new object called :code:`response`, which will then be printed to the screen with :code:`print_result(response)`

Perform the same task for our security policies, this time calling :code:`configure_policies` instead.
