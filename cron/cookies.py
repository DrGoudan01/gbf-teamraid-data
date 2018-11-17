import os
import json
import pathlib
import config
from typing import List, Dict
from vars import cron_dir
import pickle


def loadCookies():
    with open(str(cron_dir / 'cookies.dump'), 'rb') as f:
        cookies = pickle.load(f)  # type: Dict[str,str]
    return cookies


def get_chrome_cookies(url, profile: str = 'Default'):
    import os
    import sqlite3
    import win32crypt

    cookie_file_path = os.path.join(os.environ['LOCALAPPDATA'], r'Google\Chrome\User Data\{}\Cookies'.format(profile))
    conn = sqlite3.connect(cookie_file_path)
    ret_dict = {}
    rows = list(conn.execute("select name, encrypted_value from cookies where host_key = '{}'".format(url)))
    conn.close()
    for row in rows:
        ret = win32crypt.CryptUnprotectData(row[1], None, None, None, 0)
        ret_dict[row[0]] = ret[1].decode()
    return ret_dict


try:
    cookies = loadCookies()
except FileNotFoundError:
    import requests.cookies

    try:
        c = requests.cookies.RequestsCookieJar()
        for host in ['game.granbluefantasy.jp', '.game.granbluefantasy.jp']:
            cookies = get_chrome_cookies(host, profile=config.profile)
            for key, value in cookies.items():
                c.set(key, value, domain=host)
                # c.append({'key': key, 'value': value, 'host': host})
        with open(str(cron_dir / 'cookies.dump'), 'wb+') as f:
            pickle.dump(c, f)
        print('获取cookies成功')
    except ImportError:
        raise Exception('no cookies given')
