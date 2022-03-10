import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
import supervisely as sly


# order matters (used for debug)
load_dotenv(os.path.join(os.getcwd(), "secret.env"))
load_dotenv(os.path.join(os.getcwd(), "debug.env"))


app = FastAPI()
sly.app.fastapi.init(app)

state = sly.app.StateJson()
data = sly.app.DataJson()
state["step"] = 1

import src.card_01_name as card_01_name
import src.card_02_example as card_02_example
import src.card_03_github as card_03_github

app.include_router(card_01_name.router)


@app.get("/")
async def read_index(request: Request):
    templates = sly.app.fastapi.Jinja2Templates(directory=os.getcwd())
    return templates.TemplateResponse("templates/index.html", {"request": request})


# test-app
# - raise error
# - session info
# - state mod
# - data mod
# - save to file state / data
# - projects list

# @TODO: restart dialog how to call routes functions from various files
# @TODO: widgets storage? - separate file???
# @TODO: handle github token errors
# @TODO: repo visibility
# @TODO: start new vs open recent
# @TODO: api object from request (to handle labelers tokens)
