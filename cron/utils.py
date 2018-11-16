import re

import requests
import requests.cookies
from config import proxies, headerString
from cookies import cookies as defaultCookies


def getXVersion():
    r = requests.get('http://game.granbluefantasy.jp/', proxies=proxies)
    regex = re.compile('Game\.version\s?=\s?"(\d+)";')
    result = regex.search(r.text)
    if result:
        return result.group(1)
    else:
        raise Exception('error searching')


def initSession():
    defaultHeaders = {line[0].strip(): line[1].strip() for line in
                      [x.split(":", 1) for x in
                       [line for line in headerString.format(version=getXVersion()).splitlines() if line]]
                      if len(line) == 2 and line[0] != 'Cookie'}
    s = requests.Session()
    s.proxies.update(proxies)
    jar = requests.cookies.RequestsCookieJar()
    for cookie in defaultCookies:
        jar.set(cookie['key'], cookie['value'], domain=cookie['host'])
    # jar.set('tasty_cookie', 'yum', domain='httpbin.org', path='/cookies')
    # jar.set('gross_cookie', 'blech', domain='httpbin.org', path='/elsewhere')
    s.cookies = jar
    # s.cookies.update(defaultCookies)
    s.headers.update(defaultHeaders)
    return s
