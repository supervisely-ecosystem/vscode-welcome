import supervisely as sly

templates_table = sly.app.widgets.RadioTable(
    widget_id="appTemplates",
    columns=["name", "github", "column #3"],
    rows=[
        ["Hello <user>!", "gh1", "-"],
        ["Random point", "gh2", "-"],
    ],
    subtitles={"name": "subname"},
)


def get_jinja2_context():
    return {"app_templates": templates_table}


def init(data: dict, state: dict):
    templates_table.init(data, state)
