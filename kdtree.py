import math
import sys

class Point(object):
    """
    it is convenient to create a Point class, it represents a point in the space.
    """
    def __init__(self, x = 0.0, y = 0.0):
        self.x = x
        self.y = y

    def distance(self, other):
        """ computes euclidean distance between two points """
        deltaX = (self.x - other.x) * (self.x - other.x)
        deltaY = (self.y - other.y) * (self.y - other.y)
        return math.sqrt(deltaX + deltaY)

    def __eq__(self, other):
        """ whether two points are the same? """
        return self.x == other.x and self.y == other.y
    
    def __repr__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

class Node(object):
    """
    Node class represents a node in the KD-Tree, each node has at most two child, and a pointer to its parent.
    Because later on we will use parent pointer to get sampling of parent, and children of sampling of parent.
    """
    def __init__(self):
        self.parent = None
        self.point = None
        self.child1 = None
        self.child2 = None
        self.direction = True

    def __repr__(self):
        return "(" + str(self.point.x) + ", " + str(self.point.y) + ")"

VERT = True     # split the space vertically
HORI = False    # split the space horizontally

def _sort_by_dir(data, dir):
    """ sort the points by direction """
    if not len(data): return None

    if len(data) == 1: return data[0]

    if dir:
        return sorted(data, cmp=lambda p1, p2: cmp(p1.x, p2.x))
    else:
        return sorted(data, cmp=lambda p1, p2: cmp(p1.y, p2.y))

def create_kd_tree(data, dir, parent):
    """
    given a set of points, create a kd-tree.
    dir indicates the direction, it can only be vertical or horizontal
    """
    assert (dir == VERT or dir == HORI)

    if len(data) < 1: return None
    # if there is only one point left
    if len(data) == 1:
        n = Node()
        n.point = data[0]
        n.direction = dir
        if parent: n.parent = parent
        return n
    
    root = Node()
    sorted_points = _sort_by_dir(data, dir)
    median_point = sorted_points[len(sorted_points)/2]
    root.point = median_point
    root.direction = dir
    idx = sorted_points.index(median_point)
    if parent: root.parent = parent
    # recursively create left and right child, but with opposite direction
    root.child1 = create_kd_tree(sorted_points[:idx], not dir, root)
    root.child2 = create_kd_tree(sorted_points[idx+1:], not dir, root)
    return root

ROOT_INTENTATION = 3
INTENTATION = 10

def print_tree(tree, depth=0):
    """ print the KD-Tree """
    if tree is None: return
    else:
        if not depth:
            print tree.point, "|" if tree.direction else "-"
        else:
            print " " * (INTENTATION * (depth-1) + ROOT_INTENTATION), "|------>", tree.point, "|" if tree.direction else "-"

        print_tree(tree.child1, depth+1)
        print_tree(tree.child2, depth+1)

def potential_nearest(tree, test):
    """ finds out the potential nearest point in the KD-Tree """
    if tree is None or tree.point is None: return None

    if tree.child1 is None and tree.child2 is None: return tree

    if (tree.direction and test.x < tree.point.x) or (not tree.direction and test.y < tree.point.y):
        return potential_nearest(tree.child1, test)
    else:
        return potential_nearest(tree.child2, test)

def nearest_neighbour(tree, test):
    """
    starting from potential nearest point,
    checking sampling, parents sampling, child1 and child2 of this sampling
    """
    print
    print "=== Start checking nearest neighbour ==="
    nn = None
    min_distance = sys.maxint
    checked = 0
    pn = potential_nearest(tree, test)

    if pn is not None:
        print "Checking potential nearest node %s" % pn.point
        if min_distance > test.distance(pn.point):
            nn = pn
            min_distance = test.distance(pn.point)

        sampling = pn.parent.child2 if pn.parent.child1 == pn else pn.parent.child1
        if sampling is not None:
            print "Checking sampling node %s" % sampling.point
            checked += 1
        if sampling is not None and min_distance > test.distance(sampling.point):

            nn = sampling
            min_distance = test.distance(sampling.point)

        parent_sampling = pn.parent.parent.child2 if pn.parent.parent.child1 == pn.parent else pn.parent.parent.child1
        if parent_sampling is not None:
            print "Checking parent sampling node %s" % parent_sampling.point
            checked += 1
        if parent_sampling is not None and min_distance > test.distance(parent_sampling.point):
            nn = parent_sampling
            min_distance = test.distance(parent_sampling.point)

        ps_child1 = parent_sampling.child1
        if ps_child1 is not None:
            print "Checking parent sampling child 1 node %s" % ps_child1.point
            checked += 1
        if ps_child1 is not None and min_distance > test.distance(ps_child1.point):
            nn = ps_child1
            min_distance = test.distance(ps_child1.point)

        ps_child2 = parent_sampling.child2
        if ps_child2 is not None:
            print "Checking parent sampling child 2 node %s" % ps_child2.point
            checked += 1
        if ps_child2 is not None and min_distance > test.distance(ps_child2.point):
            nn = ps_child2
            min_distance = test.distance(ps_child2.point)

        if checked < 4:
            parent = pn.parent
            if parent is not None:
                print "Checking parent node %s" % parent.point
            if parent and min_distance > test.distance(parent.point):
                nn = parent
                min_distance = test.distance(parent.point)

        print "=== end of checking nearest neighbour ==="
        print
        return nn, min_distance

    return None, 0

if __name__ == '__main__':
    p11 = Point(5, 4)
    p12 = Point(1, 6)
    p13 = Point(6, 1)
    p14 = Point(7, 5)
    p15 = Point(2, 7)
    p16 = Point(2, 2)
    p17 = Point(5, 8)

    points = [p11, p12, p13, p14, p15, p16, p17]

    tree11 = create_kd_tree(points, True, None)

    print "Create KD-Tree with root node vertically splitted"
    print_tree(tree11)
    print

    p = nearest_neighbour(tree11, Point(3, 5))
    print "The nearest neighbour of point (3, 5) is: ", p[0], "distance is: ", p[1]

    p = nearest_neighbour(tree11, Point(4.5, 2))
    print "The nearest neighbour of point (4.5, 2) is: ", p[0], "distance is: ", p[1]

    tree12 = create_kd_tree(points, False, None)

    print "Create KD-Tree with root node horizontally splitted"
    print_tree(tree12)
    print

    p = nearest_neighbour(tree12, Point(3, 5))
    print "The nearest neighbour of point (3, 5) is: ", p[0], "distance is: ", p[1]

    p = nearest_neighbour(tree12, Point(4.5, 2))
    print "The nearest neighbour of point (4.5, 2) is: ", p[0], "distance is: ", p[1]

    p21 = Point(3, 5)
    p22 = Point(1, 11)
    p23 = Point(4, 20)
    p24 = Point(7, 2)
    p25 = Point(6, 10)
    p26 = Point(5, 16)
    p27 = Point(10, 21)
    p28 = Point(15, 4)
    p29 = Point(17, 6)
    p210 = Point(13, 8)
    p211 = Point(12, 13)
    p212 = Point(14, 15)
    p213 = Point(13, 23)
    p214 = Point(11, 25)

    points2 = [p21, p22, p23, p24, p25, p26, p27, p28, p29, p210, p211, p212, p213, p214]

    tree21 = create_kd_tree(points2, True, None)

    print "Create KD-Tree with root node vertically splitted"
    print_tree(tree21)
    print

    p = nearest_neighbour(tree21, Point(12, 7))
    print "The nearest neighbour of point (12, 7) is: ", p[0], "distance is: ", p[1]

    p = nearest_neighbour(tree21, Point(5, 19))
    print "The nearest neighbour of point (5, 19) is: ", p[0], "distance is: ", p[1]

    tree22 = create_kd_tree(points2, False, None)
    print "Create KD-Tree with root node horizontally splitted"
    print_tree(tree22)
    print
    p = nearest_neighbour(tree22, Point(12, 7))
    print "The nearest neighbour of point (12, 7) is: ", p[0], "distance is: ", p[1]

    p = nearest_neighbour(tree22, Point(5, 19))
    print "The nearest neighbour of point (5, 19) is: ", p[0], "distance is: ", p[1]
    