from data.aquarium import *
from data.cell import *
from data.puzzle import *


def read_puzzle(filename):
    """Reads a puzzle in a file with name 'filename'

    Parameters:

    filename: name of the file that contains the puzzle

    Returns:
    The puzzle present in the file
    """

    file = open(filename, 'r')

    # Reading the size of the puzzle
    size = read_size(file)

    # Reading the aquariums
    aquariums = read_aquariums(file)

    # Reading the limits 
    limits = read_limits(file)

    file.close()

    return Puzzle(size, aquariums, limits)


def read_size(file):

    sizes = read_and_split(file)
    n_rows = int(sizes[0])
    
    return n_rows


def read_aquariums(file):
    aquariums = []
    n_aqs = int(read_and_split(file)[0])
    for i in range(n_aqs):

        line = read_and_split(file)

        aquarium = create_aquarium(line)
        
        aquariums.append(aquarium)

    return aquariums


def create_aquarium(line):
    id = int(line[0])    
    max_level = int(line[1])

    aq = Aquarium(id, max_level)

    for i in range(2, len(line)):
        pos = get_pos(line[i])

        cell = Cell(pos)

        aq.add_cell(cell)

    return aq


def read_limits(file):
    line = read_and_split(file)

    # Converting the list of strings to a list of integers
    horz_limits = [int(n) for n in line]

    line = read_and_split(file)

    # Converting the list of strings to a list of integers
    vert_limits = [int(n) for n in line]

    return [horz_limits, vert_limits]


def read_and_split(file):
    """Reads a line of the file and splits it into a list of strings

    Parameters:

    file: the file

    Returns:
    A list of strings
    """

    line = file.readline()
    return line.split()


def get_pos(pos_string):
    """Converts a string if the position of the cell to a tuple with the same information

    Parameters:

    pos_string: the position, in a string

    Returns:
    A tuple with the position
    """

    tpl_str = tuple(pos_string)
    return (int(tpl_str[0]), int(tpl_str[1]))