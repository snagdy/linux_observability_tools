import pandas as pd
import argparse

from os import path
from sys import stdin
from json import dumps, load


def load_key_to_field_map(field_map_config_file_path, full_path=False):
    # get the config file's full path and load it into a dictionary for descriptive field name lookups for keys.
    if not full_path:
        directory_of_script = path.dirname(path.realpath(__file__))
        file_path = path.join(directory_of_script, field_map_config_file_path)
    else:
        file_path = field_map_config_file_path
    with open(file_path) as json_file:
        return load(json_file)


def get_key_val_pair(lsof_data_string, field_lookup_table):
    raw_key = lsof_data_string[0]
    key = field_lookup_table[raw_key]
    if len(lsof_data_string) > 1:
        value = lsof_data_string[1:]
    else:
        value = ''
    return raw_key, key, value


def convert_data_lines_to_list_of_dicts(input_file_object, field_lookup_table):
    # initialise our list of dictionaries.
    list_of_dicts = [{}]
    # while loop that breaks on AssertionError.
    while True:
        try:
            # get data line, one at a time, removing trailing newlines.
            data_line = input_file_object.readline().rstrip()
            # check that the line is not blank, should not be any with lsof -F output.
            assert len(data_line) > 0
            # get our raw key and then lookup a descriptive name to use as the key instead.
            raw_key, key, value = get_key_val_pair(data_line, field_lookup_table)
            # we add a new key value pair to the last item in our list of dictionaries.
            list_of_dicts[-1][key] = value
            # when our raw key is an 'n', we have reached the end of this record since the last item is always filename.
            # this appends a new dictionary which will be used as the new last item on the next iteration.
            if raw_key == 'n':
                new_dict = {}
                list_of_dicts.append(new_dict)
        # the last line of STDIN input seems to have a blank, so this will also terminate processing.
        # no blank lines are expected in the middle of the input, but if so, this will also break.
        # this is a trade-off between memory efficiency for large inputs and handling completely unexpected exceptions.
        # workaround would require loading more lines, i.e. using a rolling buffer, and impacts performance somewhat.
        except AssertionError:
            break
    return list_of_dicts


def convert_list_of_dicts_to_dict_of_dicts(list_of_dictionaries):
    # we convert the output to a dictionary of dictionaries for proper JSON conversion.
    # we remove the trailing blank dict if we have at least two dicts.
    if len(list_of_dictionaries) > 1:
        return {key: value for key, value in enumerate(list_of_dictionaries[:-1])}
    else:
        return {key: value for key, value in enumerate(list_of_dictionaries)}


def print_to_stdout(dict_of_dictionaries, display_option):
    if display_option == 'json':
        print(dumps(dict_of_dictionaries))
    elif display_option == 'df':
        print(pd.DataFrame(dict_of_dictionaries))


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('cfg_file_name', nargs='?', type=str,
                        help='''REQUIRED: Pass file name of the field lookup config JSON file in script directory, 
                        else use full file path and set "full_cfg_file_path" optional argument to 1 instead.''')

    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=stdin,
                        help='''REQUIRED: This is by default the data passed in using STDIN for which a file object is 
                        created.''')

    parser.add_argument('-full_cfg_file_path', nargs='?', type=int, default=0,
                        help='''Set to 1 when field lookup config JSON file is not in the script directory, supply
                        the full file path to "cfg_file_name". Default is 0.''')

    parser.add_argument('-display_option', nargs='?', type=str, default='json',
                        help='''Pass either "json" or "df" to get output to STDOUT as JSON or a pandas.DataFrame 
                        object. Default is "json".''')
    inputs = parser.parse_args()

    use_full_path = inputs.full_cfg_file_path
    config_file_path = inputs.cfg_file_name
    stdin_file_object = inputs.infile
    display_option = inputs.display_option

    if use_full_path:
        field_name_lookup_table = load_key_to_field_map(config_file_path, full_path=True)
    else:
        field_name_lookup_table = load_key_to_field_map(config_file_path)

    list_of_dicts = convert_data_lines_to_list_of_dicts(stdin_file_object, field_name_lookup_table)
    dict_of_dicts = convert_list_of_dicts_to_dict_of_dicts(list_of_dicts)
    print_to_stdout(dict_of_dicts, display_option)
    return 0


if __name__ == '__main__':
    main()
