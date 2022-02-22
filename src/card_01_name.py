import os
from haikunator import Haikunator
import supervisely as sly
from fastapi import APIRouter, FastAPI, Request, Depends
from supervisely.app.content import DataJson, StateJson
from supervisely.app.fastapi import Jinja2Templates

# import card_github
router = APIRouter()


_vscode = "vscode"
_agent_name = os.environ["AGENT_NAME"]
_agent_path = os.environ["SUPERVISELY_AGENT_FILES"]

_haikunator = Haikunator()
_default_name = "my-app-"

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
    return os.path.join(_agent_path, _vscode, name)


def generate_team_files_path(name):
    return os.path.join("/", _agent_name, _vscode, name)


def generate_project_name():
    return _default_name + _haikunator.haikunate(token_length=0)


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
    raise ValueError(123)
    data = DataJson()
    state["name"] = generate_project_name()
    update_paths()
    state = None
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
