[//]: # (Image References)

[image1]: ./images/board.png "Sudoku board"
[image2]: ./images/diagonal.png "Diagonal Sudoku"
[image3]: ./images/labels.png "labels"
[image4]: ./images/peers.png "peers"


# Solve Sudoku with Artificial Intelligence

## Synopsis

This project applies an AI concept called [Constraint Propagation](https://en.wikipedia.org/wiki/Constraint_satisfaction) to solve _diagonal_ Sudoku puzzles. See the final section in this README document **Sudoku explained** for an overview of Sudoku, diagonal Sudoku and relevant terminologies.

### Key AI concept: Constraint propagation
Below is an explanation of how constraint propagation is applied to solve the naked twins problem and the diagonal Sudoku problem (see `solution.py` for the implementation and **Sudoku explained** for an overview):

* The naked twins problem: Each box must have a different value from the rest of the boxes in the same unit. So if two boxes have naked twins as possibilities, we can remove these possibilities from the rest of the boxes in the same unit. As we do so, we recompute the possible value sets across the unit. When we apply Naked Twins strategy, together with Eliminate and Only Choice, repeatedly, we will likely reach a solution to the Sudoku.
* The diagonal Sudoku problem: When we add diagonal units to both the unit and peer dictionaries, all the functions such as `naked_twins`, `eliminate` and `only_choice` will take into account this new constraint. As we apply these functions repeatedly, this constraint ensures the resulting board will have a unique value for each box on each diagonal.

## Code

* `solution.py` - Solves a diagonal Sudoku puzzle and visualizes the solution.
* `solution_test.py` - Tests `solution.py`.
* `PySudoku.py` and `visualize.py`- Helper files for visualizing the solution. They are not to be run separately, but will be called when running `solution.py`.

## Setup

You need the following:

* Python 3
* [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
* The AIND environment provided in the Anaconda lesson of Udacity's AIND Nanodegree (also available in this repo `aind-universal.yml`)
* **pygame** is needed to see the visualization. It is available in the AIND environment or installed separately from [here](http://www.pygame.org/download.shtml).

## Run

To activate an Anaconda environment (OS X or Unix/Linux), use:
    
`source activate <environment_name>`

To run any script file, use:

`python <script.py>`

## Sudoku explained

Sudoku consists of a 9x9 grid, and the objective is to fill the grid with digits in such a way that each row, each column, and each of the 9 principal 3x3 subsquares contains all of the digits from 1 to 9. The detailed rules can be found, for example, [here](http://www.conceptispuzzles.com/?uri=puzzle/sudoku/rules).
Basic rules:

* If a box has a value, then all the boxes in the same row, same column, or same 3x3 square cannot have that same value.
* If there is only one allowed value for a given box in a row, column, or 3x3 square, then the box is assigned that value.

![Sudoku board][image1]

### Diagonal Sudoku

A diagonal Sudoku puzzle is identical to traditional Sudoku puzzles with the added constraint that the boxes on the two main diagonals of the board must also contain the digits 1-9 in each cell (just like the rows, columns, and 3x3 blocks)

![Diagonal Sudoku][image2]

### Naked twins

See [this link](http://www.sudokudragon.com/tutorialnakedtwins.htm) for an explanation.

### Naming conventions

**Rows and columns**

* The rows will be labelled by the letters A, B, C, D, E, F, G, H, I.
* The columns will be labelled by the numbers 1, 2, 3, 4, 5, 6, 7, 8, 9. In the below diagram we can see the unsolved and solved puzzles with the labels for the rows and columns.
* The 3x3 squares won't be labelled, but in the diagram, they can be seen with alternating colors of grey and white.

![labels][image3]

**Boxes, units and peers**

* The individual squares at the intersection of rows and columns will be called _boxes_. These boxes will have labels 'A1', 'A2', ..., 'I9'.
* The complete rows, columns, and 3x3 squares, will be called _units_. Thus, each unit is a set of 9 boxes, and there are 27 units in total.
* For a particular box (such as 'A1'), its _peers_ will be all other boxes that belong to a common unit (namely, those that belong to the same row, column, or 3x3 square).

Let's see an example. In the grids below, the set of highlighted boxes represent _units_. Each grid shows a different _peer_ of the box at E3.

![peers][image4]

Source: udacity[https://www.udacity.com/]
