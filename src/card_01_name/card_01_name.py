import os
from typing import TypedDict
from haikunator import Haikunator
import supervisely as sly
from fastapi import APIRouter, FastAPI, Request, Depends
from supervisely.app.content import DataJson, StateJson
from supervisely.app.fastapi import Jinja2Templates

# import card_github
router = APIRouter()


vscode = "vscode"
agent_name = os.environ["AGENT_NAME"]
agent_path = os.environ["SUPERVISELY_AGENT_FILES"]

haikunator = Haikunator()
default_name = "my-app-"

done1 = sly.app.widgets.DoneLabel("New application is defined")

# print(Path(__file__))
# print(Path(__file__).stem)
# print(Path(__file__).absolute())
# print(Path(__file__).parent.absolute())
# templates = Jinja2Templates()
# templates.context_widgets["card_01_name"] = self


def init():
    state = StateJson()
    state["name"] = generate_project_name()
    data = DataJson()
    update_paths()


def generate_local_path(name):
    return os.path.join(agent_path, vscode, name)


def generate_team_files_path(name):
    return os.path.join("/", agent_name, vscode, name)


def generate_project_name():
    return default_name + haikunator.haikunate(token_length=0)


def update_paths():
    state = StateJson()
    data = DataJson()
    name = state["name"]
    data["localPath"] = generate_local_path(name)
    data["teamFilesPath"] = generate_team_files_path(name)
    # card_github.update_repo_url(name)


@router.post("/generate")
async def generate(
    request: Request, state: StateJson = Depends(StateJson.from_request)
):
    data = DataJson()
    state["name"] = generate_project_name()
    update_paths()
    await state.synchronize_changes()
    await data.synchronize_changes()


@router.post("/name-changed")
async def name_changed(
    request: Request, state: StateJson = Depends(StateJson.from_request)
):
    data = DataJson()
    update_paths()
    await data.synchronize_changes()


init()
