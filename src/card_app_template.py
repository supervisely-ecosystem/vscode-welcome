import supervisely as sly

templates = [
    {"name": "Hello <user>!", "github": "gh1"},
    {"name": "Random point", "github": "gh2"},
]

templates_table = sly.app.widgets.RadioTable(
    state_field="selectedDemo", data_field="demos", content=templates
)


def get_jinja2_context():
    return {"templates": templates_table}
