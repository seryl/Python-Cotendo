from lxml import etree

# DNS Results
class DNSResult(object):
    """Abstract skeleton for every DNS result"""
    def __init__(self, ttl=1800):
        self._etree = etree.Element("result")
        self.ttl = ttl
        self._result_type = 'dns'

    def _get_ttl(self):
        return self._etree.get("ttl")

    def _set_ttl(self, ttl):
        return self._etree.set("ttl", str(ttl))

    ttl = property(_get_ttl, _set_ttl)

class DomainResult(DNSResult):
    """Abstract skeleton for CNAME and MX records"""
    def __init__(self, domain='', ttl=1800):
        super(DomainResult, self).__init__(ttl)
        self.domain = str(domain)
        self._result_type = 'domain'

    def _get_domain(self):
        return self._etree.get("domain_name")

    def _set_domain(self, domain):
        return self._etree.set("domain_name", domain)

    domain = property(_get_domain, _set_domain)

class AResult(DNSResult):
    """A record entry"""
    def __init__(self, ip='', ttl=10800):
        super(AResult, self).__init__(ttl)
        self.ip = ip
        self._result_type = 'a'

    def _get_ip(self):
        return self._etree.get("ip")

    def _set_ip(self, ip):
        return self._etree.set("ip", str(ip))

    ip = property(_get_ip, _set_ip)

class CNAMEResult(DomainResult):
    """CNAME record entry"""
    def __init__(self, domain='', ttl=1800):
        super(CNAMEResult, self).__init__(domain, ttl)
        self._result_type = 'cname'

class MXResult(DomainResult):
    """MX record entry"""
    def __init__(self, domain='', preference=20, ttl=1800):
        super(MXResult, self).__init__(domain, ttl)
        self.preference = preference
        self._result_type = 'mx'

    def _get_preference(self):
        return self._etree.get("preference")

    def _set_preference(self, preference):
        return self._etree.set("preference", str(preference))

    preference = property(_get_preference, _set_preference)

class PTRResult(DomainResult):
    """PTR record entry"""
    def __init__(self, domain='', ttl=1800):
        super(PTRResult, self).__init__(domain, ttl)
        self._result_type = 'ptr'

class TXTResult(DNSResult):
    def __init__(self, text="", ttl=1800):
        super(TXTResult, self).__init__(ttl)
        self._result_type = 'txt'

    def _get_text(self):
        return self._etree.get("text")

    def _set_text(self, text):
        return self._etree.set("text", text)

    text = property(_get_text, _set_text)

# DNS Records
class DNSRecord(object):
    """Abstract DNS Record"""
    def __init__(self, record=None):
        self.results = []
        self._etree = None
        self._record_type = 'dns'

    def _get_host(self):
        return self._etree.get("host")

    def _set_host(self, host):
        return self._etree.set("host", host)

    def _init_records(self, record=None, result_type=None, params=()):
        if record is not None:
            self.host = record.get("host")
            for r in record.getchildren():
                result = self._append_results(result_type, r, params)
                self._etree.append(result._etree)
                self.results.append(result)
        else:
            self.host = ""

    def _append_results(self, func_ptr, result, params):
        kwargs = {}
        for key in params:
            if key == 'domain':
                kwargs[key] = result.get('domain_name')
            else:
                kwargs[key] = result.get(key)

        return func_ptr(**kwargs)

    host = property(_get_host, _set_host)

class SOARecord(DNSRecord):
    """This always returns the default cotendo SOA Record"""
    def __init__(self, record=None):
        self._etree = etree.Element("soa")
        self._etree.append(
            etree.Element("reference", domain_name="cotdns.net."))
        self._record_type = 'soa'

class NSRecord(DNSRecord):
    """This always returns the default cotendo NS Record"""
    def __init__(self, record=None):
        self._etree = etree.Element("ns", host="")
        self._etree.append(
            etree.Element("reference", domain_name="cotdns.net."))
        self._record_type = 'ns'

class ARecord(DNSRecord):
    """A record listing"""
    def __init__(self, record=None):
        super(ARecord, self).__init__()
        self._etree = etree.Element("a")
        self._init_records(record, AResult, ("ip", "ttl"))
        self._record_type = 'a'

class CNAMERecord(DNSRecord):
    """CNAME record listing"""
    def __init__(self, record=None):
        super(CNAMERecord, self).__init__()
        self._etree = etree.Element("cname")
        self._init_records(
            record, CNAMEResult, ("domain", "ttl"))
        self._record_type = 'cname'

class MXRecord(DNSRecord):
    """MX record listing"""
    def __init__(self, record=None):
        super(MXRecord, self).__init__()
        self._etree = etree.Element("mx")
        self._init_records(
            record, MXResult, ("domain", "preference", "ttl"))
        self._record_type = 'mx'

class TXTRecord(DNSRecord):
    """TXT record listing"""
    def __init__(self, record=None):
        super(TXTRecord, self).__init__()
        self._etree = etree.Element("txt")
        self._init_records(
            record, TXTResult, ("text", "ttl"))
        self._record_type = 'txt'

class PTRRecord(DNSRecord):
    """PTR record listing"""
    def __init__(self, record=None):
        super(PTRRecord, self).__init__()
        self._etree = etree.Element("ptr")
        self._init_records(
            record, PTRResult, ("domain", "ttl"))
        self._record_type = 'ptr'

# CDN Records
class CDNRecord(object):
    def __init__(self):
        pass
