import numpy as np

file_path = "input/day08.txt"

with open(file_path, mode="r") as f:
    text = f.read()

forest = np.array([list(line) for line in text.strip("\n").split("\n")], dtype = int)

def get_peaks_mask(forest: np.ndarray):
    shape = forest.shape
    is_peak = np.array([[False]*shape[1]]*shape[0])
    for rotation in range(4):
        forest_rotated = np.rot90(forest, rotation)
        is_peak = is_peak | np.rot90(get_peaks_from_west(forest_rotated), -rotation)
    return is_peak

def get_peaks_from_west(forest):
    peak_from_west = np.maximum.accumulate(forest, axis=1)
    is_peak = (peak_from_west[:,1:]-peak_from_west[:,:-1])>0
    true_vec = np.array([[True]]*peak_from_west.shape[0])
    return np.concatenate([true_vec, is_peak] ,axis=1)

peak_mask = get_peaks_mask(forest)
solution_part1 = peak_mask.sum()

print(f"Solution to part 1: {solution_part1}")

"""
Part 2
"""

def get_scenic_score_for_array(value, array):
    return next((i+1 for i, tree in enumerate(array) if tree >= value),len(array))

def get_scenic_score_at_position(forest, x, y):
    value = forest[x,y]
    arrays = [
        forest[x,y+1:],
        np.flip(forest[x,:y]),
        forest[x+1:,y],
        np.flip(forest[0:x,y]),
    ]
    return np.prod([get_scenic_score_for_array(value, array) for array in arrays])

scenic_scores = np.array([
    [
        get_scenic_score_at_position(forest,x,y)
        for y in range(forest.shape[1])
    ]
    for x in range(forest.shape[0])
])

solution_part2 = scenic_scores.max()

print(f"Solution to part 2: {solution_part2}")