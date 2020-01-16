# import argparse

from sys import stdin
from json import dumps


key_tuple = tuple(stdin.read().split(''))
data_dict = dict()

for key in key_tuple:
    data_dict[key] = []

for line in stdin:
    data = line.split('')
    for i in range(len(key_tuple)):
        curr_key = key_tuple[i]
        data_dict[curr_key] = data[i]

print(dumps(data_dict))

