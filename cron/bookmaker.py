import time
import urllib.parse
# import win32crypt
import json
import datetime

from bs4 import BeautifulSoup

from mongo import bookmaker
from utils import initSession
from vars import cron_dir, teamraid
import pickle
import pymongo


def main():
    s = initSession()
    r = s.get('http://game.granbluefantasy.jp/{}/bookmaker/content/top'.format(teamraid))
    # print(s.cookies))
    # for key, value in s.cookies.items():
    # print(key, value)
    # with open(str(cron_dir / 'cookie.json'), 'w+', encoding='utf8') as f:
    # json.dump({o.name: o.value for o in s.cookies}, f)
    try:
        res = r.json()

        soup = BeautifulSoup(urllib.parse.unquote(res['data']), 'html.parser')
        data = {
            'north': int(soup.find('div', class_='lis-area area1').div.decode_contents().replace(',', '')),
            'west': int(soup.find('div', class_='lis-area area2').div.decode_contents().replace(',', '')),
            'east': int(soup.find('div', class_='lis-area area3').div.decode_contents().replace(',', '')),
            'south': int(soup.find('div', class_='lis-area area4').div.decode_contents().replace(',', '')),
            'time': int(time.time())
        }

        print('成功抓取到数据', data)
        result = bookmaker.insert_one(data)
        print('成功保存数据')
    except pymongo.errors.ConnectionFailure:
        print('成功获取到数据, 但是无法保存')
    except:
        print(r.text)
        print('未能成功保存数据, 请检查输出')


if __name__ == '__main__':
    main()
    print('======{}======'.format(datetime.datetime.now()))
