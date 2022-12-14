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

pair_str_list = [line.split("\n") for line in text.strip("\n").split("\n\n")]

in_order = 0

for pair in pair_str_list:
    for packet_str in pair:
        result = parse_packet(packet_str)
        str_final = str(result).replace(" ", "")
        if str_final != packet_str:
            raise Exception()
        else:
            print("Fine!")

def in_order_inner(left, right):
    determined = False
    for left_val, right_val in zip(left, right):
        if left_val == right_val:
            pass
        else:
            if isinstance(left_val, int) & isinstance(right_val, int):
                determined = True
                result = left_val < right_val
            else:
                if isinstance(left_val, int) & isinstance(right_val, list):
                    determined, result = in_order_inner([left_val], right_val)
                elif isinstance(left_val, list) & isinstance(right_val, int):
                    determined, result = in_order_inner(left_val, [right_val])
                else:
                    raise Exception()
            if determined:
                return determined, result
    return determined, None

def in_order(left, right):
    determined, result = in_order_inner(left, right)
    if not determined:
        return True
    else:
        return result