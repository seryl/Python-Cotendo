Python-Cotendo
==============

References the [Cotendo API](http://help.cotendo.net/display/Manual22/APIs?undefined).

## Overview

    from cotendo import CotendoHelper

    username = 'bob'
    password = 'passlolz'

    c = CotendoHelper(username, password)

    # Grab the production mysite.com config
    c.dns.GrabDNS('mysite.com', 1)
    ...

### Pretty print the config

    ...
    # Note this sorts the config, it's a relatively slow operation
    print c.ExportDNS()

## Updating and modifying the config

You could always create your own xml parts and import them yourself, but there's a helper function provided to make that a little easier.

### Creating a record

    ...
    results = [{'ip': '10.1.2.3', 'ttl': 1800},
        {'ip': '10.1.2.4', 'ttl': 1800}]
    record = c.dns.CreateRecord('a', 'myserver', results)

### Add a record to the configuration

    ...
    # Note that this adds or updates a current record
    c.dns.add_record(record)

### Delete a record from the configuration

    ...
    c.dns.del_record('a', 'myserver')

### Import a config into the Cotendo Helper

    ...
    c.dns.ImportDNS(config, token)

### Update the DNS config on Cotendo's side

    ...
    # This takes the config from the CotendoHelper.dns.config
    c.dns.UpdateDNS('mysite.com', 1)

### Publish the configuration

    ...
    c.dns_publish_conf('mysite.com')

### printing a cli readable version of the config

    ...
    c.dns.show()

## Lighter API

    from cotendo import Cotendo

    # Note: you can pass true as a third parameter to enable debug
    c = Cotendo(username, password)

    # get the staging domain conf and token
    token, config = c.dns_get_conf('mysite.com', 0)

    # publish the config to production
    c.dns_set_conf('mysite.com', config, 1, token)

    # publish it!
    c.dns_publish_conf('mysite.com')
