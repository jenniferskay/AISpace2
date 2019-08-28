# stripsCSPPlanner.py - CSP planner where actions are represented using STRIPS
# AIFCA Python3 code Version 0.7.1 Documentation at http://aipython.org

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from aipython.cspProblem import CSP, Constraint
from aipython.stripsProblem import (Planning_problem, delivery_domain,
                                    strips_blocks1, strips_blocks2,
                                    strips_blocks3, strips_delivery1,
                                    strips_delivery2, strips_delivery3)


class CSP_from_STRIPS(CSP):
    """A CSP where:
    * a CSP variable is constructed by st(var,stage).
    * the dynamics are specified by the STRIPS representation of actions
    """

    def __init__(self, planning_problem, horizon=2):
        prob_domain = planning_problem.prob_domain
        initial_state = planning_problem.initial_state
        goal = planning_problem.goal
        self.act_vars = [st('action', stage) for stage in range(horizon)]
        domains = {av: prob_domain.actions for av in self.act_vars}
        domains.update({st(var, stage): dom
                        for (var, dom) in prob_domain.feats_vals.items()
                        for stage in range(horizon + 1)})
        # intial state constraints:
        constraints = [Constraint((st(var, 0),), is_(val))
                       for (var, val) in initial_state.items()]
        # goal constraints on the final state:
        constraints += [Constraint((st(var, horizon),),
                                   is_(val))
                        for (var, val) in goal.items()]
        # precondition constraints:
        constraints += [Constraint((st(var, stage), st('action', stage)),
                                   if_(val, act))  # st(var,stage)==val if st('action',stage)=act
                        for act, strps in prob_domain.strips_map.items()
                        for var, val in strps.preconditions.items()
                        for stage in range(horizon)]
        # effect constraints:
        constraints += [Constraint((st(var, stage + 1), st('action', stage)),
                                   if_(val, act))  # st(var,stage+1)==val if st('action',stage)==act
                        for act, strps in prob_domain.strips_map.items()
                        for var, val in strps.effects.items()
                        for stage in range(horizon)]
        # frame constraints:
        constraints += [Constraint((st(var, stage), st('action', stage), st(var, stage + 1)),
                                   eq_if_not_in_({act for act in prob_domain.actions
                                                  if var in prob_domain.strips_map[act].effects}))
                        for var in prob_domain.feats_vals
                        for stage in range(horizon)]
        CSP.__init__(self, domains, constraints)

    def extract_plan(self, soln):
        return [soln[a] for a in self.act_vars]


def st(var, stage):
    """returns a string for the var-stage pair that can be used as a variable"""
    return str(var) + "_" + str(stage)


def is_(val):
    """returns a function that is true when it is it applied to val.
    """
    return lambda x: x == val


def if_(v1, v2):
    """if the second argument is v2, the first argument must be v1"""
    # return lambda x1,x2: x1==v1 if x2==v2 else True
    def if_fun(x1, x2):
        return x1 == v1 if x2 == v2 else True
    if_fun.__doc__ = "if x2 is " + str(v2) + " then x1 is " + str(v1)
    return if_fun


def eq_if_not_in_(actset):
    """first and third arguments are equal if action is not in actset"""
    return lambda x1, a, x2: x1 == x2 if a not in actset else True


def con_plan(prob, horizon):
    """finds a plan for problem prob given horizon.
    """
    csp = CSP_from_STRIPS(prob, horizon)
    sol = Con_solver(csp).solve_one()
    return csp.extract_plan(sol) if sol else sol


#from aipython.searchGeneric import Searcher
#from aipython.cspConsistency import Search_with_AC_from_CSP, Con_solver

# Problem 1
# con_plan(strips_delivery1,1) # should it succeed?
# con_plan(strips_delivery1,2) # should it succeed?
# con_plan(strips_delivery1,3) # should it succeed?
# To use search to enumerate solutions
#searcher0a = Searcher(Search_with_AC_from_CSP(CSP_from_STRIPS(strips_delivery1, 1)))
# print(searcher0a.search())

# Problem 2
# con_plan(strips_delivery2,5) # should it succeed?
# con_plan(strips_delivery2,4) # should it succeed?
# To use search to enumerate solutions:
#searcher15a = Searcher(Search_with_AC_from_CSP(CSP_from_STRIPS(strips_delivery2,5)))
# print(searcher15a.search())

# Problem 3
# con_plan(strips_delivery3,6)  # should fail??
# con_plan(strips_delivery3,7)  # should succeed???

# Example 6.13
# strips_edgeless = Planning_problem(delivery_domain,
#                                    {'SWC': True, 'RHC': False}, {'SWC': False})
# con_plan(strips_edgeless,2)  # Horizon of 2
# con_plan(strips_edgeless,3)  # Horizon of 3

# strips_delivery4 = Planning_problem(delivery_domain, {'SWC': True},
#                                   {'SWC': False, 'MW': False, 'RHM': False})

# For the stochastic local search:
#from cspSLS import SLSearcher, Runtime_distribution
# cspplanning15 = CSP_from_STRIPS(strips_delivery2,5) # should succeed
#se0 = SLSearcher(cspplanning15); print(se0.search(100000,0.5))
#p = Runtime_distribution(cspplanning15)
# p.plot_run(1000,1000,0.7)  # warning will take a few minutes
