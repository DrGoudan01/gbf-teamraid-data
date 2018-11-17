# usage

## get bookmaker data

```python
import requests
import datetime
import pytz
import pprint
timezone = pytz.timezone('Asia/Shanghai')
start_time = datetime.datetime(2018, 5, 30, 6, 0, 0, tzinfo=timezone)
end_time = datetime.datetime(2018, 5, 30, 11, 30, 0, tzinfo=timezone)
start_time = int(start_time.timestamp())
end_time = int(end_time.timestamp())
r = requests.get('https://{your_host}/api/v0.1/bookmaker?start={}&end={}'
                 .format(start_time, end_time))
pprint.pprint(r.json())
```

replace `{your_host}` with real host you are running the server.

start_time and end_time should be standard unix timestamp.

## Cron

you need to install `pypiwin32` when you try to get cookies from Chrome on windows.

`cron/rank/individual.py` is an example for fetching individual rank.

`cron/bookmaker.py` is an example for fetching bookmaker data.

## Deploy

### 请使用mobage注册的账号, 其他登录方式不保证一定可以成功抓取数据

### 请先把项目clone到本地,

首先安装python >= 3.6.5

然后进入项目文件夹(gbf-teamraid-data), 运行`pip install -r requirements.txt`, 安装完所需的python依赖.

然后安装`pywin32`(`pip install pypiwin32`, 你也可以通过那个exe安装.)

修改`cron/config.py`中的`profile`为你要使用的对应的chrome的profile, 修改`cron/vars.py`中的`teamraid`变量 , 比如2018年8月24号这次团战是 `teamraid040` 这个值会出现在古战场首页的网页链接中.

请确保使用的profile对应的账号看(skip)过了第一次点进马票的剧情, 不然会导致无法抓取马票数据.

首先运行`python cron/cookies.py`, 在这一步程序会把对应的cookies从chrome的数据库中复制出来保存在本地`cron/cookies.dump`文件, 你会看到`获取cookies成功`. 

(这是一个`requests.cookies.RequestsCookieJar`实例经过`pickle`持久化的文件.)

尝试运行`python cron/bookmaker.py` 会使用`cron/cookies.dump`做为cookies抓取数据 如果抓取成功了会尝试把抓取到的数据存入数据库.你会看到屏幕输出类似`{'north': 0, 'west': 0, 'east': 0, 'south': 0, 'time': 1542379231}`的内容.

如果cy又改了认证方式导致无法登录,你会看到`{"auth_status":"require_auth","state":"mobage-connect_5beed740437a99.44333034"}`和`未能成功抓取数据`

(如果出现了后者, 可以开个issue, 我看心情会修...)

### 然后把整个项目文件夹(gbf-teamraid-data)复制到服务器上

安装:

- python >= 3.6.5
- mongodb on default port

`pip install -r requirements.txt`, 安装完所有的依赖.

如果成功抓取到了数据, 把整个cron文件夹复制到你的服务器上, 设置一个定时任务, 定时在服务器上运行`python cron/bookmaker.py`抓取数据. 频率根据你的心情和需求. 不过马票网页应该是每20分钟更新一次. 建议设置为每小时的8 28 48进行抓取.

server文件夹不需要做修改(如果你的mongodb是运行在默认端口上), 安装好依赖后直接`python app.py`启动服务器, 默认会运行在6001端口. (当然, 也要放在服务器上)

也就是说, 项目clone到本地为的是通过`cron`提供的`cookies.py`获取到chrome提供的cookies, 以在服务器上使用.

## About data

因为我已经退坑了, 也不会再在服务器上运行这个项目. 所以如果想要数据的话请自己从cy那边爬.

## LICENSE

DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
        Version 2, December 2004

Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>

Everyone is permitted to copy and distribute verbatim or modified
copies of this license document, and changing it is allowed as long
as the name is changed.

DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

0. You just DO WHAT THE FUCK YOU WANT TO.
