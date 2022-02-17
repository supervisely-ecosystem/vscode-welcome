import os
import sys

from fastapi import FastAPI
import supervisely as sly

app = None
templates = None
api = None


def init():
    global app, templates, api

    app = FastAPI()
    app.mount("/sly", sly.app.fastapi.create())

    templates = sly.app.fastapi.Jinja2Templates(directory="templates")
    sly.app.fastapi.enable_hot_reload_on_debug(app, templates)

    api = sly.Api.from_env()


if app is None:
    init()
