# searchProblem.py - representations of search problems
# AIFCA Python3 code Version 0.7.1 Documentation at http://aipython.org

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en


class Search_problem(object):
    """A search problem consists of:
    * a start node
    * a neighbors function that gives the neighbors of a node
    * a specification of a goal
    * a (optional) heuristic function.
    The methods must be overridden to define a search problem."""

    def start_node(self):
        """returns start node"""
        raise NotImplementedError("start_node")   # abstract method

    def is_goal(self, node):
        """is True if node is a goal"""
        raise NotImplementedError("is_goal")   # abstract method

    def neighbors(self, node):
        """returns a list of the arcs for the neighbors of node"""
        raise NotImplementedError("neighbors")   # abstract method

    def heuristic(self, n):
        """Gives the heuristic value of node n.
        Returns 0 if not overridden."""
        return 0


class Arc(object):
    """An arc has a from_node and a to_node node and a (non-negative) cost"""

    def __init__(self, from_node, to_node, cost=1, action=None):
        assert cost >= 0, ("Cost cannot be negative for" +
                           str(from_node) + "->" + str(to_node) + ", cost: " + str(cost))
        self.from_node = from_node
        self.to_node = to_node
        self.action = action
        self.cost = cost

    def __repr__(self):
        """string representation of an arc"""
        if self.action:
            return str(self.from_node) + " --" + str(self.action) + "--> " + str(self.to_node)
        else:
            return str(self.from_node) + " --> " + str(self.to_node)


class Search_problem_from_explicit_graph(Search_problem):
    """A search problem consists of:
    * a list or set of nodes
    * a list or set of arcs
    * a start node
    * a list or set of goal nodes
    * a dictionary that maps each node into its heuristic value
    * a dictionary that maps each node name into its (x,y)-position.
    (node names should be unique)
    """

    def __init__(self, nodes, arcs, start=None, goals=set(), hmap={}, positions={}):
        self.neighs = {}
        self.nodes = nodes
        for node in nodes:
            self.neighs[node] = []
        self.arcs = arcs
        for arc in arcs:
            self.neighs[arc.from_node].append(arc)
        self.start = start
        self.goals = goals
        self.hmap = hmap
        self.positions = positions

    def start_node(self):
        """returns start node"""
        return self.start

    def is_goal(self, node):
        """is True if node is a goal"""
        return node in self.goals

    def neighbors(self, node):
        """returns the neighbors of node"""
        return self.neighs[node]

    def heuristic(self, node):
        """Gives the heuristic value of node n.
        Returns 0 if not overridden in the hmap."""
        if node in self.hmap:
            return self.hmap[node]
        else:
            return 0

    def __repr__(self):
        """returns a string representation of the search problem"""
        res = ""
        for arc in self.arcs:
            res += str(arc) + ".  "
        return res

    def neighbor_nodes(self, node):
        """returns an iterator over the neighbors of node"""
        return (path.to_node for path in self.neighs[node])


class Path(object):
    """A path is either a node or a path followed by an arc"""

    def __init__(self, initial, arc=None):
        """initial is either a node (in which case arc is None) or
        a path (in which case arc is an object of type Arc)"""
        self.initial = initial
        self.arc = arc
        if arc is None:
            self.cost = 0
        else:
            self.cost = initial.cost + arc.cost

    def end(self):
        """returns the node at the end of the path"""
        if self.arc is None:
            return self.initial
        else:
            return self.arc.to_node

    def nodes(self):
        """enumerates the nodes for the path.
        This starts at the end and enumerates nodes in the path backwards."""
        current = self
        while current.arc is not None:
            yield current.arc.to_node
            current = current.initial
        yield current.initial

    def initial_nodes(self):
        """enumerates the nodes for the path before the end node.
        This starts at the end and enumerates nodes in the path backwards."""
        if self.arc is not None:
            for nd in self.initial.nodes():
                yield nd     # could be "yield from"

    def __repr__(self):
        """returns a string representation of a path"""
        if self.arc is None:
            return str(self.initial)
        elif self.arc.action:
            return (str(self.initial) + "\n   --" + str(self.arc.action)
                    + "--> " + str(self.arc.to_node))
        else:
            return str(self.initial) + " --> " + str(self.arc.to_node)


search_empty = Search_problem_from_explicit_graph(
    {}, [], start=None, goals={})

search_simple1 = Search_problem_from_explicit_graph(
    {'a', 'b', 'c', 'd', 'g'},
    [Arc('a', 'b', 1), Arc('a', 'c', 3), Arc('b', 'c', 1), Arc('b', 'd', 3), Arc('c', 'd', 1), Arc('c', 'g', 3), Arc('d', 'g', 1)],
    start='a',
    goals={'g'},
    positions={'g': (60, 483), 'd': (229, 110), 'a': (919, 385), 'b': (659, 60), 'c': (489, 436)})

search_simple2 = Search_problem_from_explicit_graph(
    {'a', 'b', 'c', 'd', 'e', 'g', 'h', 'j'},
    [Arc('a', 'b', 1), Arc('b', 'c', 3), Arc('b', 'd', 1), Arc('d', 'e', 3), Arc('d', 'g', 1), Arc('a', 'h', 3), Arc('h', 'j', 1)],
    start='a',
    goals={'g'})

search_edgeless = Search_problem_from_explicit_graph(
    {'a', 'b', 'c', 'd', 'e', 'g', 'h', 'j'},
    [],
    start='g',
    goals={'k', 'g'})

search_acyclic_delivery = Search_problem_from_explicit_graph(
    {'mail', 'ts', 'o103', 'o109', 'o111', 'b1', 'b2', 'b3', 'b4', 'c1', 'c2', 'c3',
     'o125', 'o123', 'o119', 'r123', 'storage'},
    [Arc('ts', 'mail', 6),
        Arc('o103', 'ts', 8),
        Arc('o103', 'b3', 4),
        Arc('o103', 'o109', 12),
        Arc('o109', 'o119', 16),
        Arc('o109', 'o111', 4),
        Arc('b1', 'c2', 3),
        Arc('b1', 'b2', 6),
        Arc('b2', 'b4', 3),
        Arc('b3', 'b1', 4),
        Arc('b3', 'b4', 7),
        Arc('b4', 'o109', 7),
        Arc('c1', 'c3', 8),
        Arc('c2', 'c3', 6),
        Arc('c2', 'c1', 4),
        Arc('o123', 'o125', 4),
        Arc('o123', 'r123', 4),
        Arc('o119', 'o123', 9),
        Arc('o119', 'storage', 7)],
    start='o103',
    goals={'r123'},
    hmap={
        'mail': 26,
        'ts': 23,
        'o103': 21,
        'o109': 24,
        'o111': 27,
        'o119': 11,
        'o123': 4,
        'o125': 6,
        'r123': 0,
        'b1': 13,
        'b2': 15,
        'b3': 17,
        'b4': 18,
        'c1': 6,
        'c2': 10,
        'c3': 12,
        'storage': 12
    }
)

search_cyclic_delivery = Search_problem_from_explicit_graph(
    {'mail', 'ts', 'o103', 'o109', 'o111', 'b1', 'b2', 'b3', 'b4', 'c1', 'c2', 'c3',
     'o125', 'o123', 'o119', 'r123', 'storage'},
    [Arc('ts', 'mail', 6), Arc('mail', 'ts', 6),
        Arc('o103', 'ts', 8), Arc('ts', 'o103', 8),
        Arc('o103', 'b3', 4),
        Arc('o103', 'o109', 12), Arc('o109', 'o103', 12),
        Arc('o109', 'o119', 16), Arc('o119', 'o109', 16),
        Arc('o109', 'o111', 4), Arc('o111', 'o109', 4),
        Arc('b1', 'c2', 3),
        Arc('b1', 'b2', 6), Arc('b2', 'b1', 6),
        Arc('b2', 'b4', 3), Arc('b4', 'b2', 3),
        Arc('b3', 'b1', 4), Arc('b1', 'b3', 4),
        Arc('b3', 'b4', 7), Arc('b4', 'b3', 7),
        Arc('b4', 'o109', 7),
        Arc('c1', 'c3', 8), Arc('c3', 'c1', 8),
        Arc('c2', 'c3', 6), Arc('c3', 'c2', 6),
        Arc('c2', 'c1', 4), Arc('c1', 'c2', 4),
        Arc('o123', 'o125', 4), Arc('o125', 'o123', 4),
        Arc('o123', 'r123', 4), Arc('r123', 'o123', 4),
        Arc('o119', 'o123', 9), Arc('o123', 'o119', 9),
        Arc('o119', 'storage', 7), Arc('storage', 'o119', 7)],
    start='o103',
    goals={'r123'},
    hmap={
        'mail': 26,
        'ts': 23,
        'o103': 21,
        'o109': 24,
        'o111': 27,
        'o119': 11,
        'o123': 4,
        'o125': 6,
        'r123': 0,
        'b1': 13,
        'b2': 15,
        'b3': 17,
        'b4': 18,
        'c1': 6,
        'c2': 10,
        'c3': 12,
        'storage': 12
    }
)

sample_tree_graph = Search_problem_from_explicit_graph({'S','N1','N2','N3','N4','N5','N6','N7','N8','N9','N10','G',},
                 [Arc('S','N1',9.9),
                 Arc('N1','N3',11.9),
                  Arc('N3','N7',9.6),
                  Arc('N1','N4',9.1),
                 Arc('N4','N8',8.7),
                 Arc('S','N2',10.6),
                 Arc('N2','N5',9.1),
                 Arc('N5','N9',8.6),
                 Arc('N5','G',8.8),
                 Arc('N2','N6',12.8),
                 Arc('N6','N10',8.5),],
                     start='S',
                goals={'G'},
                 hmap ={'S':26.0,'N1':25.1,'N2':16.4,'N3':27.6,'N4':18.1,'N5':8.8,'N6':8.5,'N7':28.0,'N8':18.7,'N9':10,'N10':6.5,'G':0,},
                    positions={
"S": (278,50),
"N5": (307,186),
"N9": (255,247),
"G": (349,247),
"N10": (442,240),
"N6": (424,156),
"N2": (372,111),
"N1": (147,99),
"N3": (62,156),
"N7": (38,226),
"N4": (183,166),
"N8": (142,236)})

extend_tree_graph = Search_problem_from_explicit_graph(
    nodes={'N2', 'N3', 'N20', 'N1', 'S', 'N11', 'N18', 'N10', 'N8', 'N19', 'N13', 'N15', 'N4', 'N17', 'N14', 'N9', 'N16', 'N12', 'N6', 'N5', 'N7', 'G'},
    arcs=[Arc('N1', 'N3', 11.9), Arc('N1', 'N4', 9.1), Arc('N2', 'N6', 12.8), Arc('N2', 'N5', 9.1), Arc('S', 'N1', 9.9), Arc('S', 'N2', 10.6), Arc('N5', 'N9', 8.6), Arc('N5', 'N10', 2.0), Arc('N4', 'N8', 8.7), Arc('N3', 'N7', 16.6), Arc('N9', 'N13', 4.0), Arc('N9', 'N14', 5.0), Arc('N14', 'N18', 3.0), Arc('N14', 'G', 4.0), Arc('N6', 'N12', 2.0), Arc('N12', 'N16', 6.0), Arc('N6', 'N11', 8.0), Arc('N11', 'N15', 8.0), Arc('N15', 'N19', 10.0), Arc('N7', 'N20', 2.0), Arc('N13', 'N17', 6.0)],
    start='S',
    goals={'G'},
    hmap={'N1': 27.1, 'N2': 18.4, 'N3': 30.2, 'N4': 28.9, 'N6': 10.5, 'N5': 14.8, 'N18': 0.0, 'S': 30.0, 'N9': 8.0, 'N10': 14.5, 'N8': 30.0, 'N7': 32.0, 'N13': 15.0, 'N14': 0.0, 'G': 0.0, 'N15': 14.0, 'N16': 13.0, 'N12': 14.9, 'N11': 14.0, 'N19': 17.0, 'N20': 33.0, 'N17': 10.0},
    positions={'N1': (7723.0767, 5182.8604), 'N2': (7867.8647, 5163.451), 'N3': (7584.081, 5286.368), 'N4': (7747.4663, 5295.6665), 'N6': (8075.205, 5266.595), 'N5': (7895.591, 5276.804), 'N18': (7905.7705, 5590.145), 'S': (7797.393, 5079.8394), 'N9': (7858.6997, 5388.454), 'N10': (7982.9863, 5382.1826), 'N8': (7724.952, 5387.6284), 'N7': (7546.7407, 5379.1914), 'N13': (7796.918, 5492.031), 'N14': (7954.2715, 5479.5015), 'G': (8014.078, 5585.455), 'N15': (8122.802, 5475.834), 'N16': (8268.428, 5473.6763), 'N12': (8254.093, 5352.59), 'N11': (8106.6533, 5366.197), 'N19': (8128.3945, 5585.9844), 'N20': (7545.5723, 5478.4287), 'N17': (7800.804, 5590.161)})
