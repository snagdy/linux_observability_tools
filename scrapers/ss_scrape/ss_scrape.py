from sys import stdin
from argparse import ArgumentParser
from json import dumps
from pandas import DataFrame


def parse_headers(header_string):
    # split the header string and remove trailing whitespace characters, add extra header for extra info.
    header_list = header_string.rstrip().split()
    # handling headers with spaces using slice reassignment.
    local_addr_start_index = header_list.index('Local')
    header_list[local_addr_start_index: local_addr_start_index + 2] = \
    [' '.join(header_list[local_addr_start_index: local_addr_start_index + 2])]

    peer_addr_start_index = header_list.index('Peer')
    header_list[peer_addr_start_index: peer_addr_start_index + 2] = \
    [' '.join(header_list[peer_addr_start_index: peer_addr_start_index + 2])]

    return header_list


def process_data_lines(data_line_string, headers):
    # split the data line string, remove trailing whitespace, returns dict.
    raw_data_line_list = data_line_string.rstrip().split()

    # handle slightly different local and peer port data on u_* Netid lines.
    if raw_data_line_list[0][0] == 'u':
        raw_data_line_list[4:6] = [':'.join(raw_data_line_list[4:6])] # local port data merge.
        raw_data_line_list[5:7] = [':'.join(raw_data_line_list[5:7])] # peer port data merge.

    # handle extra output where it has internal whitespace.
    data_len = len(raw_data_line_list)
    header_len = len(headers)
    diff = data_len - header_len

    if diff > 0:
        # collect extra elements into last list element by reassigning slice.
        raw_data_line_list[-diff:] = [' '.join(raw_data_line_list[-diff:])]
    else: # if there are less data items than headers, discard line as "bad data" line.
        return None


    new_headers = headers + ['extra information']
    data_dict = {key: val for key, val in zip(new_headers, raw_data_line_list)}
    return data_dict


def parse_ss_data(stdin_file_object):
    # get headers, then readline while loop through stdin file object to parse data and build dict of dicts.
    headers = parse_headers(stdin_file_object.readline())
    dict_of_dicts = dict()

    current_item_index_key = 0
    while True:
        try:
            current_data_line = stdin_file_object.readline()
            assert len(current_data_line) > 0 # check if this is a blank line, blank lines indicate end of input.
            current_data_dict = process_data_lines(current_data_line, headers=headers)

            if current_data_dict is None: # if we encounter a "bad data" line, we go to the next iteration.
                continue

            dict_of_dicts[current_item_index_key] = current_data_dict
            current_item_index_key += 1
        except AssertionError:
            break
    return dict_of_dicts


def display_to_stdout(dictionary_of_dicts, display_option):
    if display_option == 'json':
        print(dumps(dictionary_of_dicts))
    elif display_option == 'df':
        print(DataFrame(dictionary_of_dicts))


def main():
    parser = ArgumentParser()
    parser.add_argument('infile', nargs='?', type=str, default=stdin,
                        help='Provide the data via a STDIN pipe.')
    parser.add_argument('-display_option', nargs='?', type=str, default='json',
                        help='Specify JSON "json" or pandas.DataFrame "df" as output. Default is "json".')
    inputs = parser.parse_args()
    data_dict_of_dicts = parse_ss_data(inputs.infile)
    display_to_stdout(data_dict_of_dicts, inputs.display_option)


if __name__ == '__main__':
    main()
