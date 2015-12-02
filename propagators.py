#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the warehouse domain.

'''This file will contain different constraint propagators to be used within
   bt_search.

   propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned variables
      can be accessed via methods, the values assigned can also be accessed.

      newly_instaniated_variable is an optional argument.
      if newly_instantiated_variable is not None:
          then newly_instantiated_variable is the most
           recently assigned variable of the search.
      else:
          propagator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of variable values pairs are all of the values
      the propagator pruned (using the variable's prune_value method).
      bt_search NEEDS to know this in order to correctly restore these
      values when it undoes a variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newly_instantiated_variable = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated constraints)
        we do nothing...return true, []

        for forward checking (where we only check constraints with one remaining variable)
        we look for unary constraints of the csp (constraints whose scope contains
        only one variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newly_instantiated_variable = a variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned variable left

         for gac we initialize the GAC queue with all constraints containing V.

   '''
import copy

def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no
    propagation at all. Just check fully instantiated constraints'''

    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, []
    return True, []

def prop_FC(csp, newVar=None):
    '''Do forward checking. That is check constraints with
       only one uninstantiated variable. Remember to keep
       track of all pruned variable,value pairs and return '''
    vals_pruned = list()
    '''for forward checking (where we only check constraints with one remaining variable)
    we look for unary constraints of the csp (constraints whose scope contains
    only one variable) and we forward_check these constraints.
    NOTE: You should be able to handle "wrong" inputs, where a variable has been assigned but newVar=none'''

    if not newVar:
        for c in csp.get_all_cons():
            if c.get_n_unasgn() == 1:
                vars = c.get_scope()
                unasgn_var = c.get_unasgn_vars()[0]
                for value in unasgn_var.cur_domain():
                    vals = []
                    for var in vars:
                        if var.is_assigned():
                            vals.append(var.get_assigned_value())
                        else:
                            vals.append(value)
                    if not c.check(vals):
                        my_t = (unasgn_var, value)
                        vals_pruned.append(my_t)
                        unasgn_var.prune_value(value)
                if(unasgn_var.cur_domain_size() == 0):
                    return False, vals_pruned
        return True, vals_pruned

        ''' THIS CODE IS ABLE TO CHECK UNARY CONSTRAINTS - IF NO "WRONGS" VALUES ARE PASSED IT WILL WORK FLAWLESSLY
        for c in csp.get_all_cons():
            var_list = c.get_scope()
            if len(var_list) == 1:
                var = var_list[0]
                for value in var.cur_domain():
                    value_list = list(value)
                    if not c.check(value_list):
                        my_t = (var,value)
                        vals_pruned.append(my_t)
                        var.prune_value(value)
                if(var.cur_domain_size == 0):
                    return False, vals_pruned
        return True, vals_pruned
        '''

    '''
    for forward checking we forward check all constraints with V
    that have one unassigned variable left
    '''
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 1:
            vars = c.get_scope()
            unasgn_var = c.get_unasgn_vars()[0]
            for value in unasgn_var.cur_domain():
                vals = []
                for var in vars:
                    if var.is_assigned():
                        vals.append(var.get_assigned_value())
                    else:
                        vals.append(value)
                if not c.check(vals):
                    my_t = (unasgn_var, value)
                    vals_pruned.append(my_t)
                    unasgn_var.prune_value(value)
            if(unasgn_var.cur_domain_size() == 0):
                return False, vals_pruned
    return True, vals_pruned

def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''

    gac_queue = list()

    '''for gac we establish initial GAC by initializing the GAC queue
        with all constraints of the csp'''

    if not newVar:
        gac_queue = csp.get_all_cons()
        '''
        constraints = csp.get_all_cons()
        for c in constraints:
            for var in c.get_scope():
                for var2 in c.get_scope():
                if var != var2:
                    my_t = (var,var2)
                    if my_t not in gac_queue:
                        gac_queue.append(my_t)
                        my_t2 = (var2, var)
                        gac_queue.append(my_t2)
        '''
    else:
        gac_queue = csp.get_cons_with_var(newVar)
        '''for gac we initialize the GAC queue with all constraints containing V.'''
        '''
        const_newvar = csp.get_cons_with_var(newVar)
        for c in const_newvar:
            for var in c.get_scope():
                if newVar != var:
                    my_t = (newVar,var)
                    if my_t not in gac_queue:
                        gac_queue.append(my_t)
                        my_t2 = (var, newVar)
                        gac_queue.append(my_t2)
        '''
    vals_pruned = list()
    while len(gac_queue) > 0:
        c = gac_queue.pop()
        for var in c.get_scope():
            for value in var.cur_domain():
                if not c.has_support(var,value):
                    var.prune_value(value)
                    test = (var,value)
                    vals_pruned.append(test)

                    if var.cur_domain_size() == 0:
                        return False, vals_pruned
                    else:
                        for ct in csp.get_cons_with_var(var):
                            if ct not in gac_queue:
                                gac_queue.append(ct)

    return True, vals_pruned


    '''ORIGINAL IMPLEMENTATION - NOT REALLY WORKING
    vals_pruned = list()
    last_number_vals_pruned = -1
    while len(vals_pruned) != last_number_vals_pruned:
        last_number_vals_pruned = len(vals_pruned)
        for c in gac_queue:
            if c.get_n_unasgn() == 1: #FC
                vars = c.get_scope()
                unasgn_var = c.get_unasgn_vars()[0]
                for value in unasgn_var.cur_domain():
                    vals = []
                    for var in vars:
                        if var.is_assigned():
                            vals.append(var.get_assigned_value())
                        else:
                            vals.append(value)
                    if not c.check(vals):
                        my_t = (unasgn_var, value)
                        vals_pruned.append(my_t)
                        unasgn_var.prune_value(value)
                if(unasgn_var.cur_domain_size() == 0):
                    return False, vals_pruned
            elif c.get_n_unasgn() == 2:
                vars = c.get_scope()
                unasgn_var = c.get_unasgn_vars()[0]
                unasgn_var2 = c.get_unasgn_vars()[1]
                for value2 in unasgn_var2.cur_domain():
                    isValid = False
                    for value in unasgn_var.cur_domain():
                        vals = []
                        for var in vars:
                            if var.is_assigned():
                                vals.append(var.get_assigned_value())
                            elif var == unasgn_var:
                                vals.append(value)
                            elif var == unasgn_var2:
                                vals.append(value2)
                        if c.check(vals):
                            isValid = True
                            break;
                    if not isValid:
                        my_t = (unasgn_var2, value2)
                        vals_pruned.append(my_t)
                        unasgn_var2.prune_value(value2)
                if(unasgn_var2.cur_domain_size() == 0):
                    return False, vals_pruned

                for value in unasgn_var.cur_domain():
                    isValid = False
                    for value2 in unasgn_var2.cur_domain():
                        vals = []
                        for var in vars:
                            if var.is_assigned():
                                vals.append(var.get_assigned_value())
                            elif var == unasgn_var:
                                vals.append(value)
                            elif var == unasgn_var2:
                                vals.append(value2)
                        if c.check(vals):
                            isValid = True
                            break;
                    if not isValid:
                        my_t = (unasgn_var, value)
                        vals_pruned.append(my_t)
                        unasgn_var.prune_value(value)
                if(unasgn_var.cur_domain_size() == 0):
                    return False, vals_pruned

    return True, vals_pruned
    '''
#IMPLEMENT
