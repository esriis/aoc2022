file_path = "input/day3.txt"

with open(file_path, mode="r") as f:
    text = f.read()

rucksacks = [
    list(line)
    for line in text.strip("\n").split("\n")
]

rucksack_compartments = [
    (rucksack[:len(rucksack)//2], rucksack[len(rucksack)//2:])
    for rucksack in rucksacks
]

errors = [
    list(set(compartments[0]).intersection(compartments[1]))
    for compartments in rucksack_compartments
]

lower_offset = -ord("a")+1
upper_offset = -ord("A")+27

def get_item_priority(item: str):
    if item.islower():
        priority = ord(item)+lower_offset
    else:
        priority = ord(item)+upper_offset
    return priority

priorities_part1 = [
    sum([get_item_priority(item) for item in error])
    for error in errors
]

solution_part1 = sum(priorities_part1)
print(f"Solution to part 1: {solution_part1}")


def get_badge(rucksacks):
    badges = list(set.intersection(
        *[set(rucksack) for rucksack in rucksacks]
    ))
    if len(badges) != 1:
        raise Exception()
    return badges[0]

badges = [
    get_badge(rucksacks[3*i:3*(i+1)])
    for i in range(len(rucksacks)//3)
]

solution_part2 = sum(get_item_priority(badge) for badge in badges)


print(f"Solution to part 2: {solution_part2}")