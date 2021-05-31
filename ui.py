import os
import asyncio
import concurrent.futures

import pandas as pd
from io import StringIO
from time import sleep
from win32api import GetSystemMetrics
from threading import Thread

import json

import database_access as dba
import user_creation_and_manip as ucm
import coords_creation_and_manip as ccm
import config

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy_garden.mapview import MapView, MapMarker

WIDTH = 1000
HEIGHT = 1000

Window.size = (WIDTH, HEIGHT)
Window.top = 40 + max(GetSystemMetrics(1) // 2 - 540, 0)
Window.left = GetSystemMetrics(0) // 2 - 500


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
                if key == dba.user_keys[6]:
                    new_coords = str(val.text).split(sep=";")
                    data_dict[str(key)] = (float(new_coords[0]), float(new_coords[1]))
                elif key == dba.user_keys[3] and not ucm.check_email(str(val.text)):
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
            marker = MapMarker(lon=coord[1], lat=coord[0],
                               source=os.path.join("coords", "start_point.png"))
            super().add_marker(marker)
            counter += 1

        counter = 0
        for coord in ccm.give_end_points():
            marker = MapMarker(lon=coord[1], lat=coord[0],
                               source=os.path.join("coords", "end_point.png"))
            super().add_marker(marker)
            counter += 1

    pass


class CreatePathThread(Thread):
    def __init__(self, threadId, func, user_id):
        Thread.__init__(self)
        self.threadId = threadId
        self.exit_flag = True
        self.func = func
        self.user_id = user_id

    def run(self) -> None:
        print(f"Starting thread id {self.threadId}\n", end="")
        while self.exit_flag:
            try:
                self.func(self.user_id)
            except:
                print(f"Exiting thread id {self.threadId}\n", end="")
                self.exit_flag = not self.exit_flag


class PopSimMapView(MapView):
    # In MapView:
    # Lon, Lat
    # In Google API's
    # Lat, Lon
    def __init__(self):
        super().__init__()
        users_json_str = json.dumps(dba.get_all_users('json'))
        users_data_firebase = pd.read_json(StringIO(users_json_str)).transpose()
        self.user_paths = {}

        for index, row in users_data_firebase.iterrows():
            if str(index).find("-") != -1:
                random_path = ccm.get_random_path()
                self.user_paths[index] = random_path

        for key in self.user_paths.keys():
            self.user_paths[key] = self.user_paths[key][::-1]

        self.user_ids = []
        for user_id in self.user_paths.keys():
            self.user_ids.append(user_id)

        self.markers = {}
        for user_id in self.user_ids:
            self.markers[user_id] = MapMarker(lon=self.user_paths[user_id][-1][1], lat=self.user_paths[user_id][-1][0],
                                              source=os.path.join("coords", "end_point.png"))
            super().add_marker(self.markers[user_id])
        self.create_paths()

    def create_paths(self):
        counter = 0
        for user_id in self.user_ids:
            thread = CreatePathThread(counter, self.create_path, user_id)
            thread.start()
            counter += 1

    def create_path(self, user_id):
        while True:
            coords = self.user_paths[user_id].pop()
            super().remove_marker(self.markers[user_id])
            self.markers[user_id].lat = coords[0]
            self.markers[user_id].lon = coords[1]
            super().add_marker(self.markers[user_id])
            dba.update_user_coords(user_id, coords)
            sleep(config.interval)

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
