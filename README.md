Python-Cotendo
==============

References the [Cotendo API](http://help.cotendo.net/display/Manual22/APIs?undefined).

## Overview

    from cotendo import CotendoHelper

    c = CotendoHelper(username, password)
    c.GrabDNS('mysite.com', 1)
    print c.dns.conf

## Lighter API

    from cotendo import Cotendo
    
    c = Cotendo(username, password)
    
    # print the staging domain conf and token
    print c.dns_get_conf('mydomain.com', 0)


