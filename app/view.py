
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty

class MainWindow(BoxLayout):
    username = StringProperty("mandos")
    role = StringProperty("user")
    def __init__(self, **kw):
        super().__init__(**kw)
