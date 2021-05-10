from datetime import date
from random import randint, uniform
from collections import OrderedDict


class Tag:
    def __init__(self, name: str, author: str = "EmulationApp",
                 creation_date: str = str(date.today()), users=None):
        self.author = author
        self.name = name.replace("#", "")
        self.creation_date = creation_date
        self.users = users

    def insert_user(self, user):
        if self.users is None:
            self.users = []
        if user not in self.users:
            self.users.append(user)
            return True
        return False

    def delete_user(self, user):
        if user in self.users:
            self.users.remove(user)
            return True
        return False

    def create_firebase_entry(self):
        data = {
            "Name": self.name.replace("#", ""),
            "Author": self.author,
            "Creation_date": str(self.creation_date),
            "Users": self.users
        }
        # print(data)
        return data

    def __repr__(self):
        return_string = f"{self.name}\n\tCreation date: {self.creation_date}\n\tAuthor: {self.author}\n\t" \
                        f"Active users: {self.users}\n"
        return return_string


def mark_random_tags(given_list_of_tags):
    ord_dict = OrderedDict()
    for tag in given_list_of_tags:
        random = uniform(0, 1)
        ord_dict[tag] = random

    sorted_ord_dict_list = sorted(ord_dict.items(), key=lambda x: x[1], reverse=True)

    return_tag_list = []

    for tag_name in sorted_ord_dict_list[0:5]:
        return_tag_list.append(tag_name[0].replace("#", ""))

    return return_tag_list


def create_tags(num_of_tags: int, list_of_user_ids: list):
    """Max amount of tags is the max amount of line from custom_tags.txt min is 1"""
    custom_tag_names = open("custom_tags.txt").read().splitlines()

    if num_of_tags < 1 or num_of_tags > len(custom_tag_names):
        raise Exception("num_of_tags cannot be < 1 or > len(custom_tags.txt)")

    list_of_tags = []
    for tag_name in custom_tag_names[0:num_of_tags]:
        list_of_tags.append(Tag(tag_name))

    updated_users_dict = {}
    for user_id in list_of_user_ids:
        updated_users_dict[user_id] = {}

    for val in updated_users_dict.values():
        val["Current_used_tags"] = []

    for user_id in list_of_user_ids:
        rand_tags = mark_random_tags(custom_tag_names[0:num_of_tags])
        for tag in list_of_tags:
            if tag.name.replace("#", "") in rand_tags:
                tag.insert_user(user_id)
                updated_users_dict[user_id]["Current_used_tags"].append(tag.name.replace("#", ""))

    return list_of_tags, updated_users_dict


def create_tags_dict(num_of_tags: int, list_of_user_ids: list):
    created_tags, updated_users_dict = create_tags(num_of_tags, list_of_user_ids)

    firebase_dict = {}

    for tag in created_tags:
        firebase_dict[tag.name.replace("#", "")] = tag.create_firebase_entry()

    return firebase_dict, updated_users_dict


# user_ids = []
# for x in range(10):
#     user_ids.append(x)
#
# for item in create_tags_dict(user_ids).items():
#     print(item)
