"""Test file for the generator"""
import copy
from project.solver.solver import Solver
from project.Sudoku.Sudoku import Sudoku
from project.generator.generator import Generator

test_sudoku = [[0, 0, 0, 1, 0, 5, 0, 0, 0],
              [1, 4, 0, 0, 0, 0, 6, 7, 0],
              [0, 8, 0, 0, 0, 2, 4, 0, 0],
              [0, 6, 3, 0, 7, 0, 0, 1, 0],
              [9, 0, 0, 0, 0, 0, 0, 0, 3],
              [0, 1, 0, 0, 9, 0, 5, 2, 0],
              [0, 0, 7, 2, 0, 0, 0, 8, 0],
              [0, 2, 6, 0, 0, 0, 0, 3, 5],
              [0, 0, 0, 4, 0, 9, 0, 0, 0]]

test_sudoku_diagonal = [[0, 1, 0, 0, 9, 0, 0, 0, 0],
                        [0, 4, 8, 6, 0, 1, 0, 2, 0],
                        [0, 0, 0, 3, 0, 0, 7, 6, 0],
                        [1, 0, 0, 0, 0, 0, 2, 0, 4],
                        [0, 0, 0, 7, 0, 9, 0, 0, 0],
                        [5, 0, 2, 0, 0, 0, 0, 0, 9],
                        [0, 6, 4, 0, 0, 5, 0, 0, 0],
                        [0, 7, 0, 1, 0, 2, 8, 3, 0],
                        [0, 0, 0, 0, 3, 0, 0, 5, 0]]

test_sudoku_diagonal_2 = [[0, 5, 0, 0, 3, 0, 0, 0, 0],
                          [0, 3, 8, 2, 0, 1, 0, 7, 0],
                          [0, 0, 0, 5, 0, 0, 4, 6, 0],
                          [9, 0, 0, 0, 0, 0, 2, 0, 5],
                          [0, 0, 0, 9, 0, 7, 0, 0, 0],
                          [4, 0, 2, 0, 0, 0, 0, 0, 1],
                          [0, 6, 7, 0, 0, 3, 0, 0, 0],
                          [0, 2, 0, 1, 0, 6, 8, 4, 0],
                          [0, 0, 0, 0, 9, 0, 0, 1, 0]]

def test_add_random_number_into_grid():
    """Test if adding a random number into the grid works"""
    generator = Generator()
    original_grid = copy.deepcopy(generator.generatedgrid)
    generator.add_number_into_grid(generator.generatedgrid)

    assert is_grid_updated(original_grid, generator.generatedgrid)


def test_add_specified_number_into_grid():
    """Test if adding a number to the grid in a specified location works"""
    generator = Generator()
    original_grid = copy.deepcopy(generator.generatedgrid)
    coordinates = (2, 3)
    generator.add_number_into_grid(generator.generatedgrid, coordinates)

    assert is_grid_updated(original_grid, generator.generatedgrid)

def is_grid_updated(original_grid, updated_grid):
    """Test two grids are different"""
    for i in range(len(original_grid)):
        for j in range(len(original_grid)):
            if original_grid[i][j] != updated_grid[i][j]:
                return True
    return False

def test_diagonal_switch():
    gen = Generator()
    flipped = gen.flip_along_diagonal(copy.deepcopy(test_sudoku))
    assert flipped == test_sudoku_diagonal

def test_second_diagonal_switch():
    gen = Generator()
    flipped = gen.flip_along_diagonal(copy.deepcopy(test_sudoku), diagonal_number=2)
    assert flipped == test_sudoku_diagonal_2

def test_same_sudoku():
    """Tests 'compare_solutions' with the same grid"""
    sudoku = Sudoku(test_sudoku)
    sudoku_copy = Sudoku(test_sudoku)
    gen = Generator()
    test_result = gen.compare_solutions(sudoku, sudoku_copy)

    assert test_result[0] is True
    assert test_result[1] is None

def test_different_sudoku():
    """Tests 'compare_solutions' with two different grids"""
    sudoku = Sudoku(test_sudoku)
    different_test_sudoku = copy.deepcopy(test_sudoku)
    different_test_sudoku[0][3] = 4
    sudoku_different = Sudoku(different_test_sudoku)
    gen = Generator()
    test_result = gen.compare_solutions(sudoku, sudoku_different)

    assert test_result[0] is False
    assert test_result[1] == [(0, 3)]

def test_starting_field():
    """Tests if 30 numbers are added to the grid"""
    gen = Generator(initial_values=30)
    gen.create_starting_grid()
    created_grid = gen.generatedgrid
    count_added_num = 0
    for row in range(len(created_grid)):
        for col in range(len(created_grid)):
            if created_grid[row][col] != 0:
                count_added_num += 1
    assert count_added_num == 30

def test_generator_function():
    """Tests if the entire generator works"""
    # the only way to test this that i could think of was just checking
    # if the genereted solution is unique
    gen = Generator(sudoku=Sudoku(size=4), initial_values=2)
    gen.generate_sudoku()
    flipped_grid = gen.generatedgrid[::-1]
    sud_orignial = Sudoku(gen.generatedgrid, size=4)
    sud_flipped = Sudoku(flipped_grid, size=4)
    sol_original = Solver(sud_orignial)
    sol_flipped = Solver(sud_flipped)
    sol_original.solvebrute()
    sol_flipped.solvebrute()

    assert sud_orignial.solutiongrid == sud_flipped.solutiongrid[::-1]

def test_quick_generator_function():
    """Tests if the entire quick generator works"""
    # the only way to test this that i could think of was just checking
    # if the genereted solution is unique
    gen = Generator(sudoku=Sudoku(size=4), initial_values=2)
    generated_sud = gen.quick_find_sudoku()
    flipped_grid = generated_sud[::-1]
    sud_orignial = Sudoku(generated_sud, size=4)
    sud_flipped = Sudoku(flipped_grid, size=4)
    sol_original = Solver(sud_orignial)
    sol_flipped = Solver(sud_flipped)
    sol_original.solvebrute()
    sol_flipped.solvebrute()

    assert sud_orignial.solutiongrid == sud_flipped.solutiongrid[::-1]

def test_backwards_removal():
    """checks if the result from backwards removal is solvable"""
    gen = Generator(initial_values=5)
    sudoku = Sudoku(test_sudoku)
    solving = Solver(sudoku)
    solving.solvebrute()
    solution = sudoku.solutiongrid
    solution_copy = copy.deepcopy(solution)
    reduced_solution = Sudoku(gen.backwards_removal(solution_copy))
    solving_again = Solver(reduced_solution)

    assert solving_again.solvebrute() is True

def test_solution_is_unique():
    gen = Generator()
    assert gen.solution_is_unique(test_sudoku) is True

if __name__ == '__main__':
    test_quick_generator_function()
    test_second_diagonal_switch()
