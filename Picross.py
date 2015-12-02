__author__ = 'FlavioMatheus'

from propagators import *
from cspbase import *
from sudoku_csp import *

def print_Picross(variables):
    for row in variables:
        print(["T" if var.get_assigned_value() == True else "F" for var in row])

if __name__ == "__main__":

    # Picross board: First the columns list, Second the row list
    board = [[[5,2],[9,3],[1,2,1,3],[1,1,5],[3,1,1,3],[4,2,1,1,2],[6,2,1,1],[9,1,1],[6,2,1,1],[4,2,1,1,2],[3,1,1,3],[1,1,5],[1,2,1,3],[9,3],[5,2]],[[5],[7],[13],[1,7,1],[1,3,1],[2,5,2],[2,1,1,1,2],[3,3,3],[15],[2,2],[13],[1,1],[4,4],[15],[6,6]]]

    csp, variable_array = picross_model(board)
    solver  = BT(csp)
    print("=========================================================")
    print("Using GAC")
    solver.bt_search(prop_GAC)
    print("Solution")
    print_Picross(variable_array)
    print("=========================================================")
    print("Using Foward Check")
    solver.bt_search(prop_FC)
    print_Picross(variable_array)

