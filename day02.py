file_path = "input/day02.txt"

with open(file_path, mode="r") as f:
    text = f.read()

rounds_raw = [
    tuple(step.split(" ")) for step in text.strip("\n").split("\n")
]


def get_outcome_score(opponent, you):
    return (((you-opponent+1) % 3))*3

def get_total_score(rounds):
    shape_score = sum([your_move+1 for _, your_move in rounds])
    outcome_score = sum([get_outcome_score(step[0], step[1]) for step in rounds])
    return shape_score + outcome_score


# translate to rock = 0, paper = 1, scissors = 2

rounds_part1 = [
    (ord(step[0])-ord("A"), ord(step[1])-ord("X")) for step in rounds_raw
]

score_part1 = get_total_score(rounds_part1)

print(f"Solution to part 1: {score_part1}")

"""
Part 2
"""

rounds_part2 = [
    (
        ord(step[0])-ord("A"),
        ((ord(step[0])-ord("A")) + (ord(step[1])-ord("X")-1)) % 3
    ) for step in rounds_raw
]

score_part2 = get_total_score(rounds_part2)

print(f"Solution to part 2: {score_part2}")
