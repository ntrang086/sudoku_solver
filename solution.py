"""Implement a solution to a diagonal Sudoku problem using
Depth-first search and Constraint Propagation"""

import sys
from utils import rows, cols, boxes, assignments, assign_value, cross, grid_values, display

# Encode the board: units and peers
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ("ABC","DEF","GHI") for cs in ("123","456","789")]
diagonal_units = [[rows[i] + cols[i] for i in range(9)]] + [[rows[i] + cols[::-1][i] for i in range(9)]]
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    
    Parameters:
    values(dict)
        a dictionary of the form {"box_name": "123456789", ...}
    Returns:
    dict
        The values dictionary with the naked twins eliminated from peers
    """
    for unit in unitlist:
        for box in unit:
            # Look for boxes that have 2 digits
            if len(values[box]) == 2:
                # Search for a twin of the current box
                for peer in unit:
                    if box != peer and values[box] == values[peer]:
                        # Eliminate the naked twins as possibilities for their peers
                        for peer2 in unit:
                            if peer2 != box and peer2 != peer:
                                values = assign_value(values, peer2, values[peer2].replace(values[box][0],""))
                                values = assign_value(values, peer2, values[peer2].replace(values[box][1],""))
    return values

def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle: if a box has a value 
    assigned, none of the peers of that box can have the same value.
    
    Parameters:
    values(dict)
        a dictionary of the form {"box_name": "123456789", ...}
    Returns:
    dict
        The values dictionary with the assigned values eliminated from peers
    """
    single_values = []
    for box in values.keys():
        if len(values[box]) == 1:
            single_values.append(box)
    for box in single_values:
        value = values[box]
        for peer in peers[box]:
            values = assign_value(values, peer, values[peer].replace(value,""))
    return values

def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle: if only one box in 
    a unit allows a certain digit, that box must be assigned that digit.

    Parameters:
    values(dict)
        a dictionary of the form {"box_name": "123456789", ...}
    Returns:
    dict
        The values dictionary with all single-valued boxes assigned
    """
    for unit in unitlist:
        for digit in "123456789":
            pos = []
            for box in unit:
                if digit in values[box]:
                    pos.append(box)
            if len(pos) == 1:
                values = assign_value(values, pos[0], digit)
    return values

def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies.

    Parameters:
    values(dict)
        a dictionary of the form {"box_name": "123456789", ...}
    Returns:
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable 
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Use the Eliminate Strategy
        values = eliminate(values)

        # Use the Only Choice Strategy
        values = only_choice(values)

        # Use the Naked Twins Strategy
        values = naked_twins(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    """Apply depth-first search in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    Parameters:
    values(dict)
        a dictionary of the form {"box_name": "123456789", ...}
    Returns:
    dict or False
        The values dictionary with all boxes assigned or False
    """    
    # First, reduce the puzzle
    values = reduce_puzzle(values)
    if values is False:
        return False
    if all(len(values[s]) == 1 for s in boxes):
        return values
    # Choose one of the unfilled squares with the fewest possibilities
    min_possibility = sys.maxsize
    min_box = ""
    for box in boxes:
        if len(values[box]) > 1 and len(values[box]) < min_possibility:
            min_possibility = len(values[box])
            min_box = box
    # Use recursion to solve each one of the resulting sudokus, and 
    # if one returns a value (not False), return that answer
    for digit in values[min_box]:
        new_values = values.copy()
        new_values[min_box] = digit
        attempt = search(new_values)
        if attempt:
            return attempt

def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation.
    
    Parameters:
    grid(string)
        a string representing a sudoku grid.
        
        Ex. "2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3"
    Returns:
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    return search(grid_values(grid))


if __name__ == "__main__":
    diag_sudoku_grid = "2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3"
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print("We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.")