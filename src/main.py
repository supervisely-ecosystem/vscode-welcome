from dataclasses import dataclass
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Depends
import supervisely as sly

# @TODO: move to agent
src_dir = str(Path(__file__).parent.absolute())
root_dir = str(Path(src_dir).parent)
sys.path.extend([src_dir, root_dir])
print(f"PYTHON_PATH updated: {[src_dir, root_dir]}")

# order matters (used for debug)
load_dotenv(os.path.join(root_dir, "secret.env"))
load_dotenv(os.path.join(root_dir, "debug.env"))


app = FastAPI()
sly.app.fastapi.init(app, root_dir)

state = sly.app.StateJson()
data = sly.app.DataJson()
state["step"] = 1

# @TODO: rename _haikunator remove all leading _
import src.card_01_name
import card_02_example
import card_03_github

app.include_router(card_01_name.router)


@app.get("/")
async def read_index(request: Request):
    templates = sly.app.fastapi.Jinja2Templates(directory=root_dir)
    return templates.TemplateResponse("templates/index.html", {"request": request})


# @TODO: restart dialog how to call routes functions from various files
# @TODO: widgets storage? - separate file???
# @TODO: handle github token errors
# @TODO: repo visibility
# @TODO: start new vs open recent
# @TODO: api object from request (to handle labelers tokens)
