__author__ = 'FlavioMatheus'

from propagators import *
from cspbase import *
from sudoku_csp import *

def print_Picross(variables):
    for row in variables:
        #print(["T" if var.get_assigned_value() == True else "F" for var in row])
        for variable in row:
            if(variable.get_assigned_value()):
                print("XX",end="")
            else:
                print("  ",end="")
        print("")

if __name__ == "__main__":

    # Picross board: First the columns list, Second the row list
    #GOOMBA
    #board = [[[5,2],[9,3],[1,2,1,3],[1,1,5],[3,1,1,3],[4,2,1,1,2],[6,2,1,1],[9,1,1],[6,2,1,1],[4,2,1,1,2],[3,1,1,3],[1,1,5],[1,2,1,3],[9,3],[5,2]],[[5],[7],[13],[1,7,1],[1,3,1],[2,5,2],[2,1,1,1,2],[3,3,3],[15],[2,2],[13],[1,1],[4,4],[15],[6,6]]]
    #EDGE
    #board = [[[1],[3],[1],[2,2],[2],[4],[1],[3],[3],[1]],[[1],[3],[1],[2],[1],[3],[3],[1],[2],[2],[4]]]
    #DANCER
    #board = [[[2,1],[2,1,3],[7],[1,3],[2,1]],[[2],[2,1],[1,1],[3],[1,1],[1,1],[2],[1,1],[1,2],[2]]]
    #4x4 X (multiple solutions)
    #board = [[[1,1],[2],[2],[1,1]],[[1,1],[2],[2],[1,1]]]
    #5x5 X
    #board = [[[1,1],[1,1],[3],[1,1],[1,1]],[[1,1],[3],[1],[3],[1,1]]]
    #5x7 turtle
    #board = [[[1,1],[3,1],[3,2],[3,1],[1,1]],[[1,1],[3],[3],[3],[1,1],[3],[1]]]
    #7x6 strange face
    board = [[[1,2],[2,1],[2,1],[1,1],[1,1,1],[2,1],[2,3]],[[3,3],[2,2],[0],[1,2,1],[1,1],[6]]]
    #8x7 strange face (same as 7x6, with an empty row and column)
    board = [[[0],[1,2],[2,1],[2,1],[1,1],[1,1,1],[2,1],[2,3]],[[0],[3,3],[2,2],[0],[1,2,1],[1,1],[6]]]
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

