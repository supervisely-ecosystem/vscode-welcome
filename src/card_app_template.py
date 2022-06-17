import supervisely as sly

templates_table = sly.app.widgets.RadioTable(
    columns=["name", "github", "column #3"],
    rows=[
        ["Hello <user>!", "gh1", "-"],
        ["Random point", "gh2", "-"],
    ],
    subtitles={"name": "subname"},
)

# rows=[
#         {"Hello <user>!", "gh1", "-"},
#         {"Random point", "gh2", "-"},
#     ]


def get_jinja2_context():
    return {"templates": templates_table}
