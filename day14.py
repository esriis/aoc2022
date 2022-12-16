import numpy as np

file_path = "input/day14.txt"

with open(file_path, mode="r") as f:
    text = f.read()

def parse_coords(text: str):
    lines = text.splitlines()
    coords_str = [line.split(" -> ") for line in lines]
    coords = [[tuple(int(value) for value in coord.split(",")) for coord in line] for line in coords_str]
    return coords

def get_ranges_and_offset(
    coords: list,
    rock_source: tuple,
    pad_x: int,
    pad_y: int
):
    coords_list = [rock_source]
    _ = [coords_list.extend(coord) for coord in coords]
    min_x = min(coord[0] for coord in coords_list)-pad_x
    min_y = min(coord[1] for coord in coords_list)
    max_x = max(coord[0] for coord in coords_list)+pad_x
    max_y = max(coord[1] for coord in coords_list)+pad_y
    x_range = np.array([min_x, max_x])
    y_range = np.array([min_y, max_y])
    offset = np.array([min_x-1, min_y])
    return x_range, y_range, offset

def build_scan(
    coords: list,
    x_range: np.ndarray,
    y_range: np.ndarray,
    offset: np.ndarray
) -> np.ndarray:
    # pad x on both sides and y on one side 
    scan = np.array([["."]*(y_range[1]-y_range[0]+1)]*(x_range[1]-x_range[0]+1))
    for path in coords:
        for step in range(len(path)-1):
            start = path[step]-offset
            end = path[step+1]-offset
            diff = end - start
            direction = np.sign(diff)
            length = np.abs(diff).max()+1
            for i in range(length):
                scan[tuple(start+i*direction)] = "#"
    return scan

def drop_rock(scan, rock_source, offset):
    rock_position = rock_source - offset
    rolling_rock = True
    abyss_reached = False
    source_clogged = scan[tuple(rock_source-offset)] != "."
    while rolling_rock and (not abyss_reached) and (not source_clogged):
        if rock_position[1]+1 == scan.shape[1]:
            abyss_reached = True
        elif scan[tuple(rock_position+(0,1))] == ".":
            rock_position += (0,1)
        elif scan[tuple(rock_position+(-1,1))] == ".":
            rock_position += (-1,1)
        elif scan[tuple(rock_position+(1,1))] == ".":
            rock_position += (1,1)
        else:
            scan[tuple(rock_position)] = "o"
            rolling_rock = False
    return scan, abyss_reached, source_clogged

"""
Part 1
"""

coords = parse_coords(text)
rock_source = (500,0)
x_range, y_range, offset = get_ranges_and_offset(coords, rock_source, pad_x=1, pad_y=1)

scan = build_scan(
    coords=coords,
    x_range=x_range,
    y_range=y_range,
    offset=offset
)


abyss_reached = False
rocks_dropped = 0
max_rocks = 10_000
while (not abyss_reached) and (rocks_dropped < max_rocks):
    rocks_dropped += 1
    scan, abyss_reached, _ = drop_rock(
        scan=scan,
        rock_source=rock_source,
        offset=offset
    )

solution_part1 = rocks_dropped - 1

print(f"Solution to part 1 is: {solution_part1}")

"""
Part 2
"""

_, test_y_range, _ = get_ranges_and_offset(coords, rock_source, pad_x=1, pad_y=2)

x_range, y_range, offset = get_ranges_and_offset(
    coords,
    rock_source,
    pad_x=test_y_range[1]-test_y_range[0],
    pad_y=2
)

scan = build_scan(
    coords=coords,
    x_range=x_range,
    y_range=y_range,
    offset=offset
)
scan[:,-1] = "#"

abyss_reached = False
source_clogged = False
rocks_dropped = 0
max_rocks = 100_000
while (not abyss_reached) and (not source_clogged) and (rocks_dropped < max_rocks):
    if rocks_dropped % 500 == 0:
        print(f"Rocks dropped: {rocks_dropped}.")
    rocks_dropped += 1
    scan, abyss_reached, source_clogged = drop_rock(
        scan=scan,
        rock_source=rock_source,
        offset=offset
    )

solution_part2 = rocks_dropped - 1

print(f"Solution to part 2 is: {solution_part2}")