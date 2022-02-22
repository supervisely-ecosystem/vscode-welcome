from dataclasses import dataclass
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Depends
import supervisely as sly

src_dir = str(Path(__file__).parent.absolute())
app_dir = str(Path(src_dir).parent)
sys.path.extend([src_dir, app_dir])
print(f"PYTHON_PATH updated: {[src_dir, app_dir]}")

# order matters (used for debug)
load_dotenv(os.path.join(app_dir, "secret.env"))
load_dotenv(os.path.join(app_dir, "debug.env"))


app = FastAPI()
sly.app.fastapi.init(app)

state = sly.app.StateJson()
data = sly.app.DataJson()
state["step"] = 1

import card_01_name
import card_02_example
import card_03_github

app.include_router(card_01_name.router)


@app.get("/")
async def read_index(request: Request):
    templates = sly.app.fastapi.Jinja2Templates(directory="templates")
    return templates.TemplateResponse("index.html", {"request": request})


# @TODO: remove restart dialog from SDK
# @TODO: handle errors with readble dialog window - stack trace to html (discuss with den)
# @TODO: restart dialog how to call routes functions from various files
# @TODO: widgets storage? - separate file???
# @TODO: handle github token errors
# @TODO: repo visibility
# @TODO: start new vs open recent
# @TODO: api object from request (to handle labelers tokens)
