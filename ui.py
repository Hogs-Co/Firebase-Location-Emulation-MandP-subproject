import kivy
import database_access as dba
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout

Window.size = (600, 600)


class HomeWindow(Screen):
    pass


class BrowseWindow(Screen):
    pass


class ManageWindow(Screen):
    pass


class GenerateUsersWindow(Screen):
    def btnAppend(self):
        show_popup_append()

    def btnClearAndGenerate(self):
        show_popup_clear_and_generate()
    pass


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("emulation.kv")


class PopCreateAppend(FloatLayout):
    pass


class PopClearAndGenerate(FloatLayout):
    def incorrectPassword(self):
        self.ids.incorrectPasswd.text = "Incorrect password"

    def correctPassword(self):
        self.ids.incorrectPasswd.text = ''
        self.ids.correctPasswd.text = 'Done'
    pass


class Pop(FloatLayout):
    pass


class EmulationApp(App):
    def build(self):
        Window.clearcolor = (0, 0, 0, 0)
        return kv


def show_popup_append():
    show = PopCreateAppend()
    popupWindow = Popup(title="Append users list", content=show, size_hint=(None,None), size=(400,400))
    popupWindow.open()


def show_popup_clear_and_generate():
    show = PopClearAndGenerate()
    popupWindow = Popup(title="Clear current users list and generate new", content=show, size_hint=(None,None), size=(400,400))
    popupWindow.open()


if __name__ == "__main__":
    EmulationApp().run()
