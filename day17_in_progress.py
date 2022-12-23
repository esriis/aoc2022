import numpy as np

file_path = "input/day17.txt"

VERBOSE = False

with open(file_path, mode="r") as f:
    text = f.read()

directions = list(text.splitlines()[0])

rocks = [
    np.array([(x, 0) for x in range(4)]),
    np.array([
        (x, y) for x in range(3) for y in range(3)
        if not all([x in [0,2], y in [0,2]])
    ]),
    np.array([
        (x, y) for x in range(3) for y in range(3)
        if (y == 0) or (x == 2)
    ]),
    np.array([(0, y) for y in range(4)]),
    np.array([(x,y) for x in range(2) for y in range(2)])
]

def print_array(array):
    print()
    for y in reversed(range(array.shape[1])):
        print(" ".join(array[:,y]))
    print()

offset = (2, 3)
width  = 7
actual_height = 0
height = 0

num_rocks = 2022

chamber = np.array([["."]*height]*width)

counter = 0
counter2 = counter

def shift_rock(rock, direction, chamber: np.ndarray):
    if direction == "<":
        dir_str = "left"
        move = (-1, 0)
    elif direction == ">":
        dir_str = "right"
        move = (1, 0)
    else:
        raise Exception()
    new_rock = rock + move
    if (
        all(ind in range(chamber.shape[0]) for ind in new_rock[:, 0])
        and (chamber[new_rock[:,0], new_rock[:,1]] == ".").all()
    ):
        rock = new_rock
        success = True
    else:
        success = False
    if VERBOSE:
        if success:
            print(f"Pushes {dir_str}")
        else:
            print(f"Tries to push {dir_str} but fails")
    return rock


tracking = []

for i in range(100*num_rocks): #num_rocks
    prev_counter = counter
    if (i+1) % 200 == 0:
        print(f"Handling rock number {i+1}")
        # print(height)
    if VERBOSE:
        print("________________")
        print(f"Step {i+1}")
        print("________________")
    i2 = i % len(rocks)
    rock = rocks[i2].copy()
    rock_height = rock[:,1].max()+1
    chamber = np.concatenate(
        (
            chamber,
            np.array([["."]*(height+rock_height+offset[1]-chamber.shape[1])]*width)
        ),
        axis=1
    )
    rock = (rock + offset) + (0,height)
    if VERBOSE:
        tmp_chamber = chamber.copy()
        tmp_chamber[rock[:,0], rock[:,1]] = "@"
        print_array(tmp_chamber)
        print()
    rock = shift_rock(rock=rock, direction=directions[counter2], chamber=chamber)
    if VERBOSE:
        tmp_chamber = chamber.copy()
        tmp_chamber[rock[:,0], rock[:,1]] = "@"
        print_array(tmp_chamber)
        print()
    counter += 1
    counter2 = counter % len(directions)
    next_move = rock + (0,-1)
    while (
        all(ind in range(chamber.shape[0]) for ind in next_move[:, 0])
        and (next_move[:,1].min() >= 0)
        and (chamber[next_move[:,0], next_move[:,1]] == ".").all()
    ):
        if VERBOSE:
            print("moves down")
        rock = next_move
        
        if VERBOSE:
            tmp_chamber = chamber.copy()
            tmp_chamber[rock[:,0], rock[:,1]] = "@"
            print_array(tmp_chamber)
            print()
        rock = shift_rock(rock=rock, direction=directions[counter2], chamber=chamber)
        tmp_chamber = chamber.copy()
        tmp_chamber[rock[:,0], rock[:,1]] = "@"
        if VERBOSE:
            print_array(tmp_chamber)
            print()
        counter += 1
        counter2 = counter % len(directions)
        next_move = rock + (0,-1)
    chamber[rock[:,0], rock[:,1]] = "#"
    actual_height += max(0, max(rock[:,1])+1 - height)
    height = max(height, max(rock[:,1])+1)
    level = rock[:,1].max()
    while any(chamber[:, level] != "#") and level >= rock[:,1].min():
        level -= 1
    if level >= rock[:,1].min():
        # print_array(chamber)
        chamber = chamber[:, level+1:]
        height -= level+1
        if (
            (chamber[2, 0:6] == "#").all()
            and ((chamber == "#").sum() == 6)
        ):
            print(i)
            print_array(chamber)
            print(actual_height)
            tracking.append(actual_height)
            print(tracking)
    
    if VERBOSE:
        print()
        print(f"Final result for step {i+1}")
        print()
        print_array(chamber)
        print(f"Height = {height}")
    if (
        ((i+1) % len(rocks) == 0)
        and ((counter+1) % len(directions) == 0)
    ):
        print(f"YES! {i} {counter}")
    # print(f"Rock {i} ({i2}), counter {counter} ({counter2}), diff {counter-prev_counter}")
    
solution_part1 = actual_height

print(f"Solution to part 1: {solution_part1}")

# print(height)
# print_array(chamber)
