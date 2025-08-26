import time
import os
import random

cd = os.getcwd()
STATE_FILE = "player_state.txt"
ACTION_FILE = "inputs.txt"
ZONE_LOG_FILE = "visited_zones.txt"
TILE_LOG_FILE = "tile_log.txt"
STATE_PATH = os.path.join(cd, STATE_FILE)
ACTION_PATH = os.path.join(cd, ACTION_FILE)
ZONE_PATH = os.path.join(cd, ZONE_LOG_FILE)
TILE_PATH = os.path.join(cd, TILE_LOG_FILE)

chunk_size = 10

DIRECTIONS = ["UP", "DOWN", "LEFT", "RIGHT"]
OPPOSITE = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}

visited_zones = set()
discovered_tiles = {}  # (map_id, x, y, z) -> type
explored_directions = {}  # (map_id, x, y, z) -> set of directions
blocked_directions = {}  # (map_id, x, y, z) -> set of blocked directions
interaction_attempts = {}  # (map_id, x, y, z) -> int
total_reward = 0

def load_visited_zones():
    if os.path.exists(ZONE_PATH):
        with open(ZONE_PATH, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 3:
                    visited_zones.add(tuple(map(int, parts)))

def save_visited_zone(zone):
    with open(ZONE_PATH, "a") as f:
        f.write(f"{zone[0]},{zone[1]},{zone[2]}\n")

def load_tile_log():
    if os.path.exists(TILE_PATH):
        with open(TILE_PATH, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 5:
                    key = (int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3]))
                    discovered_tiles[key] = parts[4]
                    explored_directions.setdefault(key, set())
                    blocked_directions.setdefault(key, set())

def save_tile_log(map_id, x, y, z, tile_type):
    with open(TILE_PATH, "a") as f:
        f.write(f"{map_id},{x},{y},{z},{tile_type}\n")

def read_state():
    try:
        with open(STATE_PATH, "r") as f:
            line = f.readline()
            map_id, x, y, z = map(int, line.strip().split(","))
            return map_id, x, y, z
    except Exception:
        return None, None, None, None

def write_action(action):
    with open(ACTION_PATH, "w") as f:
        f.write(action)

def get_zone(map_id, x, y, chunk_size=10):
    return (map_id, x // chunk_size, y // chunk_size)

def test_direction(current_state, direction):
    map_id, x, y, z = current_state
    write_action(direction)
    time.sleep(0.3)
    new_state = read_state()
    if None in new_state:
        return None, None

    new_map_id, new_x, new_y, new_z = new_state
    moved = (new_x != x or new_y != y or new_z != z)
    map_changed = (new_map_id != map_id)

    if not moved:
        # Didn't move — check for dialog/NPC/wall
        dialog_count = 0
        for _ in range(3):
            write_action("A")
            time.sleep(0.3)
            if read_state() == current_state:
                dialog_count += 1

        if dialog_count >= 2:
            return new_state, "roadblock"
        else:
            return new_state, "npc_or_wall"

    # Moved — check if dialog immediately triggers on arrival
    dialog_triggered = True
    for _ in range(3):
        write_action("A")
        time.sleep(0.3)
        if read_state() != new_state:
            dialog_triggered = False
            break

    if dialog_triggered:
        return new_state, "roadblock"
    elif map_changed:
        return new_state, "door"
    else:
        return new_state, "empty"

def backtrack(direction):
    write_action(OPPOSITE[direction])
    time.sleep(0.3)

def detect_dialog_scene(current_state):
    stuck_count = 0
    for direction in DIRECTIONS:
        write_action(direction)
        time.sleep(0.2)
        new_state = read_state()
        if not new_state or new_state[:4] == current_state[:4]:
            stuck_count += 1
    return stuck_count == len(DIRECTIONS)

# ---- MAIN LOOP ----

load_visited_zones()
load_tile_log()

while True:
    current_state = read_state()
    if None in current_state:
        print("Waiting for valid game state...")
        write_action("")
        time.sleep(0.5)
        continue

    if detect_dialog_scene(current_state):
        print("Dialog detected! Pressing 'A'...")
        for _ in range(5):
            write_action("A")
            time.sleep(0.3)
        continue

    map_id, x, y, z = current_state
    zone = get_zone(map_id, x, y, chunk_size)
    tile_key = (map_id, x, y, z)

    if zone not in visited_zones:
        visited_zones.add(zone)
        save_visited_zone(zone)
        reward = 1.0
        print(f"New zone discovered: {zone}, +1 reward")
    else:
        reward = 0.0
    total_reward += reward

    if tile_key not in discovered_tiles:
        discovered_tiles[tile_key] = "empty"
        explored_directions[tile_key] = set()
        blocked_directions[tile_key] = set()
        interaction_attempts[tile_key] = 0
        save_tile_log(*tile_key, "empty")
        print(f"Logged current tile as empty: {tile_key}")

    unexplored_dirs = [
        d for d in DIRECTIONS
        if d not in explored_directions[tile_key]
        and d not in blocked_directions[tile_key]
    ]

    if unexplored_dirs:
        direction = unexplored_dirs[0]
        new_state, tile_type = test_direction(current_state, direction)

        if tile_type == "roadblock":
            blocked_directions[tile_key].add(direction)
            print(f"Roadblock detected going {direction} from {tile_key}, marking as blocked")
        else:
            explored_directions[tile_key].add(direction)

        if new_state:
            new_key = (new_state[0], new_state[1], new_state[2], new_state[3])
            if new_key not in discovered_tiles:
                discovered_tiles[new_key] = tile_type
                explored_directions[new_key] = set()
                blocked_directions[new_key] = set()
                interaction_attempts[new_key] = 0
                save_tile_log(*new_key, tile_type)
                print(f"Discovered {tile_type} at {new_key} by moving {direction}")

            if new_state != current_state:
                backtrack(direction)

        print(f"Zone: {map_id}, Pos: ({x},{y},{z}), Action: {direction}, Total reward: {total_reward:.1f}")
        write_action(direction)

    else:
        if interaction_attempts.get(tile_key, 0) < 3 and random.random() < 0.2:
            interaction_attempts[tile_key] += 1
            print(f"Trying interaction at {tile_key} (attempt {interaction_attempts[tile_key]})...")
            write_action("A")
        else:
            direction = random.choice(DIRECTIONS + [""])
            print(f"Zone: {map_id}, Pos: ({x},{y},{z}), Action: {direction}, Total reward: {total_reward:.1f}")
            write_action(direction)

    time.sleep(0.5)