from pathlib import Path

file_path = "input/day7.txt"

with open(file_path, mode="r") as f:
    text = f.read()


lines = text.strip("\n").split("\n")

path = Path("/")
filesystem = {path.as_posix(): {}}

i=0
while i < len(lines):
    command = lines[i]
    if not command.startswith("$ "):
        i += 1
    else:
        if command.startswith("$ cd "):
            path = path/command[5:].strip(" ")
            if path_str not in filesystem:
                filesystem[path_str] = {}
            i += 1
        elif command.startswith("$ ls"):
            i+=1
            tmp_path = path/command[5:].strip(" ")
            path_str = tmp_path.resolve().as_posix()
            if path_str not in filesystem:
                filesystem[path_str] = {}
            while (i < len(lines)) and (not lines[i].startswith("$ ")):
                output = lines[i]
                if not output.startswith("dir "):
                    size, filename = output.split(" ", 1)
                    size = int(size.strip(" "))
                    filename = filename.strip(" ")
                    filesystem[path_str][filename] = size                   
                i += 1
        
        else:
            raise Exception("Failed to parse line")
        
folder_sizes = {path: 0 for path in filesystem.keys()}
for path, files in filesystem.items():
    size = sum(files.values())
    folder_sizes[path] += size
    for parent in Path(path).parents:
        parent_path = parent.resolve().as_posix()
        folder_sizes[parent_path] += size

max_size = 100_000

solution_part1 = sum([size for size in folder_sizes.values() if size <= max_size])

print(f"Solution to part 1: {solution_part1}")

"""
Part 2
"""
total_space = 70_000_000
required_space = 30_000_000
available_space = total_space - folder_sizes["/"]
missing_space = required_space - available_space
if missing_space > 0:
    smallest_folder = next(
        folder for folder in sorted(folder_sizes, key=folder_sizes.get)
        if folder_sizes[folder] >= missing_space
    )
    solution_part2 = folder_sizes[smallest_folder]
    print(f"Solution to part 2: {solution_part2}")