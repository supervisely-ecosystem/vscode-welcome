from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
import supervisely as sly
import names


# init global state and data (singletons)
sly.app.LastStateJson({"name": ""})
sly.app.DataJson({})

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
