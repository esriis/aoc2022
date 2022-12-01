file_path = "input/day1.txt"

with open(file_path, mode="r") as f:
    result = f.read()

reindeers = sorted(
    [
        sum([int(calories) for calories in reindeer_str.split("\n")])
        for reindeer_str in result.strip("\n").split("\n\n")
    ],
    reverse=True
)

max_calories = reindeers[0]

top3_calories = sum(reindeers[0:3])