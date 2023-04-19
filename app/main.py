import json
import logging
import os
import sys

import config as cfg

from aiohttp import web
from aiohttp.abc import BaseRequest
from aiohttp.web_request import FileField
from multidict import MultiDictProxy
from aiofile import async_open


logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
logging.StreamHandler(sys.stdout)


async def handle(request: BaseRequest):
    response_obj = {'status': 'success'}
    return web.Response(headers=cfg.headers,
                        text=json.dumps(response_obj), status=200)


async def upload_image(request: BaseRequest):
    try:
        form_data: MultiDictProxy = await request.post()
        file_field: FileField = form_data.get("file")
        filename: str = file_field.filename
        async with async_open(filename, "wb") as file:
            await file.write(file_field.file.read())
        os.rename(f"{filename}", f"./storage/{filename}")
        response = {"success": True, "url": f"{cfg.API_URL_FILES}/{filename.replace(' ', '%20')}"}
        return web.Response(headers=cfg.headers,
                            text=json.dumps(response),
                            status=200)
    except Exception as e:
        response_obj = {'success': False, 'message': str(e)}
        return web.Response(headers={'Content-type': 'application/json; charset=UTF-8'},
                            text=json.dumps(response_obj),
                            status=200)


app = web.Application()
app.router.add_get('/', handle)
app.router.add_post('/uploadPicture', upload_image)

web.run_app(app, port=cfg.API_PORT)
