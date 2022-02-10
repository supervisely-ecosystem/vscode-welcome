import os
from haikunator import Haikunator

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
