import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
import supervisely as sly

src_dir = str(Path(__file__).parent.absolute())
app_dir = str(Path(src_dir).parent)
sys.path.extend([src_dir, app_dir])
print(f"PYTHON_PATH updated: {[src_dir, app_dir]}")

# order matters (used for debug)
load_dotenv(os.path.join(app_dir, "secret.env"))
load_dotenv(os.path.join(app_dir, "debug.env"))


import card_name
import card_example
import card_github


app = FastAPI()
sly.app.fastapi.enable_hot_reload_on_debug(app)
app.mount("/sly", sly.app.fastapi.create())
app.include_router(card_name.router)

state = sly.app.StateJson()
state["activeStep"] = 1
data = sly.app.DataJson()


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
