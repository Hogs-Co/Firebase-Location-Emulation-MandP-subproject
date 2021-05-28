import os
import sys
import asyncio
import concurrent.futures
import numpy as np
import pandas as pd
from io import StringIO
from time import sleep
from win32api import GetSystemMetrics

import kivy
import json
import collections

import database_access as dba
import user_creation_and_manip as ucm
import coords_creation_and_manip as ccm

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
from kivy_garden.mapview import MapView, MapMarker


WIDTH = 1000
HEIGHT = 1000

Window.size = (WIDTH, HEIGHT)
Window.top = 40 + max(GetSystemMetrics(1) // 2 - 540, 0)
Window.left = GetSystemMetrics(0) // 2 - 500

executor = concurrent.futures.ThreadPoolExecutor(max_workers=20)


class HomeWindow(Screen):
    def show_popup_map(self):
        show_popup_mapview()

    def show_popup_sim_map(self):
        show_popup_sim_mapview()

    pass


# Buttons
class DeleteUserBtn(Button):
    def __init__(self, userid):
        super().__init__()
        self.pos_hint = {'right': 1, 'bottom': 0}
        self.size_hint = (.15, None)
        self.height = 175
        self.text = "Delete\nuser"
        self.userid = userid

    def on_press(self):
        show_popup_delete_user(self.userid)

    pass


class UpdateUserDataBtn(Button):
    def __init__(self, userid):
        super().__init__()
        self.pos_hint = {'right': 1, 'bottom': 0}
        self.size_hint = (.15, None)
        self.height = 175
        self.text = "Update\nuser\ndata"
        self.userid = userid

    def on_press(self):
        show_popup_update_user_data(self.userid)

    pass


# Screens and Views
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
                self.ids.content.add_widget(Label(text=user_info, size_hint=(1, None), markup=True,
                                                  text_size=(None, None), height=int(0.25 * HEIGHT)))
                self.ids.content.size_hint = (1, (300 * len(users_list)) / HEIGHT)
                counter += 1
        else:
            self.ids.content.add_widget(Label(text="No users to display", size_hint_y=None, markup=True,
                                              text_size=(None, None), height=160))

    pass


class ScrollContent(ScrollView):
    pass


class ManageWindow(Screen):
    # @staticmethod
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

                delete_user_btn = DeleteUserBtn(user_info_dict[dba.user_keys[0]])
                update_user_data_btn = UpdateUserDataBtn(user_info_dict[dba.user_keys[0]])

                self.ids.content.add_widget(Label(text=user_info, size_hint=(.7, None), markup=True,
                                                  pos_hint={'right': 1, 'bottom': 0}, height=int(0.25 * HEIGHT)))
                self.ids.content.add_widget(delete_user_btn)
                self.ids.content.add_widget(update_user_data_btn)
                self.ids.content.size_hint = (1, None)
                self.ids.content.height = (int(0.25 * HEIGHT) + 10) * len(users_list)
                counter += 1
        else:
            self.ids.content.add_widget(Label(text="No users to display", size_hint=(.7, None), markup=True,
                                              pos_hint={'right': 1, 'bottom': 0}, height=int(0.25 * HEIGHT)))

    pass


class GenerateWindow(Screen):
    pass


class GenerateUsersWindow(Screen):
    def btn_append(self):
        show_popup_append()

    def btn_clear_and_generate(self):
        show_popup_clear_and_generate()

    pass


class GenerateTagsWindow(Screen):
    def btn_add_new_tags(self):
        show_popup_add_new_tags()

    def btn_delete_all_tags(self):
        show_popup_delete_all_tags()

    def btn_add_users_to_tags(self):
        show_popup_add_users_to_tags()

    pass


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("emulation.kv")


# Popups
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
    def __init__(self, userid):
        super().__init__()
        self.userid = userid

    def incorrect_data(self):
        self.ids.incorrect_data.text = "Incorrect password or data"

    def correct_data(self):
        self.ids.incorrect_data.text = ''
        self.ids.correct_data.text = 'Done'

    pass


class PopUpdateUserData(FloatLayout):
    def __init__(self, userid):
        super().__init__()
        self.userid = userid

    def incorrect_data(self):
        self.ids.incorrect_data.text = "Incorrect password or data"

    def correct_data(self):
        self.ids.incorrect_data.text = ''
        self.ids.correct_data.text = 'Done'

    # @staticmethod
    def generate_data_dict(self):
        data_dict = {}
        for key, val in self.ids.items():
            if key not in ["password", "incorrect_data", "correct_data"] and val.text != "":
                if key == "Current_localization":
                    new_coords = str(val.text).split(sep=";")
                    data_dict[str(key)] = (int(new_coords[0]), int(new_coords[1]))
                elif key == "Email" and not ucm.check_email(str(val.text)):
                    self.incorrect_data()
                    return None
                else:
                    data_dict[str(key)] = str(val.text)
        return data_dict

    pass


class PopAddNewTags(FloatLayout):
    def entry_done(self):
        self.ids.entry_done.text = 'Done'

    pass


class PopDeleteAllTags(FloatLayout):
    def incorrect_data(self):
        self.ids.incorrect_data.text = "Incorrect password"

    def correct_data(self):
        self.ids.incorrect_data.text = ''
        self.ids.correct_data.text = 'Done'

    pass


class PopAddUsersToTags(FloatLayout):
    def incorrect_password(self):
        self.ids.incorrect_passwd.text = "Incorrect password"

    def correct_password(self):
        self.ids.incorrect_passwd.text = ''
        self.ids.correct_passwd.text = 'Done'

    pass


class PopMapView(MapView):
    def __init__(self):
        super().__init__()
        counter = 0
        for coord in ccm.give_start_points():
            marker = MapMarker(lon=coord[0], lat=coord[1],
                               source=os.path.join("coords", "start_point.png"))
            super().add_marker(marker)
            counter += 1

        counter = 0
        for coord in ccm.give_end_points():
            marker = MapMarker(lon=coord[0], lat=coord[1],
                               source=os.path.join("coords", "end_point.png"))
            super().add_marker(marker)
            counter += 1

    pass


class PopSimMapView(MapView):
    # In MapView:
    # Lon, Lat
    # In Google API's
    # Lat, Lon
    def __init__(self):
        super().__init__()

        self.users_json_str = json.dumps(dba.get_all_users('json'))
        self.users_data_firebase = pd.read_json(StringIO(self.users_json_str)).transpose()
        self.user_paths = {}
        self.counter = 0
        self.max_counter = 0

        for index, row in self.users_data_firebase.iterrows():
            random_path = ccm.get_random_path()
            self.max_counter = max(self.max_counter, len(random_path) - 1)
            self.user_paths[index] = random_path

        # counter = 0
        # for key in self.user_paths.keys():
        #     print(f"{counter}\n{key}: {self.user_paths[key]}", end="\n\n")
        #     counter += 1

        self.do_stuff()

    def do_stuff(self):
        event_loop = asyncio.new_event_loop()
        try:
            event_loop.run_until_complete(self.create_paths())
        finally:
            event_loop.close()

    async def create_paths(self):
        while self.counter != 1:
            for index, row in self.users_data_firebase.iterrows():
                row['CurrentLocation'] = self.user_paths[row['Id']][min(self.counter,
                                                                        len(self.user_paths[row['Id']]) - 1)]
                self.users_json_str = self.users_data_firebase.transpose().to_json()
                dba.update_all_users(json.loads(self.users_json_str))
                print(self.users_json_str)
            self.counter += 1
        pass

    pass


# Popup call functions: Users
def show_popup_append():
    show = PopCreateAppend()
    popup_window = Popup(title="Append users list", content=show, size_hint=(None, None), size=(400, 400))
    popup_window.open()


def show_popup_clear_and_generate():
    show = PopClearAndGenerate()
    popup_window = Popup(title="Clear current users list and generate new", content=show, size_hint=(None, None),
                         size=(400, 400))
    popup_window.open()


def show_popup_delete_user(userid):
    show = PopDeleteUser(userid)
    popup_window = Popup(title="Delete chosen user", content=show, size_hint=(None, None), size=(400, 400))
    popup_window.open()


def show_popup_update_user_data(userid):
    show = PopUpdateUserData(userid)
    popup_window = Popup(title="Update chosen user's data", content=show, size_hint=(None, None), size=(400, 400))
    popup_window.open()


# Popup call functions: Tags
def show_popup_add_new_tags():
    show = PopAddNewTags()
    popup_window = Popup(title="Add new tags", content=show, size_hint=(None, None), size=(400, 400))
    popup_window.open()


def show_popup_delete_all_tags():
    show = PopDeleteAllTags()
    popup_window = Popup(title="Delete all tags", content=show, size_hint=(None, None), size=(400, 400))
    popup_window.open()


def show_popup_add_users_to_tags():
    show = PopAddUsersToTags()
    popup_window = Popup(title="Add users to tags", content=show, size_hint=(None, None), size=(400, 400))
    popup_window.open()


def show_popup_mapview():
    show = PopMapView()
    popup_window = Popup(title="Map", content=show, size_hint=(None, None), size=(900, 900))
    popup_window.open()


def show_popup_sim_mapview():
    show = PopSimMapView()
    popup_window = Popup(title="Simulation", content=show, size_hint=(None, None), size=(900, 900))
    popup_window.open()


# App call function
class EmulationApp(App):
    def __init__(self):
        super().__init__()
        self.new_load = True

    def build(self):
        Window.clearcolor = (0, 0, 0, 0)
        return kv


if __name__ == "__main__":
    EmulationApp().run()
