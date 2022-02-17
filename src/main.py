import os
import sys
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
import supervisely as sly

# order matters
load_dotenv("secret.env")
load_dotenv("debug.env")

import src.card_name
import src.card_example
import src.card_github


app = FastAPI()
sly.app.fastapi.enable_hot_reload_on_debug(app)
app.mount("/sly", sly.app.fastapi.create())
app.include_router(src.card_name.router)

api = sly.Api.from_env()

state = sly.app.StateJson()
state["activeStep"] = 1
data = sly.app.DataJson()


src.card_name.init()
src.card_github.init(api)


@app.get("/")
async def read_index(request: Request):
    templates = sly.app.fastapi.Jinja2Templates(directory="templates")
    return templates.TemplateResponse("index.html", {"request": request})


# @TODO: app, templates, api - global objects, how to avoid inits?
# @TODO: make app / templates as global object
# @TODO: widget checks widet_id key in global state / data and raises error
# @TODO: handle github token errors
# @TODO: repo visibility
# @TODO: start new vs open recent
# @TODO: sdk widfget style - import local script tag <link>
# @TODO: api object from request (to handle labelers tokens)
