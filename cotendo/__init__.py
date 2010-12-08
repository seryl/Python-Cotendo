import logging
import suds

from suds.client import Client
from suds.plugin import MessagePlugin
from suds.sax.element import Element
from suds.sax.text import Text

from cotendohelper import CotendoDNS, CotendoCDN, UnescapedText
from lxml import etree

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
    def __init__(self, username, password, debug=False):
        logging.basicConfig(level=logging.INFO)
        self.client = Client('https://api.cotendo.net/cws?wsdl',
                             location = 'http://api.cotendo.net/cws?ver=1.0',
                             username=username, password=password,
                             plugins=[CotendoPlugin()])
        if debug:
            logging.getLogger('suds.client').setLevel(logging.DEBUG)
            logging.getLogger('suds.transport').setLevel(logging.DEBUG)
            logging.getLogger('suds.xsd.schema').setLevel(logging.DEBUG)
            logging.getLogger('suds.wsdl').setLevel(logging.DEBUG)

    def cdn_get_conf(self, cname, environment):
        """
        Returns the existing origin configuration and token from the CDN
        """
        response = self.client.service.cdn_get_conf(cname, environment)
        cdn_config = CotendoCDN(response)
        return cdn_config

    def cdn_publish_conf(self, cname):
        """
        Publishes a requested origin staging configuration
        """
        return self.client.service.cdn_publish_conf(cname)

    def cdn_set_conf(self, cname, originConf, environment, token):
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

    def dns_get_conf(self, domainName, environment):
        """
        Returns the existing domain configuration and token from the ADNS
        """
        response = self.client.service.dns_get_conf(domainName, environment)
        dns_config = CotendoDNS(response)
        return dns_config

    def dns_publish_conf(self, domainName):
        """
        Publishes a requested origin staging configuration
        """
        return self.client.service.dns_publish_conf(domainName)

    def dns_set_conf(self, domainName, domainConf, environment, token):
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

    def dns_set_variables(self, variables):
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

class CotendoPlugin(MessagePlugin):
    def marshalled(self, context):
        # Adjust prefixes
        context.envelope.refitPrefixes()
        context.envelope.expns = None

        context.envelope = context.envelope.setPrefix(
                'soap', 'http://schemas.xmlsoap.org/soap/envelope/')

        # Update the Envelope name
        context.envelope.rename('soap:Envelope')

        # Remove Excess header
        context.envelope.remove(context.envelope.getChildren()[0])

        # Update the Body name
        context.envelope.getChildren()[0].rename('soap:Body')

        # Add prefixes
        context.envelope.addPrefix('xsi',
                'http://www.w3.org/2001/XMLSchema-instance')
        context.envelope.addPrefix('soapenc',
                'http://schemas.xmlsoap.org/soap/encoding/')
        context.envelope.addPrefix('xsd',
                'http://www.w3.org/2001/XMLSchema')

        # Set Encoding Style
        context.envelope.set('soap:encodingStyle',
                'http://schemas.xmlsoap.org/soap/encoding/')

        body = context.envelope.getChild('Body')

        # Remove xmlns from body
        body.expns = None

        # Add param xsi types and wrap data in <![CDATA[data]]>
        method = body.getChildren()[0]
        for param in method.getChildren():
            param.set('xsi:type', 'xsd:string')
            param.text = UnescapedText('<![CDATA[' + Text(param.text) + ']]>')

class CotendoHelper(Cotendo):
    def __init__(self):
        super(CotendoHelper, self).__init__(
            username, password, debug=False)
        # DNS Helper
        self.dns = None
        # CDN Helper
        self.cdn = None

    def GrabDNS(self, domain, environment):
        self.dns = self.dns_get_conf(domain, environment)

    def UpdateDNS(self, domain, environment):
        """Pushes DNS updates"""
        self.dns_set_conf(domain, self.dns.config,
                          environment, self.dns.token)

    def Flush(self):
        """Flushes DNS updates"""
        self.dns

