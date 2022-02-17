import os
import sys
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
import supervisely as sly

# from supervisely.app.fastapi import Jinja2Templates

# app_repo_dir = os.getcwd()  # app root directory (working directory)
# print(f"App root repo directory: {app_repo_dir}")
# sys.path.append(app_repo_dir)
# sys.path.append(os.path.join(app_repo_dir, "src"))
# order matters
# load_dotenv(os.path.join(app_repo_dir, "secret.env"))
# load_dotenv(os.path.join(app_repo_dir, "debug.env"))


# order matters
load_dotenv("secret.env")
load_dotenv("debug.env")

app = FastAPI()
app.mount("/sly", sly.app.fastapi.create())
sly.app.fastapi.enable_hot_reload_on_debug(app)


api = sly.Api.from_env()

state = sly.app.StateJson()
state["activeStep"] = 1
data = sly.app.DataJson()

import src.card_name
import src.card_example
import src.card_github

src.card_name.init(state, app)
src.card_github.init(app, api)


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
