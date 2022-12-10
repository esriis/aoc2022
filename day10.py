file_path = "input/day10.txt"

with open(file_path, mode="r") as f:
    text = f.read()

lines = text.splitlines()

delay = 2

def line_to_dx(line: str):
    dx_str = line[5:]
    return [0, int(dx_str)] if len(dx_str) > 0 else [0]

dx_vec = []
_ = [dx_vec.extend(line_to_dx(line)) for line in lines]
X = [1]
for dx in dx_vec:
    X.append(X[-1]+dx)

cycles = [20, 60, 100, 140, 180, 220]

solution_part1 = sum([X[cycle-1]*cycle for cycle in cycles])

print(f"The solution to part 1: {solution_part1}")

"""
Part 2
"""

sprite_width = 3

CRT_width = 40
CRT_height = 6
CRT_len = CRT_width*CRT_height

CRT_flat = ["."]*CRT_len

for cycle in range(CRT_len):
    if abs(X[cycle] - ((cycle) % CRT_width)) <= 1:
        CRT_flat[cycle] = "#"

print("CRT:")
for i in range(CRT_height):
    print("".join(CRT_flat[i*CRT_width:(i+1)*CRT_width]))
