from sys import stdin
from datetime import datetime
from json import dumps
from argparse import ArgumentParser
from pandas import DataFrame as df


def process_data(stdin_file_obj, datetime_format, display_option):
    packet_dict_of_dicts = {}
    while True:
        try:
            # read in line and strip trailing whitespace
            current_line = stdin_file_obj.readline().rstrip()
            # print(current_line)

            # check we have not reached the blank line at the end of STDIN
            assert len(current_line) > 0
            # start transforming the string to useful data
            current_line = current_line.split(' ', 1)

            # build datetime object for DataFrame output

            current_date = datetime.today().strftime('%Y-%m-%d')
            line_timestamp = current_line[0]
            time = datetime.strptime(' '.join([current_date, line_timestamp]), datetime_format)

            # build packet dictionary for either JSON or DataFrame output
            packet_details = current_line[1].split(' ', 1)
            network_or_link_protocol, message = packet_details[0], packet_details[1]

            if display_option == 'df':
                packet_dict_of_dicts[time] = {'net_or_link_protocol': network_or_link_protocol, 'message': message}
            elif display_option == 'json':
                time_str = time.strftime(datetime_format)
                packet_dict_of_dicts[time_str] = {'net_or_link_protocol': network_or_link_protocol, 'message': message}

        except AssertionError:
            break
    return packet_dict_of_dicts


def display_data(packet_dict_of_dicts, display_option):
    if display_option == 'df':
        packet_dict_for_df = packet_dict_of_dicts
        packet_df = df(packet_dict_for_df)
        print(packet_df)
    elif display_option == 'json':
        packet_dict_for_json = packet_dict_of_dicts
        packet_json = dumps(packet_dict_for_json)
        print(packet_json)


def main():
    parser = ArgumentParser()
    parser.add_argument('infile', nargs='?', type=str, default=stdin,
                        help='Pass this file in via a STDIN pipe.')
    parser.add_argument('--display-option', nargs='?', type=str, default='json',
                        help='Specify "json" or "df" for JSON and DataFrame respectively. Default is "json".')
    inputs = parser.parse_args()

    file_obj = inputs.infile
    display_opt = inputs.display_option
    datetime_fmt = '%Y-%m-%d %H:%M:%S.%f'

    packet_dict_of_dicts = process_data(stdin_file_obj=file_obj,
                                        datetime_format=datetime_fmt,
                                        display_option=display_opt)

    display_data(packet_dict_of_dicts=packet_dict_of_dicts,
                 display_option=display_opt)

if __name__ == '__main__':
    main()
