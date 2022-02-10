import os
import sys
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
import supervisely as sly
import names

from preview_paths import (
    preview_local_path,
    preview_team_files_path,
    generate_project_name,
)

app_repo_dir = os.getcwd()  # app root directory (working directory)
sys.path.append(app_repo_dir)
print(f"App root directory: {app_repo_dir}")

# order matters
load_dotenv(os.path.join(app_repo_dir, "secret.env"))
load_dotenv(os.path.join(app_repo_dir, "debug.env"))


name = generate_project_name()

# init global state and data (singletons)
sly.app.LastStateJson(
    {
        "name": name,
    }
)
sly.app.DataJson(
    {
        "localPath": preview_local_path(name),
        "teamFilesPath": preview_team_files_path(name),
    }
)

app = FastAPI()
sly_app = sly.app.fastapi.create()
app.mount("/sly", sly_app)
app.mount("/static", StaticFiles(directory="static", html=True), name="static")
templates = sly.app.fastapi.Jinja2Templates(directory="templates")


@app.get("/")
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/generate")
async def generate(request: Request):
    data = sly.app.DataJson()
    data["name"] = names.get_first_name()
    await data.synchronize_changes()


@app.post("/generate-local-path")
async def generate_local_path(
    request: Request, state: sly.app.StateJson = Depends(sly.app.StateJson.from_request)
):
    state["localPath"] = os.path.join(
        os.getenv("SUPERVISELY_AGENT_FILES"), "vscode", state["name"]
    )
    await state.synchronize_changes()
