from datetime import date
from random import randint


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

    for tag in list_of_tags:
        for user_id in list_of_user_ids:
            if randint(0, 100) < 40:
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
























































# from datetime import date
# from random import randint
#
#
# # class representing a single tag - creation date and author are optional
# # class Tag(object):
# #     def __init__(self, name, author: str = None, creation_date: str = None):
# #         super().__init__()
# #         self.name = name
# #         if creation_date is None:
# #             self.creation_date = str(date.today())
# #         else:
# #             self.creation_date = creation_date
# #         self.author = author
# #
# #     def __str__(self):
# #         return f"{self.name}"
#
#
# # used for a collection of tags - an internal class passed to Firebase
# class Tags:
#     def __init__(self, tags_filename="custom_tags.txt"):
#         self.tag_dict = {}
#         self.tag_names_list: list = None
#         try:
#             self.tag_names_list = []
#             tag_names_file = open(tags_filename).read().splitlines()
#
#             for tag_name in tag_names_file:
#                 self.tag_names_list.append(tag_name.replace('#', ''))
#
#             for tag_name in self.tag_names_list:
#                 self.tag_dict[tag_name] = {
#                     'Name': tag_name,
#                     'Author': 'EmulationApp',
#                     'Creation_date': str(date.today()),
#                     'Users': []
#                 }
#         except:
#             raise Exception("Incorrect tag names file path")
#             pass
#
#     def __str__(self):
#         return_string = ""
#         counter = 0
#         for key, val in self.tag_dict.items():
#             return_string += f"[{counter}] Users using tag '#{key}':\n"
#             counter += 1
#             for user_id in val:
#                 return_string += f'\t=> {user_id}\n'
#         if return_string == "":
#             return "Tags is empty"
#         return return_string
#
#     # inserts user or a list of users into a specified tag
#     def insert_user_or_users(self, tag_name, user_or_users):
#         if tag_name not in self.tag_dict.keys():
#             return False
#         else:
#             if user_or_users is list:
#                 for user in user_or_users:
#                     if user not in self.tag_dict[tag_name]['Users']:
#                         self.tag_dict[tag_name]['Users'].append(user)
#             elif user_or_users is not list:
#                 if user_or_users not in self.tag_dict[tag_name]['Users']:
#                     self.tag_dict[tag_name]['Users'].append(user_or_users)
#             return True
#
#     # inserts a new tag into a dictionary
#     def insert_tag(self, tag_name, tag_author: str = None, tag_creation_date: date = None):
#         if tag_name not in self.tag_dict.keys():
#             self.tag_dict[tag_name] = {
#                 'Name': tag_name,
#                 'Author': tag_author,
#                 'Creation_date': str(tag_creation_date),
#                 'Users': []
#             }
#             self.tag_names_list.append(tag_name)
#             return True
#         return False
#
#     def delete_tag(self, tag_name):
#         if tag_name not in self.tag_dict.keys():
#             return False
#         self.tag_dict.pop(tag_name)
#         return True
#
#     # inserts users from a given list randomly to random tags
#     # for testing purposes
#     def insert_randomly(self, users):
#         for user in users:
#             print(user)
#             for key in self.tag_dict.keys():
#                 if randint(0, 1):
#                     self.insert_user_or_users(key, user)
#
#     # return a list of matched users who are using the same tags
#     def find_matches(self, user_id, user_tags):
#         if user_tags:
#             tag_dict = self.tag_dict
#
#             while user_tags[0] not in tag_dict.keys():
#                 raise Exception("Cannot compare users with tags that do not exist")
#
#             # have to do it this way because list __eq__ assigns the same id to the new object
#             matching_users = []
#             for val in tag_dict[user_tags[0]]:
#                 matching_users.append(val)
#
#             for tag in user_tags:
#                 if tag in tag_dict.keys():
#                     # have to do it this way because list __eq__ assigns the same id to the new object
#                     comp_users = []
#                     for val in tag_dict[tag]:
#                         comp_users.append(val)
#
#                     for user in comp_users:
#                         if user not in matching_users:
#                             comp_users.remove(user)
#
#                     for user in matching_users:
#                         if user not in comp_users:
#                             matching_users.remove(user)
#
#             if user_id in matching_users:
#                 matching_users.remove(user_id)
#             return matching_users
#
#     def create_database_entry(self):
#         data = self.tag_dict
#         return data
#
# # tags = Tags()
# #
# # tags.insert('bar', '123')
# # tags.insert('bar', '456')
# # tags.insert('kino', '789')
# # tags.insert('kino', '101112')
# # tags.insert('sprzedam_opla', '131415')
# # tags.insert('sprzedam_opla', '161718')
# # tags.insert('yolo', '1111111')
# #
# # user_tags = ['kino', 'bar']
# #
# # print(tags.find_full_matching_users(user_tags, '123'))
# #
# # tags.insert('A', [1, 2, 3, 4, 5])
# # tags.insert('B', [2, 3, 4, 5, 6])
# # tags.insert('C', [3, 4, 5, 6, 7])
# # tags.insert('D', [4, 5, 6, 7, 8, 1, 2, 3])
# #
# # tags.print()
# # print(tags.find_matches(4, ['A', 'B', 'C', 'D']))
# # tags.print()
