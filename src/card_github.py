import sys
import os
import supervisely as sly
from fastapi import APIRouter, FastAPI, Request, Depends
from supervisely.app.fastapi import Jinja2Templates


gh_info = {}
_private_path = os.path.expanduser("~/.ssh/id_rsa")
_public_path = os.path.expanduser("~/.ssh/id_rsa.pub")


def generate_repo_url(state):
    name = state["name"]
    organization = gh_info.get("login", "your-organization")
    return f"https://github.com/{organization}/{name}"


def update_repo_url(data, state):
    data["repoUrl"] = generate_repo_url(state)


def init(
    app: FastAPI, templates: Jinja2Templates, api: sly.Api, data: dict, state: dict
):
    def create_keys():
        sly.logger.info("Create SSH keys")
        keys = api.user.get_github_keys()
        with open(_private_path, "w") as f:
            f.write(keys["private"])
        with open(_public_path, "w") as f:
            f.write(keys["public"])

    gettrace = getattr(sys, "gettrace", None)
    if gettrace is None:
        pass
        # print("Can not detect debug mode, no sys.gettrace")
    elif gettrace():
        if not sly.fs.file_exists(_public_path):
            sly.logger.info("Create keys during debug")
            create_keys()
    else:
        # print("In runtime mode ..."
        # in container for production
        create_keys()

    global gh_info
    gh_info = api.github.get_account_info()
    update_repo_url(data, state)
    # name = generate_project_name()
    # state["name"] = name
    # update_paths(name, data)
    # app.include_router(router)
