import os
import sys
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Depends

# from fastapi.staticfiles import StaticFiles
import supervisely as sly
import names
import arel


app_repo_dir = os.getcwd()  # app root directory (working directory)
sys.path.append(app_repo_dir)
sys.path.append(os.path.join(app_repo_dir, "src"))
print(f"App root directory: {app_repo_dir}")

# @TODO: repo visibility
# @TODO: start new vs open recent

# order matters
load_dotenv(os.path.join(app_repo_dir, "secret.env"))
load_dotenv(os.path.join(app_repo_dir, "debug.env"))

import card_name
import card_example

# init global state and data (singletons)
last_state = sly.app.LastStateJson({"activeStep": 1})
data = sly.app.DataJson({})
card_name.init(app, data, last_state, templates)
card_example.init(data, last_state, templates)


app = FastAPI()
templates = sly.app.fastapi.Jinja2Templates(directory="templates")
sly_app = sly.app.fastapi.create()
app.mount("/sly", sly_app)

# app.mount("/static", StaticFiles(directory="static", html=True), name="static")

sly.app.fastapi.enable_hot_reload_on_debug(app, templates)


@app.get("/")
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
