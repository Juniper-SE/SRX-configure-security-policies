==========
hosts.yaml
==========

------------------
Our inventory file
------------------

We will be using a static inventory file for our work, but it is highly encouraged that you consider one of Nornir's NSOT plugins for dynamic inventory.


.. code-block:: yaml

    ---
    Lafayette:
      hostname: 192.168.105.136
      groups:
        - junos

    Houston:
      hostname: 192.168.105.121
      groups:
        - junos


We define each firewall with its familiar name as the parent object. Nested within the name :code:`hostname`, where we are bypassing DNS by typing in the static IP address.

Finally, we associate the device to a group named :code:`junos`, which will be found at :code:`groups/groups.yaml`