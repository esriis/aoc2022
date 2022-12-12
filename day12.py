import numpy as np
from day12_classes import State

file_path = "input/day12.txt"

with open(file_path, mode="r") as f:
    text = f.read()

start_map = np.array([list(line) for line in text.strip("\n").split("\n")])

def initialise_state_map(start_map: np.ndarray) -> np.ndarray:
    state_map = np.array([[State.create(letter) for letter in line] for line in start_map])
    return state_map

def get_available_positions(
    position: tuple[int],
    number: int,
    state_map: np.ndarray,
    reverse_mode: bool = False
) -> list[np.ndarray]:
    positions = [
        tuple(position+np.array(direction)) for direction in [[1, 0], [-1, 0], [0, -1], [0, 1]]
    ]
    available_positions = []
    for position in positions:
        accessible = (position[0] in range(state_map.shape[0])) \
            and (position[1] in range(state_map.shape[1])) \
            and state_map[position].is_accessible(number=number, reverse=reverse_mode)
        if accessible:
            available_positions.append(position)
    return available_positions

start_position = tuple(pos[0] for pos in np.where(start_map == "S"))
end_position = tuple(pos[0] for pos in np.where(start_map == "E"))
start_letter = "a"
end_letter = "z"

map_corrected = start_map.copy()
map_corrected[start_position] = start_letter
map_corrected[end_position] = end_letter

state_map = initialise_state_map(map_corrected)

def claim_position(
    position: tuple[int],
    sequence: list[tuple[int]],
    state_map: np.ndarray
):
    state_map[position].sequence = sequence
    state_map[position].available = False
    return state_map


sequences = [[start_position]]
state_map = claim_position(
    position=sequences[0][-1],
    sequence=sequences[0],
    state_map=state_map
)

iterations = 5

end_reached = False
max_iterations = 1000
counter = 0
reverse_mode=False

while (counter < max_iterations) and not end_reached:
    # print(len(sequences))
    # print(counter)
    counter += 1
    new_sequences = []
    for sequence in sequences:
        position = sequence[-1]
        number = ord(map_corrected[position])
        available_positions = get_available_positions(
            position=position,number=number, state_map=state_map, reverse_mode=reverse_mode
        )
        for new_position in available_positions:
            new_sequence = sequence.copy()+[new_position]
            new_sequences.append(new_sequence)
            state_map = claim_position(
                position=new_position,
                sequence=new_sequence,
                state_map=state_map,
            )
            if new_position == end_position:
                end_reached = True
    if len(new_sequences) == 0:
        raise Exception()
    sequences = [sequence.copy() for sequence in new_sequences]

solution_part1 = len(sequences[0])-1
print(f"Solution to part 1: {solution_part1}")

"""
Part 2
"""


reverse_mode = True

iterations = 5

sequences = [[end_position]]
state_map = initialise_state_map(map_corrected)
state_map = claim_position(
    position=sequences[0][-1],
    sequence=sequences[0],
    state_map=state_map
)

a_reached = False
max_iterations = 1000
counter = 0

while (counter < max_iterations) and not a_reached:
    # print(len(sequences))
    # print(counter)
    counter += 1
    new_sequences = []
    for sequence in sequences:
        position = sequence[-1]
        number = ord(map_corrected[position])
        available_positions = get_available_positions(
            position=position,number=number, state_map=state_map, reverse_mode=reverse_mode
        )
        for new_position in available_positions:
            new_sequence = sequence.copy()+[new_position]
            new_sequences.append(new_sequence)
            state_map = claim_position(
                position=new_position,
                sequence=new_sequence,
                state_map=state_map,
            )
            if map_corrected[new_position] == "a":
                a_reached = True
    if len(new_sequences) == 0:
        raise Exception()
    sequences = [sequence.copy() for sequence in new_sequences]


solution_part2 = len(sequences[0])-1
print(f"Solution to part 2: {solution_part2}")