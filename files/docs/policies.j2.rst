===========
policies.j2
===========

-------------------------------------
Jinja2 template for security policies
-------------------------------------

Remember how we passed the parent object of :code:`data` into the template engine within our :code:`app.py` script? Well here we take those variables and run them through our template with Jinja2.

The resulting set commands will be passed back to Nornir as the configuration to push.

.. code-block:: python

    {% for each in security_policies %}


Since our :code:`security_policies` object is in list format (defined at the path of :code:`groups/groups.yaml`), we start our work off by looping over that list of items.


.. code-block:: python

    set security policies from-zone {{ each.src }} to-zone {{ each.dst }} policy {{ each.name }} match source-address {{ each.match.source_address }}
    set security policies from-zone {{ each.src }} to-zone {{ each.dst }} policy {{ each.name }} match destination-address {{ each.match.destination_address }}
    set security policies from-zone {{ each.src }} to-zone {{ each.dst }} policy {{ each.name }} match application {{ each.match.application }}
    {% if each.match.dynamic_application is defined %}
    set security policies from-zone {{ each.src }} to-zone {{ each.dst }} policy {{ each.name }} match dynamic-application {{ each.match.dynamic_application }}
    {% endif %}


Create the 'match' statements for our policy.


.. code-block:: python

    set security policies from-zone {{ each.src }} to-zone {{ each.dst }} policy {{ each.name }} then {{ each.then.action }}
    {% if each.then.log is defined %}
    set security policies from-zone {{ each.src }} to-zone {{ each.dst }} policy {{ each.name }} then log {{ each.then.log }}
    {% endif %}


Create the 'then' statements for our policy.


.. code-block:: python

    {% endfor %}


A good scout always closes their for loop in jinja2