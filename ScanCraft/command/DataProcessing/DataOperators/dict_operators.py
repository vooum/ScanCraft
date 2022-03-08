#!/usr/bin/env python3


def Change_key_type(dictionary: dict, new_type: type, layers: list = range(1000), cur_layer: int = 0) -> dict:
    new_dict = {}
    if cur_layer > 1000:  # maybe something wrong
        print('this dict has more than 1k layers, check it.')
        exit()
    for k, v in dictionary.items():
        if type(v) is dict:
            v = Change_key_type(dictionary=v, new_type=new_type,
                                layers=layers, cur_layer=cur_layer+1)
        if cur_layer in layers:
            k = new_type(k)
        new_dict.update({k: v})
    return new_dict
