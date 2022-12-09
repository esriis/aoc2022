import numpy as np

file_path = "input/day9.txt"

with open(file_path, mode="r") as f:
    text = f.read()

instructions = [
    (line[0], int(line[2:])) for line in 
    text.strip("\n").split("\n")
]

s = np.array([[0, 0]])

tail_pos = s
head_pos = s

tail_positions = tail_pos

head_movements = {"U": np.array([0, 1]), "D": np.array([0, -1]), "L": np.array([-1, 0]), "R": np.array([1, 0])}

def move_tail_pos(tail_pos, head_pos):
    distance = head_pos - tail_pos
    if np.abs(distance).max() >= 2:
        tail_pos = tail_pos + np.sign(distance)
    return tail_pos

for direction, steps in instructions:
    dv = head_movements[direction]
    for _ in range(steps):
        head_pos = head_pos+dv
        tail_pos = move_tail_pos(tail_pos, head_pos)
        tail_positions = np.append(tail_positions, tail_pos, axis=0)

solution_part1 = len(np.unique(tail_positions, axis=0))
print(f"Solution to part 1: {solution_part1}")

"""
Part 2
"""

num_knots = 10
knots = [s]*num_knots
tail_positions = s


for direction, steps in instructions:
    dv = head_movements[direction]
    for _ in range(steps):
        knots[0] = knots[0]+dv
        for i in range(num_knots-1):
            knots[i+1] = move_tail_pos(knots[i+1], knots[i])
        tail_positions = np.append(tail_positions, knots[-1], axis=0)

solution_part2 = len(np.unique(tail_positions, axis=0))
print(f"Solution to part 2: {solution_part2}")