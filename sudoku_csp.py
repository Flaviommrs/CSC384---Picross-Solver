#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the warehouse domain.

'''
Construct and return sudoku CSP models.
'''

from cspbase import *
import itertools
import propagators as my_propagators
import copy

def all_combinations_aux(sum, buckets):
    if(sum == 0):
        yield buckets
    elif(len(buckets) == 1):
        buckets[0] = list()
        buckets[0].append(sum)
        yield buckets
    else:
        middle = len(buckets)//2
        b1 = sum
        while(b1 >= 0):
            for result1 in all_combinations_aux(b1,buckets[:middle]):
                for result2 in all_combinations_aux(sum-b1,buckets[middle:]):
                    result = result1 + result2
                    yield result
            b1-=1

def all_combinations(sum, buckets):
    for combination in all_combinations_aux(sum,buckets):
        for bucket in combination:
            if len(bucket) == 0:
                bucket.append(0)
        yield combination




def same_group(i,j):
    return (i<=3 and j<=3) or (i>3 and i<=6 and j>3 and j<=6) or (i>6 and j>6)

def has_con_mod1(celli, cellj):
    celli_i = (celli) // 9 + 1
    celli_j = (celli) % 9 + 1
    cellj_i = (cellj) // 9 + 1
    cellj_j = (cellj) % 9 + 1


    if(celli_i == cellj_i):
        return True
    if(celli_j == cellj_j):
        return True
    if(same_group(celli_i,cellj_i) and same_group(celli_j,cellj_j)):
        return True

    #print('celli_i = ' + str(celli_i) + ' cell_i_j = ' + str(celli_j) + ' cell_j_i = ' + str(cellj_i) + ' cell_j_j = ' + str(cellj_j))
    return False

def sudoku_csp_model_1(initial_sudoku_board):
    '''Return a CSP object representing a sudoku CSP problem along
       with an array of variables for the problem. That is return

       sudoku_csp, variable_array

       where sudoku_csp is a csp representing sudoku using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the sudokup board (indexed from (0,0) to (8,8))



       The input board is specified as a list of 9 lists. Each of the
       9 lists represents a row of the board. If a 0 is in the list it
       represents an empty cell. Otherwise if a number between 1--9 is
       in the list then this represents a pre-set board
       position. E.g., the board

       -------------------
       | | |2| |9| | |6| |
       | |4| | | |1| | |8|
       | |7| |4|2| | | |3|
       |5| | | | | |3| | |
       | | |1| |6| |5| | |
       | | |3| | | | | |6|
       |1| | | |5|7| |4| |
       |6| | |9| | | |2| |
       | |2| | |8| |1| | |
       -------------------
       would be represented by the list of lists

       [[0,0,2,0,9,0,0,6,0],
       [0,4,0,0,0,1,0,0,8],
       [0,7,0,4,2,0,0,0,3],
       [5,0,0,0,0,0,3,0,0],
       [0,0,1,0,6,0,5,0,0],
       [0,0,3,0,0,0,0,0,6],
       [1,0,0,0,5,7,0,4,0],
       [6,0,0,9,0,0,0,2,0],
       [0,2,0,0,8,0,1,0,0]]


       This routine returns Model_1 which consists of a variable for
       each cell of the board, with domain equal to {1-9} if the board
       has a 0 at that position, and domain equal {i} if the board has
       a fixed number i at that cell.

       Model_1 also contains BINARY CONSTRAINTS OF NOT-EQUAL between
       all relevant variables (e.g., all pairs of variables in the
       same row, etc.), then invoke enforce_gac on those
       constraints. All of the constraints of Model_1 MUST BE binary
       constraints (i.e., constraints whose scope includes two and
       only two variables).
    '''
    dom = []
    for i in range(9):
        dom.append(i+1)

    variable_array = []
    vars = []
    for i in dom:
        var_line=[]
        for j in dom:
            if(initial_sudoku_board[i-1][j-1]==0):
                vars.append(Variable('Cell {}-{}'.format(i,j), dom))
                var_line.append(vars[-1])
            else:
                dom_init = list()
                dom_init.append(initial_sudoku_board[i-1][j-1])
                vars.append(Variable('Cell {}-{}'.format(i,j), dom_init))
                var_line.append(vars[-1])
                vars[-1].assign(initial_sudoku_board[i-1][j-1])
        variable_array.append(var_line)

    cons = []

    '''
    sat_tuples = []
    for i in range(9):
        for j in range(9):
            if i != j:
                t = (i+1,j+1)
                sat_tuples.append(t)
    '''

    for celli in range(80):
        for cellj in range(celli+1, 81):
            if has_con_mod1(celli,cellj):
                con = Constraint("C(Cell {}-{},Cell {}-{})".format( str((celli)//9 + 1), str((celli)%9 + 1), str((cellj)//9 + 1), str((cellj)%9 + 1)),[vars[celli], vars[cellj]])
                sat_tuples = []
                for i in vars[celli].cur_domain():
                    for j in vars[cellj].cur_domain():
                        if i != j:
                            t = (i,j)
                            sat_tuples.append(t)
                con.add_satisfying_tuples(sat_tuples)
                cons.append(con)

    sudoku_csp = CSP("Sudoku Model_1", vars)
    for c in cons:
        sudoku_csp.add_constraint(c)

    return sudoku_csp, variable_array

#IMPLEMENT

##############################

def sudoku_csp_model_2(initial_sudoku_board):
    '''Return a CSP object representing a sudoku CSP problem along
       with an array of variables for the problem. That is return

       sudoku_csp, variable_array

       where sudoku_csp is a csp representing sudoku using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the sudokup board (indexed from (0,0) to (8,8))

    The input board takes the same input format (a list of 9 lists
    specifying the board as sudoku_csp_model_1.

    The variables of model_2 are the same as for model_1: a variable
    for each cell of the board, with domain equal to {1-9} if the
    board has a 0 at that position, and domain equal {i} if the board
    has a fixed number i at that cell.

    However, model_2 has different constraints. In particular, instead
    of binary non-equals constaints model_2 has 27 all-different
    constraints: all-different constraints for the variables in each
    of the 9 rows, 9 columns, and 9 sub-squares. Each of these
    constraints is over 9-variables (some of these variables will have
    a single value in their domain). model_2 should create these
    all-different constraints between the relevant variables, then
    invoke enforce_gac on those constraints.
    '''
    dom = []
    for i in range(9):
        dom.append(i+1)

    variable_array = []
    vars = []
    for i in dom:
        var_line=[]
        for j in dom:
            if(initial_sudoku_board[i-1][j-1]==0):
                vars.append(Variable('Cell {}-{}'.format(i,j), dom))
                var_line.append(vars[-1])
            else:
                dom_init = list()
                dom_init.append(initial_sudoku_board[i-1][j-1])
                vars.append(Variable('Cell {}-{}'.format(i,j), dom_init))
                var_line.append(vars[-1])
                vars[-1].assign(initial_sudoku_board[i-1][j-1])
        variable_array.append(var_line)

    cons = []

    '''
    sat_tuples = []
    for my_tuple in itertools.permutations(dom):
        sat_tuples.append(my_tuple)
    '''

    #9 constraints for lines
    for celli in range(9):
        line = []
        for cellj in range(9):
            line.append(vars[celli*9+cellj])
        con = Constraint("C(Line{})".format(str(celli+1)),line)

        sat_tuples = list()
        sat_tuples.append(())
        for var in line:
            new_sat_tuples = list()
            while len(sat_tuples) > 0:
                temp = sat_tuples.pop()
                for value in var.cur_domain():
                    if value not in temp:
                        t = temp + (value,)
                        new_sat_tuples.append(t)
            sat_tuples = new_sat_tuples

        con.add_satisfying_tuples(sat_tuples)
        cons.append(con)

    #9 constraints for columns
    for cellj in range(9):
        column = []
        for celli in range(9):
            column.append(vars[celli*9+cellj])
        con = Constraint("C(Column{})".format(str(cellj+1)),column)

        sat_tuples = []
        sat_tuples.append(())
        for var in column:
            new_sat_tuples = list()
            while len(sat_tuples) > 0:
                temp = sat_tuples.pop()
                for value in var.cur_domain():
                    if value not in temp:
                        t = temp + (value,)
                        new_sat_tuples.append(t)
            sat_tuples = new_sat_tuples

        con.add_satisfying_tuples(sat_tuples)
        cons.append(con)

    #9 constraints for boxes
    for i_begin in range(0,7,3):
        for j_begin in range(0,7,3):
            box = []
            for celli in range(i_begin,i_begin+3):
                for cellj in range(j_begin,j_begin+3):
                    box.append(vars[celli*9+cellj])
            con = Constraint("C(Box{})".format(str(j_begin//3 + i_begin//3*3 + 1)),box)

            sat_tuples = []
            sat_tuples.append(())
            for var in box:
                new_sat_tuples = list()
                while len(sat_tuples) > 0:
                    temp = sat_tuples.pop()
                    for value in var.cur_domain():
                        if value not in temp:
                            t = temp + (value,)
                            new_sat_tuples.append(t)
                sat_tuples = new_sat_tuples

            con.add_satisfying_tuples(sat_tuples)
            cons.append(con)

    sudoku_csp = CSP("Sudoku Model_2", vars)
    for c in cons:
        sudoku_csp.add_constraint(c)

    #my_propagators.prop_GAC(sudoku_csp)

    return sudoku_csp, variable_array

#IMPLEMENT

def picross_model(picross_constraints):
    '''
    DOCUMENT PICROSS MODEL
    '''
    dom = [True,False]


    variable_array = []
    vars = []
    for i in range(len(picross_constraints[1])):
        var_line=[]
        for j in range(len(picross_constraints[0])):
            vars.append(Variable('Cell {}-{}'.format(i,j), dom))
            var_line.append(vars[-1])
        variable_array.append(var_line)


    cons = []

    #constraints for columns
    column_list = picross_constraints[0]
    line_list = picross_constraints[1]

    for cellj in range(len(picross_constraints[0])):
        column = []
        for celli in range(len(picross_constraints[1])):
            column.append(vars[celli*len(picross_constraints[0])+cellj])
        con = Constraint("C(Column{})".format(str(cellj)),column)

        column_cons_input = column_list[cellj]
        list_initial_sat = list()

        bucket_locations=list()
        location = 0
        element = 0
        for number in column_cons_input:
            bucket_locations.append(location)
            location+=number
            if(element != 0):
                location+=1
                list_initial_sat.append(False)
            for i in range(number):
                list_initial_sat.append(True)
            element += 1
        bucket_locations.append(location)

        num_remaining_falses = len(line_list) - len(list_initial_sat)

        num_boxes = len(column_cons_input) + 1

        boxes = list()
        for i in range(num_boxes):
            boxes.append([])

        sat_tuples = list()

        for result in all_combinations(num_remaining_falses,boxes):
            list_initial_sat_copy = list(list_initial_sat)
            global_offset = 0
            bucket_num = 0
            for bucket in result:
                local_offset = 0
                for i in range(bucket[0]):
                    list_initial_sat_copy.insert(global_offset+bucket_locations[bucket_num],False)
                    local_offset+=1
                global_offset+=local_offset
                bucket_num+=1

            #print(list_initial_sat_copy)
            sat_tuples.append(tuple(list_initial_sat_copy))

        con.add_satisfying_tuples(sat_tuples)
        cons.append(con)
        print("did a constraint for column")

    #constraints for lines

    for celli in range(len(picross_constraints[1])):
        line = []
        for cellj in range(len(picross_constraints[0])):
            line.append(vars[celli*len(picross_constraints[0])+cellj])
        con = Constraint("C(Line{})".format(str(celli)),line)

        line_cons_input = line_list[celli]
        list_initial_sat = list()

        bucket_locations=list()
        location = 0
        element = 0
        for number in line_cons_input:
            bucket_locations.append(location)
            location+=number
            if(element != 0):
                location+=1
                list_initial_sat.append(False)
            for i in range(number):
                list_initial_sat.append(True)
            element += 1
        bucket_locations.append(location)

        num_remaining_falses = len(column_list) - len(list_initial_sat)

        num_boxes = len(line_cons_input) + 1

        boxes = list()
        for i in range(num_boxes):
            boxes.append([])

        sat_tuples = list()

        for result in all_combinations(num_remaining_falses,boxes):
            list_initial_sat_copy = list(list_initial_sat)
            global_offset = 0
            bucket_num = 0
            for bucket in result:
                local_offset = 0
                for i in range(bucket[0]):
                    list_initial_sat_copy.insert(global_offset+bucket_locations[bucket_num],False)
                    local_offset+=1
                global_offset+=local_offset
                bucket_num+=1

            #print(list_initial_sat_copy)
            sat_tuples.append(tuple(list_initial_sat_copy))

        con.add_satisfying_tuples(sat_tuples)
        #print("sat_tuples:")
        #print(sat_tuples)
        cons.append(con)
        print("did a constraint for line")

    picross_csp = CSP("Picross Solver Model", vars)
    for c in cons:
        picross_csp.add_constraint(c)

    return picross_csp, variable_array

'''
def create_pic_tupples(total, buckets,tups, tup = tuple()):

    if buckets == 1:
        tup = tup + (total,)
        tups.append(tup)
    else:
        i = 0
        aux_total = total
        buckets -= 1
        while i <= total:
            tup = tup + (i,)
            total -= i
            create_pic_tupples(total, buckets, tups, tup)
            total = aux_total
            i += 1
'''