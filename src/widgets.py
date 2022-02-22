import supervisely as sly
from supervisely.app.content import Singleton


class WidgetsStorage(metaclass=Singleton):
    # card_01_name
    done1: sly.app.widgets.DoneLabel = None
