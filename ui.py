import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window

Window.size = (600, 600)

class HomeWindow(Screen):
    pass


class BrowseWindow(Screen):
    pass


class ManageWindow(Screen):
    pass


class GenerateUsersWindow(Screen):
    pass



class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("emulation.kv")


class EmulationApp(App):
    def build(self):
        Window.clearcolor = (0,0,0,0)
        return kv

if __name__== "__main__":
    EmulationApp().run()