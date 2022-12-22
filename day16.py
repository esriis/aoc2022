file_path = "input/day16.txt"

with open(file_path, mode="r") as f:
    text = f.read()

def parse_line(line: str):
    words = line.split(" ")
    name = words[1]
    flow_rate = int(words[4][5:-1])
    connections = [valve.strip(",") for valve in words[9:]]
    return name, flow_rate, connections

valve_data = [parse_line(line) for line in text.splitlines()]
valve_dict = {
    name: {"flow_rate": flow_rate, "connections": connections} for name, flow_rate, connections in valve_data
}

positive_valves = [name for name, valve in valve_dict.items() if valve["flow_rate"] > 0]

start_valve = "AA"
path_cost = {name: {} for name in positive_valves + [start_valve]}

for name in positive_valves + [start_valve]:
    #
    undiscovered_valves = [valve for valve in positive_valves if valve!=name]
    #
    iter_cap = 1_000
    iters = 0
    paths = [[name]]
    traversed_valves = []
    while (len(undiscovered_valves) > 0) and (iters < iter_cap):
        iters += 1
        new_paths = []
        for path in paths:
            connections = valve_dict[path[-1]]["connections"]
            for connection in connections:
                new_path = path+[connection]
                if connection in undiscovered_valves:
                    path_cost[name][connection] = len(new_path)
                    new_paths.append(new_path)
                    undiscovered_valves.remove(connection)
                    traversed_valves.append(connection)
                elif connection not in traversed_valves:
                    new_paths.append(new_path)
                    traversed_valves.append(connection)
        paths = new_paths


total_time = 30

paths = [{"path": [start_valve], "time": 0, "flow": 0, "flow_rate": 0}]
finished_paths = []
max_iter = total_time
iters = 0
while (len(paths) > 0) and (iters <= max_iter):
    iters += 1
    print(f"{len(paths):_d}, {len(finished_paths):_d}")
    new_paths = []
    for data in paths:
        path = data["path"]
        name = path[-1]
        path_finished = True
        for connection, cost in path_cost[name].items():
            if (connection not in path) and (data["time"]+cost <= total_time):
                new_data = data.copy()
                new_data["path"] = new_data["path"] + [connection]
                new_data["flow"] += cost*new_data["flow_rate"]
                new_data["time"] += cost
                new_data["flow_rate"] += valve_dict[connection]["flow_rate"]
                new_paths.append(new_data)
        if path_finished:
            data["flow"] += (total_time-data["time"])*data["flow_rate"]
            data["time"] = total_time
            finished_paths.append(data)
    paths = new_paths

solution_part1 = max(data["flow"] for data in finished_paths)

print(f"Solution to part 1: {solution_part1}")

"""
Part 2
"""


total_time = 26

paths = [(
    {"path": [start_valve], "time": 0, "flow": 0, "flow_rate": 0},
    {"path": [start_valve], "time": 0, "flow": 0, "flow_rate": 0}
)]

finished_paths = []
max_iter = total_time
iters = 0
while (len(paths) > 0) and (iters <= max_iter):
    iters += 1
    print(f"{len(paths):_d}, {len(finished_paths):_d}")
    new_paths = []
    for i, datas in enumerate(paths):
        if i % 10_000 == 0:
            print(f"i = {i}")
        # print(len(new_paths))
        path_finished = True
        human = datas[0]
        elephant = datas[1]
        human_name = human["path"][-1]
        elephant_name = elephant["path"][-1]
        total_path = human["path"] + elephant["path"]
        # hi
        for h_connection, h_cost in path_cost[human_name].items():
            if (h_connection not in total_path) and (h_cost + human["time"] <= total_time):
                path_finished = False
                new_human = human.copy()
                new_human["path"] = new_human["path"] + [h_connection]
                new_human["flow"] += h_cost*new_human["flow_rate"]
                new_human["time"] += h_cost
                new_human["flow_rate"] += valve_dict[h_connection]["flow_rate"]
                new_paths.append((new_human, elephant))
        for h_connection, h_cost in path_cost[human_name].items():
            for e_connection, e_cost in path_cost[elephant_name].items():
                if (
                    (e_connection not in total_path)
                    and (e_cost + elephant["time"] <= total_time)
                    and (h_connection not in total_path)
                    and (h_cost + human["time"] <= total_time)
                    and (e_connection != h_connection)
                ):
                    path_finished = False
                    new_human = human.copy()
                    new_human["path"] = new_human["path"] + [h_connection]
                    new_human["flow"] += h_cost*new_human["flow_rate"]
                    new_human["time"] += h_cost
                    new_human["flow_rate"] += valve_dict[h_connection]["flow_rate"]
                    new_elephant = elephant.copy()
                    new_elephant["path"] = new_elephant["path"] + [e_connection]
                    new_elephant["flow"] += e_cost*new_elephant["flow_rate"]
                    new_elephant["time"] += e_cost
                    new_elephant["flow_rate"] += valve_dict[e_connection]["flow_rate"]
                    new_paths.append((new_human, new_elephant))
        if path_finished:
            datas[0]["flow"] += (total_time-datas[0]["time"])*datas[0]["flow_rate"]
            datas[0]["time"] = total_time
            datas[1]["flow"] += (total_time-datas[1]["time"])*datas[1]["flow_rate"]
            datas[1]["time"] = total_time
            finished_paths.append((datas))
    old_len = len(new_paths)
    print("finished iterations")
    new_paths = [
        (
            (tuple(d[0]["path"]), d[0]["flow"], d[0]["flow_rate"], d[0]["time"]),
            (tuple(d[1]["path"]), d[1]["flow"], d[1]["flow_rate"], d[1]["time"])
        )
        for d in new_paths
    ]
    print("hashing")
    new_paths = [
        (
            {"path": list(d[0][0]), "flow": d[0][1], "flow_rate": d[0][2], "time": d[0][3]},
            {"path": list(d[1][0]), "flow": d[1][1], "flow_rate": d[1][2], "time": d[1][3]}
        )
        for d in list(set(new_paths))
    ]
    new_len = len(new_paths)
    print(f"old len: {old_len}. new len: {new_len}")
    print("cleaning")
    if new_len >= 5_000:
        new_paths = sorted(
            new_paths,
            key=lambda d: d[0]["flow_rate"]*(total_time - d[0]["time"]) + d[0]["flow"]
                + d[1]["flow_rate"]*(total_time - d[1]["time"]) + d[1]["flow"],
            reverse=True                
        )[:5_000]
    paths = new_paths

solution_part2 = max(d[0]["flow"] + d[1]["flow"] for d in finished_paths)

print(f"Solution to part 2: {solution_part2}")
