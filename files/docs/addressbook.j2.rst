==============
addressbook.j2
==============

---------------------------------
Jinja2 template for address books
---------------------------------

Remember how we passed the parent object of :code:`data` into the template engine within our :code:`app.py` script? Well here we take those variables and run them through our template with Jinja2.

The resulting set commands will be passed back to Nornir as the configuration to push.

.. code-block:: python

    {% for each in addressbook %}
    set security address-book global address {{ each.name }} {{ each.prefix }}
    {% endfor %}


Since our :code:`addressbook` object is in list format (defined at the path of :code:`groups/groups.yaml`), we start our work off by looping over that list of items.
