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
# @TODO: replace special symbols (space-> '-') in app-name
# @TODO: debug mode -add x-debug-mode : 1 in header
# @TODO: https://stackoverflow.com/questions/1690400/getting-an-instance-name-inside-class-init
# https://stackoverflow.com/questions/63436496/is-it-possible-to-have-python-ides-offer-autocompletion-for-dynamically-generate
# https://stackoverflow.com/questions/13603088/python-dynamic-help-and-autocomplete-generation/13603392#13603392
# https://intellij-support.jetbrains.com/hc/en-us/community/posts/115000665110-auto-completion-for-dynamic-module-attributes-in-python
# https://amir.rachum.com/blog/2016/10/05/python-dynamic-attributes/
# https://stackoverflow.com/questions/13603088/python-dynamic-help-and-autocomplete-generation
# https://github.com/dsc/bunch
# https://github.com/python-attrs/attrs

# order matters
load_dotenv(os.path.join(app_repo_dir, "secret.env"))
load_dotenv(os.path.join(app_repo_dir, "debug.env"))

# import src.preview_paths as step1

import card_general
import card_app_template

# init global state and data (singletons)
last_state = sly.app.LastStateJson({"activeStep": 1})
data = sly.app.DataJson({})
card_general.init(data, last_state)
card_app_template.init(data, last_state)


class WidgetsStorage:
    def __init__(self):
        pass

    def __dir__(self):
        return super().__dir__() + [str(k) for k in self.keys()]


app = FastAPI()
sly_app = sly.app.fastapi.create()
app.mount("/sly", sly_app)
app.include_router(card_general.router)
# app.mount("/static", StaticFiles(directory="static", html=True), name="static")
templates = sly.app.fastapi.Jinja2Templates(directory="templates")
sly.app.fastapi.enable_hot_reload_on_debug(app, templates)


@app.get("/")
async def read_index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            **card_app_template.get_jinja2_context(),
        },
    )
