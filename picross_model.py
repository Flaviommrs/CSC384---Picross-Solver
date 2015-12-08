
'''
Construct and return a picross CSP models.
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

