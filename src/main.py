import os
import sys
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
import arel
import supervisely as sly


app_repo_dir = os.getcwd()  # app root directory (working directory)
sys.path.append(app_repo_dir)
sys.path.append(os.path.join(app_repo_dir, "src"))
print(f"App root directory: {app_repo_dir}")

# order matters
load_dotenv(os.path.join(app_repo_dir, "secret.env"))
load_dotenv(os.path.join(app_repo_dir, "debug.env"))

# init global state and data (singletons)

app = FastAPI()
templates = sly.app.fastapi.Jinja2Templates(directory="templates")
app.mount("/sly", sly.app.fastapi.create())
api = sly.Api.from_env()
# app.mount("/static", StaticFiles(directory="static", html=True), name="static")
sly.app.fastapi.enable_hot_reload_on_debug(app, templates)

import card_name
import card_example
import card_github

state = sly.app.StateJson({"activeStep": 1})
data = sly.app.DataJson()

# state = sly.app.StateJson()

card_name.init(app, templates, data, state)
card_example.init(app, templates, data, state)
card_github.init(app, templates, api, data, state)


@app.get("/")
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# @TODO: widget checks widet_id key in global state and raises error
# @TODO: handle github token errors
# @TODO: repo visibility
# @TODO: start new vs open recent
