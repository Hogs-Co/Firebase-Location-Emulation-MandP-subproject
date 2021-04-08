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
from kivy.properties import ObjectProperty
from kivy.uix.stacklayout import StackLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.text import LabelBase

Window.size = (600, 600)


class HomeWindow(Screen):
    pass


class BrowseWindow(Screen):
    def btn_create_user_labels(self):

        users_list = dba.get_all_users()
        counter = 1

        for child in [child for child in self.ids.content.children]:
            self.ids.content.remove_widget(child)

        if len(users_list) != 0:
            for x in range(len(users_list)):
                user_info_dict = users_list[x]

                user_info = f"[b][{counter}][/b]\n"
                for key in user_info_dict.keys():
                    value = user_info_dict[key]
                    user_info += "[b]{0:22}[/b]{1}\n".format(str(key) + ':', str(value))
                self.ids.content.add_widget(Label(text=user_info, size_hint=(1, None), markup=True, text_size=(None, None),
                                                  height=160))
                self.ids.content.size_hint = (1, (179.5*len(users_list))/600)
                counter += 1
        else:
            self.ids.content.add_widget(Label(text="No users to display", size_hint_y=None, markup=True, text_size=(None, None),
                                              height=160))
    pass


class ScrollContent(ScrollView):
    pass


class ManageWindow(Screen):
    def btn_create_user_labels(self):

        users_list = dba.get_all_users()

        counter = 1

        for child in [child for child in self.ids.content.children]:
            self.ids.content.remove_widget(child)

        if len(users_list) != 0:
            for x in range(len(users_list)):
                user_info_dict = users_list[x]

                user_info = f"[b][{counter}][/b]\n"

                for key in user_info_dict.keys():
                    value = user_info_dict[key]
                    user_info += "[b]{0:22}[/b]{1}\n".format(str(key) + ':', str(value))
                self.ids.content.add_widget(Label(text=user_info, size_hint=(1, None), markup=True,
                                                  text_size=(None, None), height=160))
                self.ids.content.size_hint = (1, (179.5*len(users_list))/600)
                counter += 1
        else:
            self.ids.content.add_widget(Label(text="No users to display", size_hint_y=None, markup=True, text_size=(None, None),
                                              height=160))

    def btn_delete_user(self):
        show_popup_delete_user()

    def btn_update_user_data(self):
        show_popup_update_user_data()

    pass


class GenerateUsersWindow(Screen):
    def btn_append(self):
        show_popup_append()

    def btn_clear_and_generate(self):
        show_popup_clear_and_generate()

    pass


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("emulation.kv")


class PopCreateAppend(FloatLayout):
    def entry_done(self):
        self.ids.entry_done.text = 'Done'
    pass


class PopClearAndGenerate(FloatLayout):
    def incorrect_password(self):
        self.ids.incorrect_passwd.text = "Incorrect password"

    def correct_password(self):
        self.ids.incorrect_passwd.text = ''
        self.ids.correct_passwd.text = 'Done'
    pass


class PopDeleteUser(FloatLayout):
    def incorrect_data(self):
        self.ids.incorrect_data.text = "Incorrect password or data"

    def correct_data(self):
        self.ids.incorrect_data.text = ''
        self.ids.correct_data.text = 'Done'
    pass


class PopUpdateUserData(FloatLayout):
    def incorrect_data(self):
        self.ids.incorrect_data.text = "Incorrect password or data"

    def correct_data(self):
        self.ids.incorrect_data.text = ''
        self.ids.correct_data.text = 'Done'

    # @staticmethod
    def generate_data_dict(self, keys_string, data_string):
        keys_list = keys_string.split(sep=";")
        data_list = data_string.split(sep=";")

        data_dict = {}
        for key, value in zip(keys_list, data_list):
            if value.isdigit():
                data_dict[key] = int(value)
            else:
                data_dict[key] = value
        return data_dict

    pass


class Pop(FloatLayout):
    pass


class EmulationApp(App):
    def build(self):
        Window.clearcolor = (0, 0, 0, 0)
        return kv


def show_popup_append():
    show = PopCreateAppend()
    popup_window = Popup(title="Append users list", content=show, size_hint=(None,None), size=(400, 400))
    popup_window.open()


def show_popup_clear_and_generate():
    show = PopClearAndGenerate()
    popup_window = Popup(title="Clear current users list and generate new", content=show, size_hint=(None,None),
                         size=(400, 400))
    popup_window.open()


def show_popup_delete_user():
    show = PopDeleteUser()
    popup_window = Popup(title="Delete chosen user", content=show, size_hint=(None,None), size=(400, 400))
    popup_window.open()


def show_popup_update_user_data():
    show = PopUpdateUserData()
    popup_window = Popup(title="Update chosen user's data", content=show, size_hint=(None, None), size=(400, 400))
    popup_window.open()


if __name__ == "__main__":
    EmulationApp().run()
