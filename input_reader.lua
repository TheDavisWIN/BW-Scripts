local path_file = "C:\\Users\\davis\\BW-Scripts\\path_inputs.txt"
local location_file = "C:\\Users\\davis\\BW-Scripts\\player_state.txt"

local last_location = {map=-1, x=-1, y=-1, z=-1}
local current_input = nil
local waiting_for_move = false

local function read_location()
    local map = memory.readword(0x0224F90C)
    local x = memory.readword(0x0224F912, 2)
    local y = memory.readword(0x0224F91A)
    local z = memory.readword(0x0224F916)
    return {map=map, x=x, y=y, z=z}
end

local function same_location(loc1, loc2)
    return loc1.map == loc2.map and loc1.x == loc2.x and loc1.y == loc2.y and loc1.z == loc2.z
end

local function read_next_input()
    local f = io.open(path_file, "r")
    if not f then return nil end

    local all_lines = {}
    local next_input = nil

    for line in f:lines() do
        if not next_input then
            next_input = line  -- first line is the input
        else
            table.insert(all_lines, line)  -- keep remaining lines
        end
    end
    f:close()

    -- Rewrite the file without the first line
    f = io.open(path_file, "w")
    if f then
        for _, line in ipairs(all_lines) do
            f:write(line .. "\n")
        end
        f:close()
    end

    return next_input
end

while true do
    local current_location = read_location()

    -- Write current location to file
    local loc_file = io.open(location_file, "w")
    if loc_file then
        loc_file:write(string.format("%d,%d,%d,%d\n", current_location.map, current_location.x, current_location.y, current_location.z))
        loc_file:close()
    end

    local joypad_table = {}

    if not current_input and not waiting_for_move then
        current_input = read_next_input()
        if current_input then
            print("New input:", current_input)
            waiting_for_move = true
        end
    end

    if current_input then
        if not waiting_for_move then
            -- Already moved, get next input next frame
            current_input = nil
        else
            if not same_location(current_location, last_location) then
                waiting_for_move = false
            else
                -- Hold the button until movement occurs
                if current_input == "UP" then joypad_table.up = true end
                if current_input == "DOWN" then joypad_table.down = true end
                if current_input == "LEFT" then joypad_table.left = true end
                if current_input == "RIGHT" then joypad_table.right = true end
                if current_input == "A" then joypad_table.A = true end
                if current_input == "B" then joypad_table.B = true end
                if current_input == "START" then joypad_table.start = true end
                if current_input == "SELECT" then joypad_table.select = true end
            end
        end
    end

    joypad.set(1, joypad_table)
    last_location = current_location

    emu.frameadvance()
end