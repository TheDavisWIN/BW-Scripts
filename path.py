import json
import os
import time
from collections import deque

cd = os.getcwd()
STATE_FILE = "player_state.txt"
GRAPH_FILE = "tile_graph.json"
PATH_FILE = "path_inputs.txt"
STATE_PATH = os.path.join(cd, STATE_FILE)
GRAPH_PATH = os.path.join(cd, GRAPH_FILE)
PATH_PATH = os.path.join(cd, PATH_FILE)


def read_state():
    if os.path.exists(STATE_PATH):
        with open(STATE_PATH, "r") as f:
            line = f.read().strip()
            if line:
                try:
                    return tuple(map(int, line.split(",")))
                except ValueError:
                    return None
    return None

def load_graph():
    with open(GRAPH_PATH, "r") as f:
        data = json.load(f)
        graph = {
            eval(k): {d: eval(v) for d, v in edges.items()}
            for k, edges in data["graph"].items()
        }
        doors = [eval(d) for d in data["doors"]]
        return graph, doors

def find_shortest_path(graph, start, goal_set):
    queue = deque([(start, [])])
    visited = set()

    while queue:
        current, path = queue.popleft()
        if current in goal_set:
            return path

        visited.add(current)
        for direction, neighbor in graph.get(current, {}).items():
            if neighbor not in visited:
                queue.append((neighbor, path + [direction]))

    return None

def write_path(path):
    with open(PATH_PATH, "w") as f:
        for move in path:
            f.write(move + "\n")

def main():
    current_tile = None
    while current_tile is None:
        current_tile = read_state()
        time.sleep(0.2)

    graph, doors = load_graph()
    same_map_doors = [d for d in doors if d[0] == current_tile[0]]
    if not same_map_doors:
        print("No doors found on the current map.")
        return

    path = find_shortest_path(graph, current_tile, set(same_map_doors))
    if not path:
        print("No path found to any door on this map.")
        return

    print(f"Path found: {path}")
    write_path(path)
    print("Path written to path_inputs.txt. Lua will now handle movement.")

if __name__ == "__main__":
    main()