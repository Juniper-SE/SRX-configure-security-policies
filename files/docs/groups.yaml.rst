===========
groups.yaml
===========

--------------------------
Where we store our goodies
--------------------------

Here is our location for variables to be used within our script. 


.. code-block:: yaml

    ---
    junos:
      username: 'nornir'
      password: 'juniper123'
      platform: junos


Starting off simple, this block of objects will tell Nornir to use the username of :code:`nornir` and password of :code:`juniper123` when connecting to our device. Additionally, we tell Nornir to expect our device to be running JunOS.

.. code-block:: yaml

      data:
        security_policies:

          # LAN to WAN security policy
          # permits all traffic
          - src: 'LAN'
            dst: 'WAN'
            name: 'LAN-WAN'
            match:
              source_address: 'any'
              destination_address: 'any'
              application: 'any'
              dynamic_application: 'any'
            then:
              action: 'permit'
              log: 'session-close'

          # LAN to DMZ security policy
          # permits all traffic
          - src: 'LAN'
            dst: 'DMZ'
            name: 'LAN-DMZ'
            match:
              source_address: 'any'
              destination_address: 'any'
              application: 'any'
              dynamic_application: 'any'
            then:
              action: 'permit'
              log: 'session-close'

          # WAN to DMZ security policy
          # permits all traffic sourced from 74.51.192.0/24
          - src: 'WAN'
            dst: 'DMZ'
            name: 'WAN-DMZ'
            match:
              source_address: 'WAN'
              destination_address: 'any'
              application: 'any'
            then:
              action: 'permit'
              log: 'session-close'

        addressbook:

          # WAN subnet
          - name: 'WAN'
            prefix: '74.51.192.0/24'


This is where we create our configuration variables; please note that the top-level object's name is :code:`data`, we will reference this object in our task's exection.

We first define our security policies under :code:`security_policies`, a list of policies asking the traditional policy information to be ran through :code:`templates/policies.j2`

Finally, we create an address book list as :code:`addressbook`, which will be ran through :code:`templates/addressbook.j2`