file_path = "input/day4.txt"

with open(file_path, mode="r") as f:
    text = f.read()

pairs_str = [
    pair.split(",")
    for pair in text.strip("\n").split("\n")
]

def str_to_bounds(input: str):
    bounds = [int(char) for char in input.split("-")]
    return bounds 

pairs_bounds = [
    [str_to_bounds(elf_str) for elf_str in pair]
    for pair in pairs_str
]

def contained(A, B):
    return (
        (A[0] <= B[0]) & (A[1] >= B[1])
    ) | (
        (A[0] >= B[0]) & (A[1] <= B[1])
    )

pairs_contained = [contained(*pair) for pair in pairs_bounds]

solution_part1 = sum(pairs_contained)

print(f"Solution to part 1: {solution_part1}")


reduced_bounds = [
    [max(pair[0][0], pair[1][0]), min(pair[0][1], pair[1][1])]
    for pair in pairs_bounds
]

overlaps = [
    max(0, bounds[1]-bounds[0]+1) > 0
    for bounds in reduced_bounds
]

solution_part2 = sum(overlaps)
print(f"Solution to part 2: {solution_part2}")
