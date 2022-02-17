import os
import sys
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
import supervisely as sly


app_repo_dir = os.getcwd()  # app root directory (working directory)
print(f"App root repo directory: {app_repo_dir}")
sys.path.append(app_repo_dir)
sys.path.append(os.path.join(app_repo_dir, "src"))
# order matters
load_dotenv(os.path.join(app_repo_dir, "secret.env"))
load_dotenv(os.path.join(app_repo_dir, "debug.env"))

app = FastAPI()
app.mount("/sly", sly.app.fastapi.create())

templates = sly.app.fastapi.Jinja2Templates(directory="templates")
sly.app.fastapi.enable_hot_reload_on_debug(app, templates)
api = sly.Api.from_env()

state = sly.app.StateJson()
state["activeStep"] = 1
data = sly.app.DataJson()

import card_name
import card_example
import card_github

card_name.init(state, app)
card_github.init(app, templates, api)


@app.get("/")
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# @TODO: handle exceptions
# @TODO: make app / templates as global object
# @TODO: widget checks widet_id key in global state / data and raises error
# @TODO: handle github token errors
# @TODO: repo visibility
# @TODO: start new vs open recent
# @TODO: sdk widfget style - import local script tag <link>
# @TODO: api object from request (to handle labelers tokens)
