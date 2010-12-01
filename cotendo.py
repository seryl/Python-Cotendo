from suds.client import Client

class Cotendo(object):
    """
    Variable information:

    * cname
        The CNAME of the origin

    * domainName
        Name of the domain

    * domainConf
        [Domain XML Configuration](http://help.cotendo.net/display/Manual22/ADNS+XML+Reference+Guide?undefined)

    * environment
        Staging or Production configuration. (0 for staging, 1 for production)

    * expressions
        The expression can contain multiple flush jobs.
        The delimiter is by a new line.

    * originConf
        [Origin XML Configuration](http://help.cotendo.net/display/Manual22/CDN+XML+Reference+Guide?undefined)

    * token
        Last origin configuration token.
        (Call cdn_get_conf to retrieve the latest token)

    * type
        Flush type is either 'hard' or 'soft'

    * variables
        Container for the variable tags

        Ex:

            <variables>
               <variable name="ny_weight" value="10"/>
            </variables>

    * variable tag
        Ex:

            <variable name="ny_weight" value="10"/>

    """
    def __init__(self, username, password):
        self.client = Client('https://api.cotendo.net/cws?wsdl',
                             username=username, password=password)

    def cdn_get_conf(cname, environment):
        """
        Returns the existing origin configuration and token from the CDN
        """
        return self.client.service.cdn_get_conf(cname, environment)

    def cdn_publish_conf(cname):
        """
        Publishes a requested origin staging configuration
        """
        return self.client.service.cdn_publish_conf(cname)

    def cdn_set_conf(cname, originConf, environment, token):
        """
        The cdn_set_conf method enables the user to update an existing
        origin configuration in the CDN.

        The cdn_get_conf returns the token in the response and the
        cdn_set_conf requires a token as one of the parameters.

        The set action is valid only if the token returned is equal to
        the token representing the current version of the configuration file.
        """
        return self.client.service.cdn_set_conf(
            cname, originConf, environment, token)

    def dns_get_conf(domainName, environment):
        """
        Returns the existing domain configuration and token from the ADNS
        """
        return self.client.service.dns_get_conf(domainName, environment)

    def dns_publish_conf(domainName):
        """
        Publishes a requested origin staging configuration
        """
        return self.client.service.dns_publish_conf(domainName)

    def dns_set_conf(domainName, domainConf, environment, token):
        """
        The cdn_set_conf method enables the user to update an existing
        origin configuration in the CDN.

        The cdn_get_conf returns the token in the response and the
        cdn_set_conf requires a token as one of the parameters.

        The set action is valid only if the token returned is equal to
        the token representing the current version of the configuration file.
        """
        return self.client.service.dns_set_conf(
            domainName, domainConf, environment, token)

    def dns_set_variables(variables):
        """
        This API sets one or more variable values in the DNS configuration.
        """
        return self.client.service.dns_set_variables(variables)

    def doFlush(self, cname, flushExpression, flushType):
        """
        doFlush method enables specific content to be "flushed" from the
        cache servers.

        * Note: The flush API is limited to 1,000 flush invocations per hour
        (each flush invocation may include several objects). *
        """
        return self.client.service.doFlush(
            cname, flushExpression, flushType)
