import os
import pathlib
from config import user_agent, teamraid, profile

cron_dir = pathlib.Path(os.path.dirname(__file__))
mongo = {
    'url': 'mongodb://127.0.0.1:27017/',
    'db': 'gbf'
}
proxies = {}

headerString = """
Accept           : application/json, text/javascript, */*; q=0.01
Accept-Encoding  : gzip, deflate
Accept-Language  : zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6
Host             : game.granbluefantasy.jp
Referer          : http://game.granbluefantasy.jp/
User-Agent       : {user_agent}
X-Requested-With : XMLHttpRequest
X-VERSION        : {version}
""".format(user_agent=user_agent, version='{version}')
