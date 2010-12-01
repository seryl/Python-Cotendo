Python-Cotendo
==============

References the [Cotendo API](http://help.cotendo.net/display/Manual22/APIs?undefined).

Usage
-----

    from cotendo import Cotendo
    
    c = Cotendo(username, password)
    
    # print the staging domain conf and token
    print c.dns_get_conf('mydomain', 0)
