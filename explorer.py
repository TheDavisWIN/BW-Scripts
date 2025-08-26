import os
import time
import json
from collections import deque

cd = os.getcwd()
STATE_FILE = "player_state.txt"
GRAPH_FILE = "tile_graph.json"
PATH_FILE = "path_inputs.txt"
STATE_PATH = os.path.join(cd, STATE_FILE)
GRAPH_PATH = os.path.join(cd, GRAPH_FILE)
PATH_PATH = os.path.join(cd, PATH_FILE)

DIRECTIONS = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0)
}

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
    if os.path.exists(GRAPH_PATH):
        with open(GRAPH_PATH, "r") as f:
            data = json.load(f)
            graph = {
                eval(k): {d: eval(v) for d, v in vmap.items()}
                for k, vmap in data.get("graph", {}).items()
            }
            doors = set(eval(d) for d in data.get("doors", []))
            return graph, doors
    return {}, set()

def save_graph(graph, doors):
    with open(GRAPH_PATH, "w") as f:
        json.dump({
            "graph": {
                str(k): {d: str(v) for d, v in vmap.items()}
                for k, vmap in graph.items()
            },
            "doors": [str(d) for d in doors]
        }, f, indent=2)

def write_path(path):
    with open(PATH_PATH, "w") as f:
        for step in path:
            f.write(step + "\n")

def opposite(direction):
    return {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}[direction]

def get_adjacent(tile):
    return {
        d: (tile[0], tile[1] + dx, tile[2] + dy, tile[3])
        for d, (dx, dy) in DIRECTIONS.items()
    }

def wait_until_path_empty(timeout=5.0, interval=0.1):
    start = time.time()
    while time.time() - start < timeout:
        if os.path.exists(PATH_PATH):
            with open(PATH_PATH, "r") as f:
                if not f.read().strip():
                    return True
        time.sleep(interval)
    return False

def wait_until_at(target_tile, timeout=4.0, interval=0.1):
    start = time.time()
    while time.time() - start < timeout:
        state = read_state()
        if state == target_tile:
            # Confirm stable position by re-checking shortly
            time.sleep(interval)
            if read_state() == target_tile:
                return True
        time.sleep(interval)
    return False

def find_path(graph, start, goal):
    queue = deque([(start, [])])
    visited = set([start])

    while queue:
        current, path = queue.popleft()
        if current == goal:
            return path

        for direction, neighbor in graph.get(current, {}).items():
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [direction]))

    return None

# New helper to clear inputs cleanly
def clear_inputs():
    wait_until_path_empty()
    write_path([])
    time.sleep(0.1)  # small delay to ensure clearing registers

def bfs_explore():
    graph, doors = load_graph()
    current_state = read_state()
    if not current_state:
        print("No initial player state.")
        return

    visited = set(graph.keys())
    queue = deque()

    if not graph:
        print(f"Starting from initial tile: {current_state}")
        visited.add(current_state)
        queue.append(current_state)
    elif current_state not in visited:
        print(f"Resuming from current tile: {current_state}")
        visited.add(current_state)
        queue.append(current_state)

    walls = set()

    while queue:
        current_tile = queue.popleft()

        # Move to the tile if not already there
        player_state = read_state()
        if player_state != current_tile:
            print(f"Moving from {player_state} to {current_tile}")
            path = find_path(graph, player_state, current_tile)
            if path:
                wait_until_path_empty()
                write_path(path)
                if not wait_until_at(current_tile):
                    print("Could not reach current_tile. Skipping.")
                    continue
                time.sleep(0.2)
            else:
                print("No path found. Skipping.")
                continue

        print(f"\n Exploring from: {current_tile}")

        for direction, neighbor in get_adjacent(current_tile).items():
            if neighbor in visited or (current_tile, direction) in walls:
                continue

            print(f"Trying {direction} to {neighbor}")

            wait_until_path_empty()
            write_path([direction])
            time.sleep(0.2)

            # Wait to see if move succeeded
            if not wait_until_at(neighbor):
                state_after_move = read_state()

                if state_after_move == current_tile:
                    print(f"Wall detected: cannot move {direction} from {current_tile}")
                    walls.add((current_tile, direction))
                    clear_inputs()
                else:
                    print(f"Unexpected movement. Now at {state_after_move}")
                    clear_inputs()

                continue
            new_state = read_state()
            if not new_state:
                print("Failed to read state after move.")
                continue

            if new_state[0] != current_tile[0]:
                print(f"Door detected at {current_tile}")
                doors.add(current_tile)
                clear_inputs()
                write_path([opposite(direction)])
                wait_until_at(current_tile)
                time.sleep(0.2)
                continue

            print(f"Reached new tile: {new_state}")

            if current_tile not in graph:
                graph[current_tile] = {}
            graph[current_tile][direction] = new_state

            rev_dir = opposite(direction)
            if new_state not in graph:
                graph[new_state] = {}
            graph[new_state][rev_dir] = current_tile

            clear_inputs()
            write_path([opposite(direction)])
            if not wait_until_at(current_tile):
                print("Could not return to start tile. At", read_state())
            else:
                time.sleep(0.2)

            if new_state not in visited:
                visited.add(new_state)
                queue.append(new_state)

            save_graph(graph, doors)

    print("\n BFS exploration complete.")
    save_graph(graph, doors)
    clear_inputs()

if __name__ == "__main__":
    bfs_explore()