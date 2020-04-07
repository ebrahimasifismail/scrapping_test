"""
Util Module
+++++++++++++

Utility functions that might be used in worker implementations
"""

from functools import reduce
import operator


def get_non_empty_lines(input_str):
    "Split input string to lines and only return non-empty lines"

    return [line for line in ensure_string(input_str).split('\n') if line.strip() != '']


def ensure_string(input_bytes_or_str):
    "Converts bytes to string, if it's already a string, does nothing"

    if isinstance(input_bytes_or_str, bytes):
        return input_bytes_or_str.decode('utf-8')

    return input_bytes_or_str


def ensure_bytes(input_bytes_or_str):
    "Converts string to bytes, if input is already bytes, does nothing"

    if not isinstance(input_bytes_or_str, bytes):
        return input_bytes_or_str.encode('utf-8')

    return input_bytes_or_str


def is_in_dict(d, keys_list):
    """
    Given a list of nested keys determines if all of them exist. Serves as a short-hand
    for avoiding multiple if conditions to check for all the keys
    """

    current = d
    for key in keys_list:
        if key not in current:
            return False

        current = current[key]

    return True


def get_from_dict(data_dict, map_list):
    return reduce(operator.getitem, map_list, data_dict)


def set_in_dict(data_dict, map_list, value):
    get_from_dict(data_dict, map_list[:-1])[map_list[-1]] = value


def dict_set_if_exists(dd, d_key, sd, s_keys):
    """
    Set an item in dictionary dd with key set as d_key if s_keys exist in sd
    """

    if is_in_dict(sd, s_keys):
        dd[d_key] = get_from_dict(sd, s_keys)


def hex_to_str(hex_str):
    "Convert a hex string to it's string/binary representation"

    hex_str = hex_str.replace(' ', '')
    assert len(hex_str) % 2 == 0

    out_str = ''
    for i in range(0, len(hex_str), 2):
        hex_code = hex_str[i:i+2]
        out_str += chr(int(hex_code, base=16))

    return out_str


def str_to_hex(in_str):
    "Convert a string to hex representation"

    hex_str = ''
    for ch in in_str:
        hex_str += hex(ord(ch))[2:].rjust(2, '0')

    return hex_str
