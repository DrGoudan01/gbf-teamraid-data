import datetime
import aiohttp.web
import aiohttp_jinja2
import pytz
from aiohttp import web
from db import mongo
from utils import check_and_covert_input, MissingInputException


@aiohttp_jinja2.template('crew/bookmaker/chart.html')
async def bookmakerTodayHanle(request: aiohttp.web.Request, ):
    # today = datetime.datetime.today()
    start = datetime.datetime(2018, 5, 30, tzinfo=pytz.timezone('Asia/Shanghai'))
    end = start + datetime.timedelta(hours=24)
    url = '/api/v0.1/bookmaker?start={start}&end={end}' \
        .format(start=int(start.timestamp()), end=int(end.timestamp()))
    return {'url': url}


@aiohttp_jinja2.template('crew/result.html')
async def teamRaidCrewHandle(request: aiohttp.web.Request, ):
    name = request.query.get('name', None)
    _id = request.query.get('id', None)
    teamraid = request.match_info.get('teamraid', None)
    if teamraid not in ['teamraid038', 'teamraid039']:
        raise web.HTTPNotFound(reason='古战id错误')
    if teamraid == 'teamraid039':
        raise web.HTTPNotFound(reason='尚未录入数据')
    if name or _id:
        con = {}
        if name:
            con['name'] = name
        elif _id:
            con['id'] = _id
        r = await request.app.mongo.gbf.get_collection(teamraid).find_one(con, {'_id': 0})
        if not r:
            raise web.HTTPNotFound(reason='暂无相应数据')
    else:
        r = None
    return {'r': r, 'teamraid': teamraid}


@aiohttp_jinja2.template('crew/individual.html')
async def teamRaidIndividualHandle(request: aiohttp.web.Request, ):
    try:
        teamraid = check_and_covert_input(request, {'name'    : 'teamraid',
                                                    'type'    : str,
                                                    'required': True}, 'match_info')['teamraid']

    except MissingInputException as e:
        return web.json_response({
            'status' : 'error',
            'message': str(e),
        }, status=400)

    except ValueError as e:
        return web.json_response({
            'status' : 'error',
            'message': str(e),
        }, status=400)

    if teamraid not in ['teamraid038', 'teamraid039']:
        raise web.HTTPNotFound(reason='古战id错误')
    if teamraid == 'teamraid039':
        raise web.HTTPNotFound(reason='尚未录入数据')

    return {'user_id': request.query.get('user_id', None), 'teamraid': teamraid}


routes = [
    web.get('/render/bookmaker/today', bookmakerTodayHanle),
    web.get('/render/{teamraid}/crew', teamRaidCrewHandle),
    web.get('/render/{teamraid}/individual', teamRaidIndividualHandle),
]
