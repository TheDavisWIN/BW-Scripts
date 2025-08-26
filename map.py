import time
import os
import json

cd = os.getcwd()
STATE_FILE = "player_state.txt"
GRAPH_FILE = "tile_graph.json"
STATE_PATH = os.path.join(cd, STATE_FILE)
GRAPH_PATH = os.path.join(cd, GRAPH_FILE)

DIRECTIONS = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0)
}

visited_tiles = set()
tile_graph = {}  # {(map_id, x, y, z): {direction: (map_id, x, y, z)}}
doors = set()
last_state = None

def read_state():
    if os.path.exists(STATE_PATH):
        with open(STATE_PATH, "r") as f:
            line = f.read().strip()
            if line:
                try:
                    return tuple(map(int, line.split(",")))  # (map_id, x, y, z)
                except ValueError:
                    return None
    return None

def get_direction(from_tile, to_tile):
    dx = to_tile[1] - from_tile[1]
    dy = to_tile[2] - from_tile[2]
    for direction, (ddx, ddy) in DIRECTIONS.items():
        if (dx, dy) == (ddx, ddy):
            return direction
    return None

def save_graph():
    graph_data = {
        "graph": {
            str(k): {d: str(v) for d, v in dir_map.items()}
            for k, dir_map in tile_graph.items()
        },
        "doors": [str(d) for d in doors]
    }
    with open(GRAPH_PATH, "w") as f:
        json.dump(graph_data, f, indent=2)

def main():
    global last_state
    print("Tracking tile graph and doors...\n")

    while True:
        current_state = read_state()
        if not current_state:
            time.sleep(0.2)
            continue

        if current_state not in visited_tiles:
            visited_tiles.add(current_state)
            print(f"New tile: Map {current_state[0]}, X {current_state[1]}, Y {current_state[2]}, Z {current_state[3]}")

        if last_state:
            # Detect doors based on map_id change
            if current_state[0] != last_state[0]:
                if last_state not in doors:
                    doors.add(last_state)
                    print(f"Door detected at: {last_state}")

            else:
                # If same map, log directional transition
                direction = get_direction(last_state, current_state)
                if direction:
                    if last_state not in tile_graph:
                        tile_graph[last_state] = {}
                    tile_graph[last_state][direction] = current_state
                    print(f"{direction} from {last_state} to {current_state}")

            save_graph()

        last_state = current_state
        time.sleep(0.2)

if __name__ == "__main__":
    main()