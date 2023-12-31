
from datetime import datetime
import hashlib
from threading import Thread
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.uix.behaviors import ButtonBehavior
from kivy.metrics import dp, sp
from kivy.utils import rgba, QueryDict
import mysql.connector

from kivy.clock import Clock, mainthread

from kivy.properties import StringProperty, ListProperty, ColorProperty, NumericProperty, ObjectProperty
from widgets.popups import ConfirmDialog

Builder.load_file('views/users/users.kv')
class Users(BoxLayout):
    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        Clock.schedule_once(self.render, .1)
        self.currentUser = None

    def render(self, _):
        t1 = Thread(target=self.get_users, daemon=True)
        t1.start()
    
    def add_new(self):
        md = ModUser()
        md.callback = self.add_user
        md.open()
    
    def get_users(self):
        mydb = mysql.connector.connect(
           host='localhost',
           user='root',
           passwd='#hasH537',
           database='pos'
        )
        mycursor = mydb.cursor()
        _users = OrderedDict()
        _users['firstName'] = {}
        _users['lastName'] = {}
        _
        users = [
            {
                "firstName": "Samuel",
                "lastName": "Mthembo",
                "username": "first.samuel",
                "password": "dhqw8473242fsdt34",
                "createdAt": "2023/01/12 12:45:56",
                "signedIn": "2023/01/12 14:25:06"
            },
            {
                "firstName": "Julian",
                "lastName": "Mthembo",
                "username": "first.julian",
                "password": "dhqw8473242fssdsatrq34dt34",
                "createdAt": "2023/01/12 01:43:06",
                "signedIn": "2022/11/08 11:21:06"
            },
            {
                "firstName": "John",
                "lastName": "Doe",
                "username": "doe.john",
                "password": "dhqw8435356373242fsdt34",
                "createdAt": "2022/11/02 10:05:58",
                "signedIn": "2023/01/12 10:12:00"
            },
        ]
        self.set_users(users)
    
    def add_user(self, mv):
        fname = mv.ids.fname
        lname = mv.ids.lname
        uname = mv.ids.uname
        pwd = mv.ids.pwd
        cpwd = mv.ids.cpwd
        # First check if inputs are not empty
        if len(fname.text.strip()) < 3:
            # Inform user that first name is invalid
            return
        
        _pwd = pwd.text.strip()
        upass = hashlib.sha256(_pwd.encode()).hexdigest()
        now = datetime.now()
        _now = datetime.strftime(now, "%Y/%m/%d %H:%M")

        user = {
                "firstName": fname.text.strip(),
                "lastName": lname.text.strip(),
                "username": uname.text.strip(),
                "password": upass,
                "createdAt": _now,
                "signedIn": "2023/01/12 14:25:06"
            }
        
        self.set_users([user])
    
    def update_user(self, user):
        mv = ModUser()
        mv.first_name = user.first_name
        mv.last_name = user.last_name
        mv.username = user.username
        mv.callback = self.set_update

        mv.open()
    
    def set_update(self, mv):
        print("updating...")

    
    @mainthread
    def set_users(self, users:list):
        grid = self.ids.gl_users
        grid.clear_widgets()

        for u in users:
            ut = UserTile()
            ut.first_name = u['firstName']
            ut.last_name = u['lastName']
            ut.username = u['username']
            ut.password = u['password']
            ut.created = u['createdAt']
            ut.last_login = u['signedIn']
            ut.callback = self.delete_user
            ut.bind(on_release=self.update_user)

            grid.add_widget(ut)
    
    def delete_user(self, user):
        self.currentUser = user
        dc = ConfirmDialog()
        dc.title = "Delete User"
        dc.subtitle = "Are you sure you want to delete this user?"
        dc.textConfirm = "Yes, Delete"
        dc.textCancel = "Cancel"
        dc.confirmColor = App.get_running_app().color_tertiary
        dc.cancelColor = App.get_running_app().color_primary
        dc.confirmCallback = self.delete_from_view
        dc.open()
    
    def delete_from_view(self, confirmDialog):

        if self.currentUser:
            self.currentUser.parent.remove_widget(self.currentUser)

class UserTile(ButtonBehavior, BoxLayout):
    first_name = StringProperty("")
    last_name = StringProperty("")
    username = StringProperty("")
    password = StringProperty("")
    created = StringProperty("")
    last_login = StringProperty("")
    callback = ObjectProperty(allownone=True)
    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        Clock.schedule_once(self.render, .1)

    def render(self, _):
        pass

    def delete_user(self):
        if self.callback:
            self.callback(self)

class ModUser(ModalView):
    first_name = StringProperty("")
    last_name = StringProperty("")
    username = StringProperty("")
    created = StringProperty("")
    last_login = StringProperty("")
    callback = ObjectProperty(allownone=True)
    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        Clock.schedule_once(self.render, .1)

    def render(self, _):
        pass

    def on_first_name(self, inst, fname):
        self.ids.fname.text = fname
        self.ids.title.text = "Update User"
        self.ids.btn_confirm.text = "Update User"
        self.ids.subtitle.text = "Enter your details below to update user"

    def on_last_name(self, inst, lname):
        self.ids.lname.text = lname

    def on_username(self, inst, fname):
        self.ids.uname.text = fname
        