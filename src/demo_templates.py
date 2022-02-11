import supervisely as sly

templates = [
    {"name": "Hello <user>!", "github": "5:00", "year": 2010},
    {"points": 25, "time": "6:00", "month": "february"},
    {"points": 90, "time": "9:00", "month": "january"},
    {"points_h1": 20, "month": "june"},
]

a = 123

demos_table = sly.app.widgets.RadioTable()


def get_jinja2_context():
    return {"demos_table": demos_table}
