===========
config.yaml
===========

---------------------------
Nornir's configuration file
---------------------------

This file will allow us to alter the default behavior of Nornir.


.. code-block:: yaml

    ---
    inventory:
        plugin: YAMLInventory
        options:
            host_file: 'inventory/hosts.yaml'
            group_file: 'groups/groups.yaml'
            defaults_file: 'defaults/defaults.yaml'


We first define how Nornir should look for our inventory. Well state that the :code:`YAMLInventory` plugin should be used, and to look for files at the paths listed above.


.. code-block:: yaml
    runner:
        plugin: threaded
        options:
            num_workers: 40


To help with performance, Nornir leverages Threads to execute its tasks. Here we state how many workers can execute in parallel.
