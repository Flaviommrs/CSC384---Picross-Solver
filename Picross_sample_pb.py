__author__ = 'FlavioMatheus'

from propagators import *
from cspbase import *
from picross_model import *
import struct, array

if __name__ == "__main__":

    # Picross board: First the columns list, Second the row list. Some boards are put directly in the board list, others use rows and cols as auxiliary variables. Please pay attention to this when testing boards.
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
    #board = [[[1,2],[2,1],[2,1],[1,1],[1,1,1],[2,1],[2,3]],[[3,3],[2,2],[0],[1,2,1],[1,1],[6]]]
    #8x7 strange face (same as 7x6, with an empty row and column)
    #board = [[[0],[1,2],[2,1],[2,1],[1,1],[1,1,1],[2,1],[2,3]],[[0],[3,3],[2,2],[0],[1,2,1],[1,1],[6]]]
    #dicaprio - can not do
    #rows = [[5,2,1,2,2], [3,2,2,2,2,4,2], [3,3,4,3,1,4,7], [3,4,1,2,5,2,2], [2,5,4,4,5,3,2], [2,9,4,11,8,8], [2,40,1], [2,5,25,3,2], [1,5,3,21,3,2,2], [5,2,1,7,1,3,1,2], [4,2,6,3,8,2,2], [4,2,7,1,5,2,2], [1,1,2,4,1,3,4,2,1], [1,2,3,4,1,5,1,1,3,1], [1,4,1,5,1,2,2,2,4], [1,7,2,3,1,1,1,3,2,6], [1,6,1,5,1,3,2,5], [2,5,2,2,1,6,4], [1,8,5,1,3,7], [1,9,3,1,1,8], [1,10,1,9], [11,1,10], [6,4,11,3,5], [5,6,9,5,4], [4,6,7,5,2], [3,8,5,7,1], [2,9,3,8], [2,13,1,12], [2,5,8,3,3,13,1,1], [1,4,7,8,12,7,1,2], [1,3,7,2,2,3,2,7,7,2], [1,1,4,9,1,9,8,7,2], [1,3,4,4,2,9,9,7,1], [2,3,4,4,23,7,1], [2,3,3,5,1,2,5,2,2,6,7,1], [1,4,4,4,2,2,3,2,2,5,6,1], [1,3,4,4,3,2,2,3,6,7,1], [1,3,3,4,1,16,6,6,1], [1,3,3,7,1,1,4,6,6,1], [1,3,3,8,1,2,4,5,6,1], [3,3,7,2,1,5,5,6,1], [3,3,7,4,2,6,4,5,1], [3,3,5,5,8,4,5,1], [2,3,12,10,4,6,1], [1,3,1,5,5,11,1,4,5,2], [1,3,1,5,8,7,1,4,4,1], [1,4,1,4,8,6,1,3,4,2], [1,3,2,3,1,7,5,1,4,4,1], [2,4,1,3,3,7,5,1,3,4,2], [1,3,1,3,1,1,6,5,2,2,3,1], [1,3,1,2,2,1,6,4,1,3,2,2], [1,2,4,2,2,6,4,2,2,1,2], [5,4,2,6,3,2,2,3], [2,4,3,2,4], [6,3,3,2]]
    #cols = [[2,2,4,8,6,2], [2,2,3,7,2,3,2,1], [2,2,2,5,3,11,2], [2,4,5,9,3], [2,3,4,9,3,1], [1,3,5,10,5,1], [2,7,4,9,6,1], [1,10,4,7,8,3], [2,4,4,4,7,12,1,2], [1,3,1,3,11,13,2,3], [2,3,1,14,12,2,2,1], [1,3,1,3,22,2,2,1], [1,3,1,4,19,4,3,1,1], [1,3,12,9,15,1,2], [1,3,5,2,23,1,3], [1,3,2,21,1,1,1], [2,3,1,1,20,1,1,1], [2,3,3,2,4,8,1,2,2], [2,4,5,3,5,1,3,2], [1,6,2,2,2,2,1,3,3], [2,5,2,2,8,5,4], [2,5,3,2,1,2,2,11], [1,4,2,2,1,1,3,1,12], [2,3,3,2,9,14], [2,5,2,3,6,3,4,7,1], [2,6,2,4,2,4,1,1,7,2], [9,5,1,6,1,7,2], [27,6,1,2,3,3], [2,7,5,1,6,1,5,4], [5,2,4,2,4,1,14,1], [1,5,2,3,6,4,10,1], [1,5,5,2,9,10,2], [1,6,2,2,1,1,3,1,10,2], [1,6,3,2,1,2,13,2], [1,7,1,1,18,1], [3,3,2,3,16,2], [3,4,5,7,5,3], [2,4,1,3,8,3,1], [1,4,1,11,2], [1,4,3,13,4], [4,4,2,16,7,1], [1,2,12,6,18,3], [1,2,1,3,16,15,3], [3,2,1,4,17,10,1], [1,1,3,1,3,15,6,3,1], [1,2,3,4,12,5,1], [1,2,3,4,12,7,1], [1,1,7,4,22,2], [1,1,4,4,20,2], [1,3,4,16,1], [1,1,2,4,13,2], [1,1,2,4,2,11,3], [2,2,3,2,5,3], [2,2,5,3], [1,3,2,8]]
    #board = [cols,rows]
    # Marley
    # rows = [[1,1], [2,3], [3,2,2], [1,1,3,6], [1,2,6], [1,1,5], [1,1,2,4], [3,4,4], [1,3,1,2,4,1], [2,3,3,4,2], [1,4,3,4,1], [1,1,4,3,8,3], [3,5,3,4,3,3], [4,6,3,1,3,2,3], [4,5,3,1,3,1,1,3], [5,1,3,3,1,3,2,1,3], [5,1,1,2,3,1,2,2,1,1,3], [4,2,2,1,2,1,3], [3,1,3,2,2,1,1,4,3], [1,2,2,2,2,1,1,3,3], [4,2,3,2,1,3,1,4], [5,2,2,3,1,1,1,4], [4,2,2,3,1,1,4], [4,3,3,2,1,4], [4,1,3,3,2,2,4], [3,1,2,2,2,1,5], [2,1,1,2,2,2,1,5], [1,1,1,2,2,2,1,5], [3,2,3,2,2,2,6], [3,2,2,2,3,4,6], [1,2,2,2,8,7], [3,2,2,5,2,1,5,1], [3,2,2,3,1,1,4,2], [2,2,2,4,1,1,1,1,5,2], [2,1,2,4,2,1,6,2], [2,1,2,4,4,1,6,1], [2,1,1,4,1,7,2], [1,1,1,6,8,3], [1,1,1,5,1,9,3], [2,1,7,1,2,8,3], [1,1,12,4,2,4], [1,1,12,2,3,4], [1,11,1,1,2,3,3], [1,10,1,2,2,2], [1,7,3,3,1,1,1], [1,6,2,2,2,1], [1,7,1,2,2,1,1], [1,6,1,1,1,4,1], [1,4,2,2,4,1], [1,3,1,1,3,2], [1,4,1,1,1,3,1], [5,2,1,3,2,1], [2,8,1,6,1], [1,6,1,7], [1,1,4,7], [1,3,7], [5,1,5,2], [3,5,3], [4,3,4], [4,3,2,1], [3,1,2,2], [2], [2]]
    # cols = [[4], [6,1], [8,5,2], [6,8], [6,6,3], [2,5,5], [2,1,2,1,1,2], [4,2], [5,1,2,9,5], [7,1,19], [18,1], [1,15,6], [1,1,2,1,19,1,1], [3,1,9,2,1,1], [1,13,1,3,3,2], [2,11,12,4,2,2,1], [1,8,15,15], [6,8,16,1], [7,10,23], [2,25,2,2], [1,36,3,1], [10,3,13,6,2], [12,3,1,6,10], [10,2,1,1,4,13], [9,1,3,2,3,2,2], [5,1,2,1,3,1,2,1], [4,1,2,1,2,1,1,2,1,2,2,1], [3,2,1,1,1,1,1,4], [1,1,1,1,2,1,4], [2,2,1,1,1,1,4], [1,1,2,2,1,1,2,1,6,1], [1,1,1,2,2,1,5,2,1], [1,1,6,2,2], [1,1,1,5,2,2], [1,1,1,1,11], [1,1,7], [2], [3], [1,2,2], [1,1,4], [2,1,7], [1,1,8], [1,7,4], [1,7,6,2], [14,5], [13,4], [11,4], [2,10,9], [4,12,7,1,1], [20,7,1,1,3], [20,10,2], [22,4]]
    #Bucks
    # rows = [[11], [17], [3,5,5,3], [2,2,2,1], [2,1,3,1,3,1,4], [3,3,3,3], [5,1,3,1,3,1,3], [3,2,2,4], [5,5,5,5], [23], [], [23], [1,1], [1,1], [1,2,1], [1,1,1,1], [1,1,1,1], [1,10,1,2,1], [1,1,1,1,1,1,3], [1,1,1,1,1,1,1,1], [1,1,1,1,1,1,1], [1,1,1,1,2,2], [5,5,3]]
    # cols = [[4,12], [6,1,1], [8,1,1], [3,2,2,1,1], [2,1,1,2,1,6], [1,1,1,1], [3,1,1,2,1,1], [3,2,3,1,1], [10,1,1], [4,2,2,1,1], [3,1,1,2,1,1], [2,1,1,1], [3,1,1,2,1,1], [3,2,3,1,6], [10,1,1], [4,2,2,1,1], [3,1,1,2,1,1], [1,1,1,9], [2,1,1,2,1,1], [2,2,3,1,3], [8,1,5], [6,1,1], [4,9,1], [1,1], [2,1], [1,1], [4]]
    #Cat
    rows = [[2], [2], [1], [1], [1,3], [2,5], [1,7,1,1], [1,8,2,2], [1,9,5], [2,16], [1,17], [7,11], [5,5,3], [5,4], [3,3], [2,2], [2,1], [1,1], [2,2], [2,2]]
    cols = [[5], [5,3], [2,3,4], [1,7,2], [8], [9], [9], [8], [7], [8], [9], [10], [13], [6,2], [4], [6], [6], [5], [6], [6]]
    # last forever
    # rows = [[1,2,2,2,2,2,1], [1,2,2,2,2,2,1,1], [1,1], [1,1], [1,3,1], [1,13,1], [1,13,1], [1,13,1], [1,4,4,1], [1,4,3,4,1], [1,4,5,4,1], [1,7,1], [1,7,1], [1,7,1], [1,7,1], [1,1,5,1], [1,2,6,1], [1,4,6,1], [1,6,6,1], [1,3,1], [1,1,1], [1,1], [1,1], [1,1,2,2,2,2,2,1], [1,2,2,2,2,2,1]]
    # cols = [[1,2,2,2,2,2,1], [1,1,2,2,2,2,2,1], [1,1], [1,1], [1,1], [1,2,1], [1,6,1,1], [1,6,2,1], [1,6,3,1], [1,4,8,1], [1,3,5,2,1], [1,4,8,2,1], [1,4,9,2,1], [1,4,11,1], [1,3,9,1], [1,4,8,1], [1,6,3,1], [1,6,2,1], [1,6,1,1], [1,2,1], [1,1], [1,1], [1,1], [1,2,2,2,2,2,1,1], [1,2,2,2,2,2,1]]
    #nineteen, twenty ....
    # rows = [[1,17], [1,17], [1,17], [1,17], [1,4,17], [1,5,18], [1,5,19], [1,3,3,20], [1,6,21], [1,2,4,21], [1,7,22], [1,7,22], [1,4,1,22], [1,5,9,12], [1,6,1,13], [1,2,6,13], [1,3,6,12], [1,5,13], [1,5,10], [1,5,12], [1,5,11], [1,6,7], [1,6,6], [1,6,5], [1,6,5], [2,6,5], [2,7,5], [3,8,5], [3,8,6], [4,2,10,7], [4,13,8], [5,11,9], [6,1,10,10], [7,2,1,8,11], [8,3,21], [9,28], [10,25], [10,23], [9,22], [8,1,21], [8,2,22], [7,2,25], [6,3,21], [5,3,19], [5,3,19]]
    # cols = [[45], [20], [18], [16], [1,14], [2,11], [1,2,9], [2,2,7], [2,2,2,4], [2,1,3,2], [2,6], [2,5,1,2,3], [2,5,1,2,6], [2,3,1,2,1,5], [2,4,1], [0], [1], [1,1], [1,1], [1,2,1], [1,2,1], [3,2,1], [6,3,1], [7,8,4,2], [35], [36], [39], [40], [45], [14,24], [15,16], [14,2,11], [13,2,1,11], [18,1,11], [18,2,12], [21,13], [21,14], [21,15], [22,16], [23,17], [45], [45], [45], [45], [45]]
    # Skid
    # rows = [[9], [1,1], [1,1,1], [1,3,1], [13], [13], [13], [13], [2,2], [2,2], [0], [2,2], [2,2], [2,2], [2,2], [2,2], [2,2], [2,2], [2,2], [2,2], [2,2], [2,2], [2,2], [2,2], [2,2]]
    # cols = [[2], [4,6], [9,4,4,2], [1,6,2,6], [1,5,2], [1,6], [1,5], [1,4], [1,4], [1,4,2], [1,4,6], [1,6,4,4,2], [9,2,6], [4,2]]
    #16 -   knot
    #rows = [[1,1], [2,2], [3,3], [2,1,1,2], [2,1,1,2], [1,1,1,1], [1,1,1,1], [18], [2,1,1,1,1,2], [1,1,1,1,1,1], [1,1,1,1,1,1], [26], [2,1,1,1,1,1,1,2], [2,1,1,2,2,1,1,2], [2,1,1,2,2,1,1,2], [14,14], [1,1,1,1], [1,1,1,1], [14,14], [2,1,1,2,2,1,1,2], [2,1,1,2,2,1,1,2], [2,1,1,1,1,1,1,2], [26], [1,1,1,1,1,1], [1,1,1,1,1,1], [2,1,1,1,1,2], [18], [1,1,1,1], [1,1,1,1], [2,1,1,2], [2,1,1,2], [3,3], [2,2], [1,1]]
    #cols = [[1,1], [2,2], [3,3], [2,1,1,2], [2,1,1,2], [1,1,1,1], [1,1,1,1], [18], [2,1,1,1,1,2], [1,1,1,1,1,1], [1,1,1,1,1,1], [26], [2,1,1,1,1,1,1,2], [2,1,1,2,2,1,1,2], [2,1,1,2,2,1,1,2], [14,14], [1,1,1,1], [1,1,1,1], [14,14], [2,1,1,2,2,1,1,2], [2,1,1,2,2,1,1,2], [2,1,1,1,1,1,1,2], [26], [1,1,1,1,1,1], [1,1,1,1,1,1], [2,1,1,1,1,2], [18], [1,1,1,1], [1,1,1,1], [2,1,1,2], [2,1,1,2], [3,3], [2,2], [1,1]]
    #20x20 smoke
    #rows = [[1,3,2,1], [1,2,2], [3,4], [2,3,2], [2,1,6], [2,13,1], [1,1,8], [2,1,1,7], [1,2,2,2,3], [3,1,1,1,3], [1,2,1,1,3], [2,1,1,3], [1,5,5], [1,1,3], [4,2], [2,2,1,2,1], [2,1,2,3,2], [4,1,6,1], [3,4,3,2], [4,2]]
    #cols = [[2,2,1], [1,6,4,4], [3,3,1,1,4], [2,2], [1,3,3,3], [1,1,1,2,1,2], [2,1,1,1,1], [2,4,3,3], [3,1,2,3,1], [1,4,2,1], [3,1,2], [2,1,1], [3,3], [7,4], [5,4], [3,2,1,3], [3,4,1], [9,2], [8,3], [1,8,2]]
    #19x19 domino
    #rows = [[3], [1], [3,1], [1], [3,1], [1], [3,1], [1], [3,1], [1], [3,1], [1], [3,1], [1], [3,1], [1], [3,1], [1], [1]]
    #cols = [[1], [1], [1,3], [1], [1,3], [1], [1,3], [1], [1,3], [1], [1,3], [1], [1,3], [1], [1,3], [1], [1,3], [1], [3]]
    #34x40 mum
    #rows = [[12], [5,2,5], [5,2,2,5], [1,2,2,2,2,2,1], [4,2,2,4,2,2,4], [4,2,2,4,2,2,4], [1,2,2,2,2,2,1], [6,2,2,2,2,2,6], [6,2,2,2,2,2,6], [1,14,1], [10,10], [8,3,3,8], [1,1,2,1,1,2,1,1], [9,2,2,2,2,9], [9,9], [1,1,1,1,1,1], [12,2,12], [12,12], [1,1,4,1,1], [14,14], [12,12], [2,1,4,1,2], [9,4,9], [1,7,4,7,1], [1,1,1,4,1,1,1], [1,7,4,7,1], [1,7,4,7,1], [1,2,1,2,1,2,1], [1,7,2,7,1], [1,1,6,2,6,1,1], [1,1,1,1,2,1,1,1,1], [1,1,6,2,6,1,1], [1,1,5,5,1,1], [1,1,1,8,1,1,1], [1,1,4,4,1,1], [1,2,6,2,1], [2,4,4,2], [2,6,2], [4,4], [6]]
    #cols = [[5], [3,2,1], [3,2,2,1], [3,2,2,2,2], [3,2,2,2,2,3], [1,2,2,2,2,2,16], [1,2,2,2,2,2,2,1,2], [1,2,2,2,2,2,2,13,1], [3,2,2,2,2,2,2,4,1,1], [6,5,2,2,2,2,6,1,1], [1,7,3,2,2,2,2,2,1,1,1], [3,4,1,2,2,2,2,2,2,1,1,1], [6,1,2,3,2,2,2,2,1,1,1], [1,7,2,16,1,1], [1,4,1,1,1,1,1,1,1,1,1], [1,2,1,3,1,1,6,1,1,1,1], [2,7,1,1,11,1,1,1,1], [2,7,1,1,11,1,1,1,1], [1,2,1,3,1,1,6,1,1,1,1], [1,4,1,1,1,1,1,1,1,1,1], [1,7,2,16,1,1], [6,1,2,3,2,2,2,2,1,1,1], [3,4,1,2,2,2,2,2,2,1,1,1], [1,7,3,2,2,2,2,2,1,1,1], [6,5,2,2,2,2,6,1,1], [3,2,2,2,2,2,2,4,1,1], [1,2,2,2,2,2,2,13,1], [1,2,2,2,2,2,2,1,2], [1,2,2,2,2,2,16], [3,2,2,2,2,3], [3,2,2,2,2], [3,2,2,1], [3,2,1], [5]]
    #23x20 animals go to heaven id:131
    #rows = [[7], [11], [13], [15], [15], [17], [3,5,3], [2,3,2], [3,2,1,2,3], [4,2,2,4], [5,5], [5,5], [6,3,6], [5,1,5], [3,3], [3,1,1,3], [1,2,2,1], [1,5,1], [2,2], [7]]
    #cols = [[2], [4], [4], [9], [5,6], [5,5], [5,2,7], [5,2,2,1], [6,1,2,1], [7,2,1], [8,1,1,1], [9,2,1,1], [8,1,1,1], [7,2,1], [6,1,2,1], [5,2,2,1], [5,2,7], [5,5], [5,6], [9], [4], [4], [2]]

    #THIS LINE SHOULD BE COMMENTED ONLY IF YOU ARE NOT USING THE ROWS AND COLS AUXILIARY VARIABLES.
    board = [cols,rows]

    #This is used only on colored picrosses. It stays here just to have the if condition below unchanged.
    boards = list()

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
