from collections import Counter
import numpy as np

file_path = "input/day15.txt"

with open(file_path, mode="r") as f:
    text = f.read()

def parse_coordinates(coords: str) -> np.ndarray:
    return np.array([int(value) for value in coords[2:].split(", y=")])

def parse_line(line: str) -> np.ndarray:
    pair = tuple(line[10:].split(": closest beacon is at "))
    return tuple(parse_coordinates(coords) for coords in pair)

print("parsing")
pairs = [parse_line(line) for line in text.splitlines()]

y = 2_000_000

def distance(x: np.ndarray, y: np.ndarray):
    return int(np.linalg.norm(x-y, 1))

print("computing distances")
range_list = []
for pair in pairs:
    beacon_distance = distance(pair[0],pair[1])
    vec_distance = abs(pair[0][1]-y)
    gap = beacon_distance - vec_distance
    print(f"sensor: {pair[0][0]:,d}, {pair[0][1]:,d}. beacon: {pair[1][0]:,d}, {pair[1][1]:,d}")
    print(f"vec: {vec_distance:,d}. beac: {beacon_distance:,d}, gap: {gap:,d}")
    if gap >= 0:
        range_list.append((pair[0][0]-gap, pair[0][0]+gap))

print("sorting")
range_list.sort(key=lambda x: [x[0], x[1]])

print("counting")
ruled_out_count = range_list[0][1]-range_list[0][0]+1
running_max = range_list[0][1]
print(f"Current range: [{range_list[0][0]:,d}, {range_list[0][1]:,d}], count: {ruled_out_count:,d}")
for i in range(1, len(range_list)):
    current_range = range_list[i]
    if current_range[1] > running_max:
        ruled_out_count += current_range[1] - max(running_max+1, current_range[0]) + 1
        running_max = current_range[1]
    print(f"Range: [{current_range[0]:,d}, {current_range[1]:,d}], count: {ruled_out_count:,d}")

beacons_on_line = [pair[1][0] for pair in pairs if pair[1][1] == y]
sensors_on_line = [pair[0][0] for pair in pairs if pair[0][0] == y]

solution_part1 = ruled_out_count - len(set(beacons_on_line))

print(f"Solution to part 1: {solution_part1}")

""" 
Part 2
"""

# case 1: It's in a corner:
x_min = 0
y_min = 0
x_max = 4_000_000
y_max = 4_000_000

x_range = [0, 4_000_000]
y_range = [0, 4_000_000]

points = [
    np.array([x,y]) for x in x_range for y in y_range
]

def out_of_range(point: np.ndarray, pairs: list[tuple[np.ndarray]]) -> bool:
    return all([distance(point, pair[0]) > distance(pair[1], pair[0]) for pair in pairs])

beacon = next((point for point in points if out_of_range(point, pairs)), None)

if beacon is None:
    print("Beacon cannot be in a corner.")

intersection_list = []


def get_intersection_left_inner(s2, d1, d2, direction, corner):
    intersections = []
    i = 1
    point = corner
    dist = distance(point, s2)
    gap = dist - d2
    if gap in [0, 1]:
        intersections.append(point)
    i += max(1, abs(gap)//2)
    while i < d1:
        point = corner + i*direction
        dist = distance(point, s2)
        prev_gap = gap
        gap = dist - d2
        if gap in [0, 1]:
            intersections.append(point)
        if (gap == prev_gap) and (abs(gap)//2 <= (d1-i)*1e-2):
            # print(f"{abs(gap)//2} < {(d1-i)*1e-4}")
            # print(f"{i}, {gap}")
            jump = 1
            tmp_point = corner + i*direction
            while ((i+jump) < d1) and (distance(tmp_point, s2) - d2 == gap):
                tmp_point = corner + (i+jump)*direction
                jump = 2*jump
            if distance(tmp_point, s2) - d2 == gap:
                jump = jump//2
            else:
                jump = jump//4
            if gap in [0, 1]:
                intersections.extend([corner+(i+j)*direction for j in range(jump)])
            i += jump+1
        else:
            i += max(1, abs(gap)//2)
            
        # print(f"dist: {dist}, i: {i} d2: {d2}, gap: {gap}")
    return intersections
        
def get_intersection_left(s1, s2, d1, d2):
    intersections = []
    direction = np.array([1, -1])
    corner = s1 + (-d1, 0)
    intersections.extend(get_intersection_left_inner(s2, d1, d2, direction, corner))
    
    direction = np.array([1, 1])
    corner = s1 + (0, -d1)
    intersections.extend(get_intersection_left_inner(s2, d1, d2, direction, corner))
    
    direction = np.array([-1, 1])
    corner = s1 + (d1, 0)
    intersections.extend(get_intersection_left_inner(s2, d1, d2, direction, corner))
    
    direction = np.array([-1, -1])
    corner = s1 + (0, d1)
    intersections.extend(get_intersection_left_inner(s2, d1, d2, direction, corner))
    return intersections
    

def get_intersection2(pairA, pairB):
    sA = pairA[0]
    sB = pairB[0]
    bA = pairA[1]
    bB = pairB[1]
    distA = distance(sA, bA)+1
    distB = distance(sB, bB)+1
    distAB = distance(sA, sB)
    if distAB > distA+distB:
        return []
    intersections = []
    intersections.extend(get_intersection_left(sA, sB, distA, distB))
    if (sA.sum() % 2) != (sB.sum() % 2):
        intersections.extend(get_intersection_left(sB, sA, distB, distA))
    return intersections

all_intersections = []
for i in range(len(pairs)):
    for j in range(i+1, len(pairs)):
        intersections = get_intersection2(pairs[i], pairs[j])
        all_intersections.extend(intersections)
        print(f"Found intersections for pairing ({i}, {j}): {len(intersections)} points")


counted = Counter([f"{element[0]},{element[1]}" for element in all_intersections])

for i, (point_str, count) in enumerate(counted.most_common()):
    if i % 1000 == 0:
        print(f"Step {i}")
    point = np.array([int(num) for num in point_str.split(",")])
    if (0< point[0] < x_range[1]) and (0 < point[1] < y_range[1]):
        if out_of_range(point, pairs):
            break

solution_part2 = 4000000*point[0]+point[1]

print(f"Solution to part 2: {solution_part2}")
