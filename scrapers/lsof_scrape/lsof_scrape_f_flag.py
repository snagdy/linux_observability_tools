from os import path
from sys import stdin
from json import dumps, load


# initialise our list of dictionaries.
list_of_dicts = [{}]
# get the config file's full path and load it into a dictionary for descriptive field name lookups for keys.
directory_of_script = path.dirname(path.realpath(__file__))
file_path = path.join(directory_of_script, 'field_config.json')
with open(file_path) as json_file:
    key_to_field_map = load(json_file)

# while loop that breaks on EOFError or AssertionError.
while True:
    try:
        # get data line, one at a time, removing trailing newlines.
        data_line = stdin.readline().rstrip()
        # check that the line is not blank, should not be any with lsof -F output.
        assert len(data_line) > 0
        # get our raw key and then lookup a descriptive name to use as the key instead.
        raw_key = data_line[0]
        key =  key_to_field_map[raw_key]
        # some fields are blank, and have one byte representing the key only, we create blank dict vals for these.
        if len(data_line) > 1:
            value = data_line[1:]
        else:
            value = ''
        # we add a new key value pair to the last item in our list of dictionaries.
        list_of_dicts[-1][key] = value
        # when our raw key is an 'n', we have reached the end of this record since the last item is always filename.
        # this appends a new dictionary which will be used as the new last item on the next iteration.
        if raw_key == 'n':
            new_dict = {}
            list_of_dicts.append(new_dict)
    # break when our exceptions are triggered, indicating the end of the file / STDIN file object has been reached.
    except AssertionError:
        break

# we convert the output to a dictionary of dictionaries for proper JSON conversion, removing the last always blank item.
dict_of_dicts = {key: value for key, value in enumerate(list_of_dicts[:-1])}
print(dumps(dict_of_dicts))
