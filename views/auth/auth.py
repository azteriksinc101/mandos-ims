
from kivy.app import App
from kivy.lang import Builder

from kivy.uix.boxlayout import BoxLayout

Builder.load_file("views/auth/auth.kv")
class Auth(BoxLayout):
    def __init__(self, **kw):
        super().__init__(**kw)
        
    def validate_user(self):
        user = self.ids.username_field
        pwd = self.ids.pwd_field
        info = self.ids.info
        
        uname = user.text 
        passw = pwd.text
        
        if uname == '' or passw == '':
            info.text = '[color=#ff0000]username and/ or password required[/color]'
        else:
            if uname == 'admin' and passw == 'admin':
                info.text = '[color=#00ff00]Login Successfully[/color]'
                self.parent.parent.current = 'scrn_admin'
            else:
                info.text = '[color=#ff0000]Invalid Username and/or Password[/color]'