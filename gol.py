import sys
import os.path

from collections import defaultdict, namedtuple
from copy import deepcopy

# named tuple for set of live cells
Grid = namedtuple("Grid", ["cells"])
# named tuple for sets of alive and dead neighbors for a given cell
Neighbours = namedtuple("Neighbours", ["alive", "dead"])


def get_cells_stdin():
    '''
        Reads stdin and returns a set of tuples with integer coordinates for live cells
    '''

    cells = set()

    # read input from stdin
    print("Specify state in Life 1.06 format. Use Ctrl d to stop the input.")
    data = sys.stdin.read()

    lines = [line.strip() for line in data.split('\n') if line]

    # check header
    if lines[0] != '#Life 1.06':
        raise ValueError('Input is not in Life 1.06 format')
    else:
        cells = set([(int(l.split(' ')[0]), int(l.split(' ')[1])) for l in lines[1:]])

    # check 64 bit integer signed range
    for c in cells:
        if c[0] > 9223372036854775807 or c[1] > 9223372036854775807 or c[0] < -9223372036854775808 or c[
            1] < -9223372036854775808:
            raise ValueError('Input is not in 64 bit signed range')

    return cells


def get_cells_file():
    '''
        Reads input file and returns a set of tuples with integer coordinates for live cells
    '''

    cells = set()

    # parse command line
    if len(sys.argv) > 1:
        # check if input filename is a file
        if os.path.isfile(sys.argv[1]):
            filename = sys.argv[1]

            with open(filename) as file:
                lines = [line.strip() for line in file]

                # check header
                if lines[0] != '#Life 1.06':
                    raise ValueError('Input is not in Life 1.06 format')
                else:
                    cells = set([(int(l.split(' ')[0]), int(l.split(' ')[1])) for l in lines[1:]])

    # check 64 bit integer signed range
    for c in cells:
        if c[0] > 9223372036854775807 or c[1] > 9223372036854775807 or c[0] < -9223372036854775808 or c[
            1] < -9223372036854775808:
            raise ValueError('Input is not in 64 bit signed range')

    return cells


def get_neighbours(grid: Grid, x: int, y: int) -> Neighbours:
    '''
        Returns alive and dead sets of neighbors for a given cell
    '''

    offsets = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
    possible_neighbours = {(x + x_add, y + y_add) for x_add, y_add in offsets}
    alive = {(pos[0], pos[1]) for pos in possible_neighbours if pos in grid.cells}

    return Neighbours(alive, possible_neighbours - alive)


def update_grid(grid: Grid) -> Grid:
    # copy grid to store previous state
    new_cells = deepcopy(grid.cells)

    # default dictionary of integers where the keys are the dead cell coordinates and values are the number of live neighbours of that  dead cell
    undead = defaultdict(int)

    for (x, y) in grid.cells:
        # find neighbors for each live cell in grid
        alive_neighbours, dead_neighbours = get_neighbours(grid, x, y)

        # check if the current live cell has either two or three neighbours, if not kill the live cell
        if len(alive_neighbours) not in [2, 3]:
            new_cells.remove((x, y))

        # increment values in undead for number of live neighbors
        for pos in dead_neighbours:
            undead[pos] += 1

    # for dead cells with three live neighbours we birth them and add them to the new grid
    for pos, _ in filter(lambda elem: elem[1] == 3, undead.items()):
        new_cells.add((pos[0], pos[1]))

    return Grid(new_cells)


def main():
    # initialize grid
    if len(sys.argv) > 1:
        # run with input file
        grid = Grid(get_cells_file())
    else:
        # run with stdin
        grid = Grid(get_cells_stdin())

    if not grid.cells:
        # live cells were not read
        print('No live cells initialized')
    else:
        input = grid

        # run gol for 10 iterations
        for i in range(10):
            input = update_grid(input)

    # write output
    if len(sys.argv) > 1:
        # write to output file
        filename = f"{sys.argv[1].split('.')[0]}_output.lif"
        with open(filename, 'w') as f:
            f.write('#Life 1.06\n')
            for c in input.cells:
                f.write(f"{c[0]} {c[1]}\n")
    else:
        # print to stdout
        print('#Life 1.06')
        for c in input.cells:
            print(f"{c[0]} {c[1]}")


if __name__ == '__main__':
    main()
