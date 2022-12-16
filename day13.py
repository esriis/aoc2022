import numpy as np
from functools import cmp_to_key

file_path = "input/day13.txt"

with open(file_path, mode="r") as f:
    text = f.read()

def parse_lists(packet_list: list) -> list:
    max_iter = 100
    iter = 0
    brackets_gone = all(["[" not in element for element in packet_list])
    while (not brackets_gone) and iter < max_iter:
        iter += 1    
        new_list = []
        for element in packet_list:
            if isinstance(element, list):
                new_list.extend(parse_lists(element))
            elif isinstance(element, str):
                # find any outer [
                l_index = next((i for i, letter in enumerate(element) if letter == "["), None)
                if l_index is None:
                    new_list.append(element)
                else:
                    # find mathing ]
                    depth = 1
                    j = l_index+1
                    while j < len(element) and depth > 0:
                        if element[j] == "[":
                            depth += 1
                        elif element[j] == "]":
                            depth -= 1
                        j += 1
                    if depth != 0:
                        raise Exception()
                    r_index = j-1
                    if l_index > 0:
                        new_list.append(element[0:l_index-1])
                    if r_index > l_index+1:
                        new_list.append(parse_lists([element[l_index+1:r_index]]))
                    else:
                        new_list.append([])
                    if r_index+2 < len(element):
                        new_list.extend(parse_lists([element[r_index+2:]]))
            else:
                raise Exception()
        packet_list = new_list
        brackets_gone = all(["[" not in element for element in packet_list])
    if not brackets_gone:
        raise Exception()
    if not isinstance(packet_list, list):
        raise Exception()
    return packet_list
    

def parse_ints(packet_list: list) -> list:
    new_list = []
    for element in packet_list:
        if isinstance(element, list):
            new_list.append(parse_ints(element))
        elif isinstance(element, str):
            if len(element) == 0:
                new_list.append([])
            else:
                new_list.extend([int(number) for number in element.split(",")])
        else:
            raise Exception()
    return new_list


def parse_packet(packet_str: str):
    return parse_ints(parse_lists([packet_str])[0])

def compare(left, right) -> int:
    """
    Returns sign(left-right):
    left > right -> sign = 1
    left = right -> sign = 0
    left < right -> sign = -1
    """
    if isinstance(left, int) and isinstance(right, int):
        sign = np.sign(left-right)
    elif isinstance(left, list) and isinstance(right, list):
        index = 0
        determined = False
        while (not determined) and (index < min(len(left), len(right))):
            sign = compare(left[index], right[index])
            if sign != 0:
                determined = True
            index += 1
        if not determined:
            sign = compare(len(left), len(right))
    elif isinstance(left, int) and isinstance(right, list):
        sign = compare([left], right)
    elif isinstance(left, list) and isinstance(right, int):
        sign = compare(left, [right])
    else:
        raise Exception()
    return sign


pair_str_list = [line.split("\n") for line in text.strip("\n").split("\n\n")]
pairs = [tuple(parse_packet(packet_str) for packet_str in line) for line in pair_str_list]
pair_in_order = [compare(pair[0], pair[1]) <= 0 for pair in pairs]

solution_part1 = sum(i+1 for i, in_order in enumerate(pair_in_order) if in_order)

print(f"Solution to part 1 is {solution_part1}")

"""
Part 2
"""

new_packets = [[[2]],[[6]]]

packet_list = new_packets.copy()
_ = [packet_list.extend(pair) for pair in pairs]


sorted_packet_list = sorted(packet_list, key=cmp_to_key(compare), reverse=False)

indices = [i+1 for i, packet in enumerate(sorted_packet_list) if packet in new_packets]

solution_part2 = indices[0]*indices[1]

print(f"Solution to part 2 is {solution_part2}")