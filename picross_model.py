
'''
Construct and return a picross CSP models.
'''

from cspbase import *
import itertools
import propagators as my_propagators
import copy
from propagators import *

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
        #print("did a constraint for column")

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
        #print("did a constraint for line")

    picross_csp = CSP("Picross Solver Model", vars)
    for c in cons:
        picross_csp.add_constraint(c)

    return picross_csp, variable_array

def write_to_file(filename, width, height, pixels):
    f = open(filename, "wb")

    f.write(b"P3\n")
    f.write(b"# TESTING PNM FORMAT FOR SAVING")
    f.write(b"\n")
    f.write(b"# BLABLABLA")
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


def rgba(r, g, b, a):
    return (struct.pack("B",r) + struct.pack("B",g) + struct.pack("B",b) + struct.pack("B",a))

#this solver is not for color picrosses you find normally. It solves the different collors as separate problems and then it merges the results.
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

    #pixels = [[0 for x in range(len(picross_constraints[0][0]))] for x in range(len(picross_constraints[0][1]))]
    pixels = [(255,255,255) for x in range(len(picross_constraints[0][0])*len(picross_constraints[0][1]))]
    """
    for x in range(len(picross_constraints[0][1])):
        for y in range(len(picross_constraints[0][0])):
            pixels[x][y] = (255,255,255)
    """

    for i in range(len(color_list)):
        index = -1
        y=-1
        for row in variable_arrayL[i]:
            y+=1
            x=-1
            for variable in row:
                x+=1
                index+=1
                if(variable.get_assigned_value()):
                    #pixels[y][x] = i+1
                    pixels[index] = (color_list[i][0],color_list[i][1],color_list[i][2])



    write_to_file("out.pnm", len(variable_arrayL[0][0]), len(variable_arrayL[0]), pixels)



def print_Picross(variables):
    for row in variables:
        #print(["T" if var.get_assigned_value() == True else "F" for var in row])
        for variable in row:
            if(variable.get_assigned_value()):
                print("XX",end="")
            else:
                print("  ",end="")
        print("")

