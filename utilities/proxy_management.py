__author__ = 'alonsobarquero'

from configs.config import ProxyConfigs as PC


def get_proxy(netloc):
    """
    This method emulates the functionality of the socialware proxy PAC file
    function FindProxyForURL(url, host)
    {
         if (dnsDomainIs(host,".twitter.com") || host == "twitter.com")
              return "PROXY proxy.qa1.socialware.com:3130";
         if (dnsDomainIs(host,".facebook.com") || host == "facebook.com")
              return "PROXY proxy.qa1.socialware.com:3130";
         if (dnsDomainIs(host,".linkedin.com") || host == "linkedin.com")
              return "PROXY proxy.qa1.socialware.com:3130";
         if (dnsDomainIs(host,".sowatest.com") || host == "sowatest.com")
              return "PROXY proxy.qa1.socialware.com:3130";
         if (host == "proxy.qa1.socialware.com")
              return "PROXY proxy.qa1.socialware.com:3130";
         if (host == "session.socialware.com")
              return "PROXY proxy.qa1.socialware.com:3130";
         return "DIRECT";
    }
    :param netloc: url.netloc from
    :return: if netloc found in list returns PC.proxies dict Else return None
    """
    exist = map(lambda (url): url in netloc, PC.URLs)
    return PC.PROXIES if any(exist) else None
