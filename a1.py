"""
CSSE1001 2019s2a1
"""

from a1_support import *

def get_position_in_direction(position, direction):
    """Calculate the new row,column position in the given direction.

    Parameters:
        position (tuple<int, int>): The row, column position of a tile.
        direction (str): The given direction.

    Returns:
        (tuple<int,int>): The resultant row,column position in the given direction.
    """
    x,y = position
    dx,dy = DIRECTIONS[direction]
    return x+dx,y+dy
    
def get_tile_at_position(level, position):
    """Determines the tile at the given position.

    Parameters:
        level (str): The level string.
        position (tuple<int, int>): The row, column position of a tile.

    Returns:
        (str): The tile at the given position in the level string.
    """
    size = level_size(level)
    index = position_to_index(position, size)
    return level[index]

def get_tile_in_direction(level, position, direction):
    """Determine the tile in the given direction.

    Parameters:
        level (str): The level string.
        position (tuple<int, int>): The row, column position of a tile.
        direction (str): The given direction.

    Returns:
        (str): The tile in the position of the given direction in the level string.
    """
    position = get_position_in_direction(position,direction)
    return get_tile_at_position(level,position)

def remove_from_level(level, position):
    """Removes the tile at the given position from the level string.

    Parameters:
        level (str): The level string.
        position (tuple<int, int>): The row, column position of a tile.

    Returns:
        (str): The level string with the tile in the given position removed.
    """
    size = level_size(level)
    index = position_to_index(position, size)
    level = level[:index] + AIR + level[1 + index:]
    return level

def move(level, position, direction):
    """Alters the players position in the given direction on the given level.

    Parameters:
        level (str): The level string.
        position (tuple<int, int>): The row, column position of a tile.
        direction (str): The given direction.

    Returns:
        (tuple<int, int>): The resultant row, column position of the player.
    """
    position = get_position_in_direction(position,direction)
    tile = get_tile_at_position(level,position)
           
    if tile == WALL:
        while tile == WALL:
            position = get_position_in_direction(position,UP)
            tile = get_tile_at_position(level,position)
    if position[1] != 0:
        below_tile = get_tile_in_direction(level, position, DOWN)   
        if tile == AIR:
            while below_tile == AIR:
                position = get_position_in_direction(position,DOWN)
                below_tile = get_tile_in_direction(level, position, DOWN)
    
    return position

def print_level(level, position):
    """Prints the level string with the player at the given position.

    Parameters:
        level (str): The level string.
        position (tuple<int, int>): The row, column position of a tile.

    Returns:
        (str): The level string with the player in the given position.
    """
    size = level_size(level)
    index = position_to_index(position, size)
    level = level[:index] + PLAYER + level[1 + index:]
    print(level)

def attack(level, position):
    """Removes the monster tile to the left or right of the player, if one exists.

    Parameters:
        level (str): The level string.
        position (tuple<int, int>): The row, column position of a tile.

    Returns:
        (str): The level string with the monster tile removed, if attacked.
    """
    left_position = get_position_in_direction(position,LEFT)
    left_tile = get_tile_at_position(level,left_position)
    right_position = get_position_in_direction(position,RIGHT)
    right_tile = get_tile_at_position(level,right_position)

    if left_tile == MONSTER:
        print ("Attacking the monster on your left!")
        level = remove_from_level(level,left_position)
    elif right_tile == MONSTER:
        print ("Attacking the monster on your right!")
        level = remove_from_level(level,right_position)
    elif left_tile != MONSTER and right_tile != MONSTER:
        print ("No monsters to attack!")
    return level

def tile_status(level, position):
    """Determines the tile at given position and prints appropriate statement or removes tile.

    Parameters:
        level (str): The level string.
        position (tuple<int, int>): The row, column position of a tile.

    Returns:
        (tuple<str,str>): A tuple containing the tile and level string.
    """
    tile = get_tile_at_position(level,position)
    
    if tile == GOAL:
        print("Congratulations! You finished the level")
    elif tile == MONSTER:
        print("Hit a monster!")
    elif tile == COIN or tile == CHECKPOINT:
        level = remove_from_level(level,position)
    return (tile,level)

def main():
    """Main interface with the user/player.
       Promps for inputs of level and action strings and calls appropriate functions until the goal is reached, game is quit, or player is killed.
    """
    position = (0,1)
    score = 0
    filename = input("Please enter the name of the level file (e.g. level1.txt): ")
    level = load_level(filename)
    checkpoint=0        

    while True:
        print ("Score:", score)
        print_level(level,position)
        
        direction = input("Please enter an action (enter '?' for help): ")
        if direction in (RIGHT,LEFT):
            position = move(level,position,direction)
        elif direction == "a":
            level = attack(level,position)
        elif direction == "?":
            print (HELP_TEXT)
        elif direction == "q":
            return
        elif direction == "n": 
            position = saved_position
            score = saved_score
            continue
    
        tile,level = tile_status(level,position)
        if tile == CHECKPOINT:
            saved_position = position
            saved_score = score
            checkpoint+=1
        if tile == MONSTER:
            if checkpoint != 0:
                position = saved_position
                score = saved_score
                continue
            break
        elif tile == GOAL:
            return
        elif tile == COIN:
            score +=1
    
    
if __name__ == "__main__":
    main()
