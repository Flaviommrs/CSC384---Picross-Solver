__author__ = 'FlavioMatheus'

from propagators import *
from cspbase import *
from picross_model import *
import struct, array

if __name__ == "__main__":
    boards = list()
    #picross basic color model
    '''
    rows1 = [[0],[1],[0],[0],[1]]
    cols1 = [[0],[0],[0],[0],[1],[0],[1]]
    board1 = [cols1,rows1]
    rows2 = [[2],[2,1],[4],[2],[0]]
    cols2 = [[1],[2],[2],[2],[2],[2],[0]]
    board2 = [cols2,rows2]
    boards = [board1,board2]
    colors = [[255,0,0],[0,0,255]]
    '''
    #end of picross basic color example

    #   color mario
    #brown
    cols1 = [[3],[1,1],[3],[1,1],[0],[0],[2,1],[2],[1],[1],[0]]
    rows1 = [[0],[0],[3,1],[1,1,1],[1,2,1],[2,4],[0]]
    board1 = [cols1,rows1]
    #yellow
    cols2 = [[0],[2],[2],[1,2],[5],[5],[1,1],[2,1],[2,1],[2],[1]]
    rows2 = [[0],[0],[2,1],[1,3,3],[1,3,3],[4],[7]]
    board2 = [cols2,rows2]
    #red
    cols3 = [[0],[1],[2],[2],[2],[2],[2],[1],[1],[1],[0]]
    rows3 = [[5],[9],[0],[0],[0],[0],[0]]
    board3 = [cols3,rows3]

    boards = [board1,board2,board3]

    colors = [[128,0,0],[255,255,0],[255,0,0]]
    # end of color mario

    if len(boards) > 1:
        color_picross_basic_solver(boards,colors)
    else:
        csp, variable_array = picross_model(board)
        solver  = BT(csp)
        print("=========================================================")
        print("Using GAC")
        solver.bt_search(prop_GAC)
        print("Solution")
        print_Picross(variable_array)
        print("=========================================================")
