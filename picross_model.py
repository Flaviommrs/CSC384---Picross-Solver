'''
Construct and return a picross CSP model.
'''

from cspbase import *
import itertools
import propagators as my_propagators
import copy
from propagators import *

#Auxiliar function to all_combinations
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

#Given a list of buckets and a "sum" number, it yields all the possible combinations for putting "sum" objects into the buckets.
#In other words, yield all the possible solutions for putting sum distinct balls into buckets.
#FUTURE IMPLEMENTATION: Use a list of integers instead of a list of lists for buckets.
def all_combinations(sum, buckets):
    for combination in all_combinations_aux(sum,buckets):
        for bucket in combination:
            if len(bucket) == 0:
                bucket.append(0)
        yield combination

#returns a picross_model given an input board
def picross_model(picross_constraints):
    '''
    Returns a variable array, split by lines, with all the variables, each one corresponding to a cell in a picross board.

    As input, it expects a list representing the board, as follows:
        board = [cols, rows]
    Where cols is a list of the constraints for the columns:
        cols = [[1],[2,1],[0]]
    And rows is a list of the constraints for the lines:
        rows = [[1],[2,1],[0]]
    '''
    #True represents painted, false represents blank
    dom = [True,False]


    #Create all the variables
    variable_array = []
    vars = []
    for i in range(len(picross_constraints[1])):
        var_line=[]
        for j in range(len(picross_constraints[0])):
            vars.append(Variable('Cell {}-{}'.format(i,j), dom))
            var_line.append(vars[-1])
        variable_array.append(var_line)


    cons = []

    #Constraints for columns
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

            sat_tuples.append(tuple(list_initial_sat_copy))

        con.add_satisfying_tuples(sat_tuples)
        cons.append(con)

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

            sat_tuples.append(tuple(list_initial_sat_copy))

        con.add_satisfying_tuples(sat_tuples)
        cons.append(con)

    #creates the CSP variable
    picross_csp = CSP("Picross Solver Model", vars)
    #add the constraints to the CSP
    for c in cons:
        picross_csp.add_constraint(c)

    return picross_csp, variable_array
'''
writes the input to an image file.
Expects:
    filename: string with the file name.
    width: width in pixels of the image
    height: height in pixels of the image
    pixels: list of RGB tuples/lists with values between 0 and 255 for Red, Green and Blue, in that order.
'''
def write_to_file(filename, width, height, pixels):
    f = open(filename, "wb")

    f.write(b"P3\n")
    f.write(b"# TESTING PNM FORMAT FOR SAVING")
    f.write(b"\n")
    f.write(b"# Authors: Rodrigo Guimaraes and Flavio Matheus")
    f.write(b"\n")
    f.write(bytes(str(width) + " " + str(height),'UTF-8'))
    f.write(b"\n")
    f.write(bytes(str(256),'UTF-8'))
    f.write(b"\n")
    i=-1
    for pixel in pixels:
        i+=1
        if(i==width):
            i=0
        f.write(bytes(str(pixel[0])+str(" ")+str(pixel[1])+str(" ")+str(pixel[2])+" ",'UTF-8'))

    f.close()

#pack and rgb-alpha standard into a byte fashion. Currently not used, since alpha is not being used.
def rgba(r, g, b, a):
    return (struct.pack("B",r) + struct.pack("B",g) + struct.pack("B",b) + struct.pack("B",a))

'''
This functions creates all the needed models and solves them to compose a color image with the result of a colored picross puzzle.

Expects:
        -picross_constraints: a list of boards, where each board is represented by a list, as follows:
            board = [cols, rows]
        Where cols is a list of the constraints for the columns:
            cols = [[1],[2,1],[0]]
        And rows is a list of the constraints for the lines:
            rows = [[1],[2,1],[0]]

        -color_list: a list of lists, where each inner list represents a color in RGB
            color_list = [red,green,blue]
            Where:
            red =   [255,0,0]
            green = [0,255,0]
            blue =  [0,0,255]

NOTE1: it is supposed that len(color_list) = len(picross_constraints)
NOTE2: this solver is not for color picrosses you find normally. It solves the different colors as separate problems and then it merges the results.
'''
def color_picross_basic_solver(picross_constraints, color_list):
    cspL = list()
    variable_arrayL = list()
    for i in range(len(color_list)):
        csp, variable_array = picross_model(picross_constraints[i])
        cspL.append(csp)
        variable_arrayL.append(variable_array)
        solver  = BT(cspL[i])
        print("=========================================================")
        print("Using GAC")
        solver.bt_search(prop_GAC)
        print("Solved for color " + str(i))
        print_Picross(variable_arrayL[i])
        print("=========================================================")

    pixels = [(255,255,255) for x in range(len(picross_constraints[0][0])*len(picross_constraints[0][1]))]

    for i in range(len(color_list)):
        index = -1
        for row in variable_arrayL[i]:
            for variable in row:
                index+=1
                if(variable.get_assigned_value()):
                    pixels[index] = (color_list[i][0],color_list[i][1],color_list[i][2])

    write_to_file("out.pnm", len(variable_arrayL[0][0]), len(variable_arrayL[0]), pixels)


'''
Command line printer for monochromatic picrosses.
Expects a variable_array, that contains:
    variable_array = [row_1,row_2, ... ,row_n]
    Where:
        row_n = [var1,var2,...,varN]

NOTE: It is using "XX" for a painted space and "  " for a blank space, since this is closer to being square than a single character.
'''
def print_Picross(variables):
    for row in variables:
        for variable in row:
            if(variable.get_assigned_value()):
                print("XX",end="")
            else:
                print("  ",end="")
        print("")
