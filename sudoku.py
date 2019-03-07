# Rows: A,B,C,D,E,F,G,H,I
# Columns: 1,2,3,4,5,6,7,8,9
# Cells: A1, A2, A3, ..., B1, B2, ....

rows = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'}
cols = {'1', '2', '3', '4', '5', '6', '7', '8', '9'}

def generate_cells(R,C):
    """
    Generates the cross product of the elements in A and B
    :param R: rows
    :param C: columns
    :return: the cross product of the 2 sets
    """
    return {r+c for r in R for c in C}


def generate_single_cell_dependencies(i, j):
    """
    Generates the set of all dependencies for a single cell
    eg: Value of B2 is dependant on Bi (for i = 1,3,..,9),
                                    j2 (for j = A,C,..,I) and
                                    [A1,A3,C1,C3] ==> 20 squares
    :param i: row index
    :param j: column index
    :return: the set of valid dependencies for cell ij
    """
    dependency_set = set()
    for r in rows - {i}:
        dependency_set.add(r+j)
    for c in cols - {j}:
        dependency_set.add(i+c)
    rows_3_by_3 = set()
    cols_3_by_3 = set()
    if i in {'A','B','C'}:
        rows_3_by_3.update({'A','B','C'})
    if i in {'D','E','F'}:
        rows_3_by_3.update({'D','E','F'})
    if i in {'G','H','I'}:
        rows_3_by_3.update({'G','H','I'})
    if j in {'1','2','3'}:
        cols_3_by_3.update({'1','2','3'})
    if j in {'4','5','6'}:
        cols_3_by_3.update({'4','5','6'})
    if j in {'7','8','9'}:
        cols_3_by_3.update({'7','8','9'})
    square_3_by_3 = generate_cells(rows_3_by_3, cols_3_by_3)
    for cell in square_3_by_3:
        dependency_set.add(cell)
    return dependency_set - {i+j}


def generate_all_dependencies():
    """
    Generates the set of all dependencies
    eg: Value of B2 is dependant on Bi (for i = 1,3,..,9),
                                    j2 (for j = A,C,..,I) and
                                    [A1,A3,C1,C3] ==> 20 squares
    :return: the set of valid dependencies
    """
    all_dependencies = list()
    for i in rows:
        for j in cols:
            all_dependencies.append(generate_single_cell_dependencies(i, j, rows, cols))
    return all_dependencies


def is_full(puzzle):
    """
    Checks if any cell is left to be assigned
    :param puzzle: the puzzle!
    :return: true / false
    """
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] is '-':
                return False
    return True


def get_first_unassigned(puzzle):
    """
    Finds the first position in the puzzle with '-'
    :param puzzle: the sudoku!
    :return: a tuple indicating the location
    """
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] is '-':
                return (i,j)


def get_cell_index(r, c):
    """
    Generates the cell index as say, A1 --> 0,0 ....
    :param r: row
    :param c: col
    :return: index
    """
    i = ord(r) - 65
    j = ord(c) - 49
    return (i,j)


def is_safe_assignment(puzzle, num, i, j):
    """
    Checks if an assignment to a cell is valid or not
    :param puzzle: the sudoku
    :param num: the value under consideration
    :param i: row index
    :param j: column index
    :return: True or False
    """
    index_i = chr(i+65)
    index_j = chr(j+49)
    dependency_set = generate_single_cell_dependencies(index_i,index_j)

    impossible_values = set()
    for cell in dependency_set:
        (i, j) = get_cell_index(cell[0], cell[1])
        impossible_values.add(puzzle[i][j])
    if chr(num+48) in impossible_values:
        return False
    else:
        return True


def solve_puzzle(puzzle):
    """
    Solves the sudoku
    :param puzzle: the sudoku!
    :return: True or False
    """
    if is_full(puzzle): # SOLVED !!!
        return True

    (i,j) = get_first_unassigned(puzzle)

    for num in range(1,10):
        if is_safe_assignment(puzzle, num, i, j):
            puzzle[i][j] = chr(num+48)
            if solve_puzzle(puzzle):
                return True
            puzzle[i][j] = '-'
    return False


def pretty_print_row(row):
    """
    Print row in a neat fashion
    :param row: a row of the puzzle
    :return: String
    """
    string = '| '
    for i in range(0,9):
        string = string + row[i] + ' | '
    return string


def pretty_print_line():
    """
    Print a line
    :return: String
    """
    return '|-----------------------------------|'


def pretty_print(puzzle):
    """
    Print in a neat fashion
    :param puzzle: puzzle
    :return: None
    """
    f = open('/home/vishakhs/AI_assignments/output.txt','w')
    f.write(pretty_print_line())
    f.write("\n")
    for i in range(0,9):
        f.write(pretty_print_row(puzzle[i]))
        f.write("\n")
        f.write(pretty_print_line())
        f.write("\n")


def main():
    with open('/home/vishakhs/AI_assignments/input.txt') as textFile:
        puzzle = [line.split() for line in textFile]

    if(solve_puzzle(puzzle)):
        pretty_print(puzzle)
    else:
        print("No solution exists for the given Soduko")


if __name__ == "__main__":
    main()