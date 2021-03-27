import uuid

dict_of_ids = {}

print(uuid.uuid4())

# for key in range(0, 100000000):
#     dict_of_ids[uuid.uuid4()] = 0
#
# print(len(dict_of_ids.keys()))


def test_kwargs(numer, *args, **kwargs):
    for key, value in kwargs.items():
        print("{}: {}".format(key, value))


test_kwargs(3, name="dupa", surname="romana")
