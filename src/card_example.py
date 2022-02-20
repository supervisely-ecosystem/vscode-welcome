import supervisely as sly


def format_github_column(value):
    new_val = f"""
    <i class="zmdi zmdi-github mr5"></i>
    <a href="{value}" target="_blank">github</a>
    """
    return new_val


def format_description_column(value):
    new_val = f"""
    <div style="text-align: left">{value}</div>
    """
    return new_val


examples = sly.app.widgets.RadioTable(
    columns=["name", "github", "description"],
    rows=[
        [
            "Hello <user>!",
            "https://github.com/supervisely-ecosystem/dev-names-generator.git",
            "How to handle button clicks and dynamically update variable",
        ],
        [
            "Random circle",
            "https://github.com/supervisely-ecosystem/dev-names-generator.git",
            "Upload local image, modify it and preview both images",
        ],
    ],
    subtitles={},  # {"name": "subname"},
    column_formatters={
        "github": format_github_column,
        "description": format_description_column,
    },
)
