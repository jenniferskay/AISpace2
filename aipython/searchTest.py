# searchTest.py - code that may be useful to compare A* and branch-and-bound
# AIFCA Python3 code Version 0.7.1 Documentation at http://aipython.org

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

import searchProblem
from searchBranchAndBound import DF_branch_and_bound
from searchGeneric import Searcher
from searchMPP import SearcherMPP
from searchTest import run

DF_branch_and_bound.max_display_level = 1
Searcher.max_display_level = 1


def run(problem, name):
    print("\n\n*******", name)
    print("\nA*:")
    tsearcher = Searcher(problem)
    print("Path found:", tsearcher.search(), "  cost=", tsearcher.solution.cost)
    print("there are", tsearcher.frontier.count(tsearcher.solution.cost),
          "elements remaining on the queue with f-value=", tsearcher.solution.cost)

    print("\nA* with MPP:"),
    msearcher = SearcherMPP(problem)
    print("Path found:", msearcher.search(), "  cost=", msearcher.solution.cost)
    print("there are", msearcher.frontier.count(msearcher.solution.cost),
          "elements remaining on the queue with f-value=", msearcher.solution.cost)

    print("\nBranch and bound (with too-good initial bound):")
    tbb = DF_branch_and_bound(problem, tsearcher.solution.cost + 0.1)  # cheating!!!!
    print("Path found:", tbb.search(), "  cost=", tbb.solution.cost)


if __name__ == "__main__":
    run(searchProblem.search_simple1, "Problem 1")
#   run(searchProblem.search_acyclic_delivery,"Acyclic Delivery")
#   run(searchProblem.search_cyclic_delivery,"Cyclic Delivery")
# also test some graphs with cycles, and some with multiple least-cost paths
