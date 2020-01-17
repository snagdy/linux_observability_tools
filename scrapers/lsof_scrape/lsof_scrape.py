# import argparse

from pprint import pprint
from sys import stdin
from json import dumps


key_tuple = tuple(stdin.readline().split())
data_dict = dict()

for key in key_tuple:
    data_dict[key] = []

for line in stdin:
    data = line.split()
    print(data)
    for i in range(len(key_tuple)-1):
        curr_key = key_tuple[i]
        print(curr_key)
        data_dict[curr_key].append(data[i])

pprint(data_dict)

