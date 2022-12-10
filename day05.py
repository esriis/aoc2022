import re

file_path = "input/day05.txt"

with open(file_path, mode="r") as f:
    text = f.read()

stack_text, procedure_text = text.strip("\n").split("\n\n")

stack_lines = stack_text.split("\n")[0:-1]

stacks = [
    [line[4*i+1] for line in reversed(stack_lines) if line[4*i+1] != " "]
    for i in range((len(stack_lines[0])+1)//4)
]

def parse_procedure(line: str):
    return tuple(int(num) for num in re.split(" from | to ", line.lstrip("move ")))

procedures = [parse_procedure(line) for line in procedure_text.split("\n")]

for procedure in procedures:
    qty, old, new = procedure
    for crate in range(qty):
        stacks[new-1].append(stacks[old-1].pop())

solution_part1 = "".join([stack[-1] for stack in stacks])

print(f"Solution to part 1 is {solution_part1}")


stacks2 = [
    [line[4*i+1] for line in reversed(stack_lines) if line[4*i+1] != " "]
    for i in range((len(stack_lines[0])+1)//4)
]

for procedure in procedures:
    qty, old, new = procedure
    old_stack = stacks2[old-1]
    new_stack = stacks2[new-1]
    substack = old_stack[-qty:]
    del old_stack[-qty:]
    new_stack.extend(substack)

solution_part2 = "".join([stack[-1] for stack in stacks2])

print(f"Solution to part 2 is {solution_part2}")