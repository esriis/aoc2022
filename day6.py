file_path = "input/day6.txt"

def find_marker(buffer: str, num_distinct_chars: int):
    start = 0
    position = 1
    mark_found = False

    while (not mark_found) & (position < len(buffer)):
        try:
            index = buffer[start:position].index(buffer[position])
            start = start+index+1
            position += 1
        except ValueError:
            if position-start+1 >= num_distinct_chars:
                mark_found = True
            else:
                position += 1
    return mark_found, position

with open(file_path, mode="r") as f:
    text = f.read()

buffer = text.strip("\n")

mark_found, position = find_marker(buffer=buffer, num_distinct_chars=4)

if mark_found:
    solution_part1 = position+1
    print(f"Solution to part 1: {solution_part1}")
else:
    print("No solution found to part 1")


mark_found, position = find_marker(buffer=buffer, num_distinct_chars=14)

if mark_found:
    solution_part2 = position+1
    print(f"Solution to part 2: {solution_part2}")
else:
    print("No solution found to part 2")

