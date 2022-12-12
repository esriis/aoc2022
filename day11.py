from day11_classes import Monkey
import math

file_path = "input/day11.txt"

with open(file_path, mode="r") as f:
    text = f.read()

monkey_list = [Monkey.parse_monkey(monkey_str) for monkey_str in text.strip("\n").split("\n\n")]
monkey_dict = {monkey.number: monkey for monkey in monkey_list}

num_rounds = 20

for _ in range(num_rounds):
    for number in sorted(monkey_dict.keys()):
        monkey_dict[number].take_turn(monkey_dict)

inspections = sorted([monkey.inspections for monkey in monkey_dict.values()])

solution_part1 = inspections[-1]*inspections[-2]

print(f"Solution to part 1: {solution_part1}")

"""
Part 2
"""

num_rounds = 10_000
worry_mode = "stressed"

monkey_list = [Monkey.parse_monkey(monkey_str) for monkey_str in text.strip("\n").split("\n\n")]
monkey_dict = {monkey.number: monkey for monkey in monkey_list}

denominator = math.lcm(*[monkey.divisible_by for monkey in monkey_list])

for i in range(num_rounds):
    if i % 1_000 == 0:
        print(f"{round((i+1)/num_rounds*100)}%")
    for number in sorted(monkey_dict.keys()):
        monkey_dict[number].take_turn(monkey_dict, worry_mode=worry_mode, denominator=denominator)

inspections = sorted([monkey.inspections for monkey in monkey_dict.values()])

solution_part2 = inspections[-1]*inspections[-2]

print(f"Solution to part 2: {solution_part2}")