import supervisely as sly

templates_table = sly.app.widgets.RadioTable(
    state_field="selectedDemo",
    data_field="demos",
    radio_key="name",
    columns=["name", "github", "column #3"],
    rows=[
        {"Hello <user>!", "gh1", "-"},
        {"Random point", "gh2", "-"},
    ],
    subtitles={"name": "subname"},
)


def get_jinja2_context():
    return {"templates": templates_table}
