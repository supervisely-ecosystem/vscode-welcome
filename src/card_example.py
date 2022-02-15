import supervisely as sly
from fastapi import FastAPI
from supervisely.app.fastapi import Jinja2Templates


def format_github_column(value):
    new_val = f"""
    <i class="zmdi zmdi-github mr5"></i>
    <a href="{value}" target="_blank">{value}</a>
"""
    return new_val


examples = sly.app.widgets.RadioTable(
    widget_id="examples",
    columns=["name", "github", "column #3"],
    rows=[
        [
            "Hello <user>!",
            "https://github.com/supervisely-ecosystem/dev-names-generator.git",
            None,
        ],
        [
            "Random point",
            "https://github.com/supervisely-ecosystem/dev-names-generator.git",
            "abcd",
        ],
    ],
    subtitles={"name": "subname"},
    column_formatters={"github": format_github_column},
)


def init(app: FastAPI, templates: Jinja2Templates, data: dict, state: dict):
    examples.init(data, state)
    templates.context_widgets[examples.widget_id] = examples
