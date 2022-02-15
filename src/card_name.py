import os
from haikunator import Haikunator
import supervisely as sly
from fastapi import APIRouter, FastAPI, Request, Depends
from supervisely.app.fastapi import Jinja2Templates

router = APIRouter()

_vscode = "vscode"
_agent_name = os.environ["AGENT_NAME"]
_agent_path = os.environ["SUPERVISELY_AGENT_FILES"]

_haikunator = Haikunator()
_default_name = "my-app-"


def preview_local_path(name):
    return os.path.join(_agent_path, _vscode, name)


def preview_team_files_path(name):
    return os.path.join("/", _agent_name, _vscode, name)


def generate_project_name():
    return _default_name + _haikunator.haikunate(token_length=0)


def init(app: FastAPI, templates: Jinja2Templates, data: dict, state: dict):
    name = generate_project_name()
    state["name"] = name
    update_paths(name, data)
    app.include_router(router)


def update_paths(name: str, data: dict):
    data["localPath"] = preview_local_path(name)
    data["teamFilesPath"] = preview_team_files_path(name)


@router.post("/generate")
async def generate(
    request: Request, state: sly.app.StateJson = Depends(sly.app.StateJson.from_request)
):
    print(sly.app.LastStateJson())
    data = sly.app.DataJson()
    init(state, data)
    await state.synchronize_changes()
    await data.synchronize_changes()


@router.post("/name-changed")
async def name_changed(
    request: Request, state: sly.app.StateJson = Depends(sly.app.StateJson.from_request)
):
    data = sly.app.DataJson()
    update_paths(state["name"], data)
    await data.synchronize_changes()
