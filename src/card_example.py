import supervisely as sly


def format_github_column(value):
    new_val = f"""
    <i class="zmdi zmdi-github mr5"></i>
    <a href="{value}" target="_blank">{value}</a>
"""
    return new_val


templates_table = sly.app.widgets.RadioTable(
    widget_id="templates_table",
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


def get_jinja2_context():
    return {templates_table.widget_id: templates_table}


def init(data: dict, state: dict):
    templates_table.init(data, state)
