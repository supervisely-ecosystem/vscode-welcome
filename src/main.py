import os
import sys
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
import supervisely as sly
import names

app_repo_dir = os.getcwd()  # app root directory (working directory)
sys.path.append(app_repo_dir)
sys.path.append(os.path.join(app_repo_dir, "src"))
print(f"App root directory: {app_repo_dir}")

# @TODO: repo visibility
# @TODO: start new vs open recent
# @TODO: replace special symbols (space-> '-') in app-name

# order matters
load_dotenv(os.path.join(app_repo_dir, "secret.env"))
load_dotenv(os.path.join(app_repo_dir, "debug.env"))

import src.preview_paths as step1

from src.preview_paths import init, update_paths

# init global state and data (singletons)
sly.app.LastStateJson({"activeStep": 1})
sly.app.DataJson({})
init(sly.app.LastStateJson(), sly.app.DataJson())

print(sly.app.LastStateJson())

app = FastAPI()
sly_app = sly.app.fastapi.create()
app.mount("/sly", sly_app)
app.mount("/static", StaticFiles(directory="static", html=True), name="static")
templates = sly.app.fastapi.Jinja2Templates(directory="templates")


@app.get("/")
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/generate")
async def generate(
    request: Request, state: sly.app.StateJson = Depends(sly.app.StateJson.from_request)
):
    print(sly.app.LastStateJson())
    data = sly.app.DataJson()
    init(state, data)
    await state.synchronize_changes()
    await data.synchronize_changes()


@app.post("/name-changed")
async def name_changed(
    request: Request, state: sly.app.StateJson = Depends(sly.app.StateJson.from_request)
):
    data = sly.app.DataJson()
    update_paths(state["name"], data)
    await data.synchronize_changes()
