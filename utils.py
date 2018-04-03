"""Utility functions for solution.py"""

# Encode rows, columns and boxes
rows = "ABCDEFGHI"
cols = "123456789"
boxes = [r + c for r in rows for c in cols]
# A list of assignments to be used for visualization
assignments = []

def assign_value(values, box, value):
    """Record each assignment (in order) for later reconstruction.
    Parameters:
    values(dict)
        a dictionary of the form {"box_name": "123456789", ...}
    Returns:
    dict
        The values dictionary in which values[box] == value
    """

    # Don"t waste memory appending actions that don"t actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def cross(A, B):
    """Cross product of elements in A and elements in B"""
    return [s+t for s in A for t in B]

def grid_values(grid):
    """Convert grid into a dict of {square: char} with "123456789" for empties.
    Parameters:
    grid(string)
        a string representing a sudoku grid.
        
        Ex. "2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3"
    
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., "A1"
            Values: The value in each box, e.g., "8". If the box has no value,
            then the value will be "123456789".
    """
    grid_length = len(grid)
    assert grid_length == 81
    sodoku_dict = {}
    for i in range(grid_length):
        if grid[i] == ".":
            sodoku_dict[boxes[i]] = "123456789"
        else:
            sodoku_dict[boxes[i]] = grid[i]
    return sodoku_dict

def display(values):
    """Display the values as a 2-D grid.
    Parameters:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = "+".join(["-"*(width*3)]*3)
    for r in rows:
        print("".join(values[r+c].center(width)+("|" if c in "36" else "")
                      for c in cols))
        if r in "CF": print(line)
    print()