import math, sys, random
import matplotlib.pyplot as plot

clusters = []

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

class Cluster(object):
    """ it represents a cluster/classification which holds classified points """
    def __init__(self, centroid):
        self.label = ''
        self.points = []
        self.centroid = centroid
        self.radius = 0.0
    
    def add(self, point):
        self.points.append(point)
    
    def calc_centroid(self):
        """ calculate new centroid based on classified points """
        sumX = 0.0
        sumY = 0.0
        dis = 0.0
        for p in self.points:
            sumX += p.x
            sumY += p.y
            d = math.sqrt((p.x - self.centroid.x) ** 2 + (p.y - self.centroid.y) ** 2)
            if dis < d: dis = d
        self.radius = dis + 0.1
        size = len(self.points)
        if size == 0: return self.centroid
        else:
            return Point(sumX/size, sumY/size)
    
    def update(self):
        """ update new centroid and calculate diff between two centroids """
        old_centroid = self.centroid
        self.centroid = self.calc_centroid()
        return old_centroid.distance(self.centroid)
    
    def __eq__(self, other):
        return self.centroid == other.centroid
    
    def __repr__(self):
        return "cluster '" + self.label + "' at " + str(self.centroid)

def _empty_clusters():
    for cl in clusters:
        cl.points = []

def kmeans(dataset, k, threshold=1e-10):
    """
    1. create k random clusters
    2. for each point, find nearest cluster and put it into it
    3. calculate new centroid for each cluster
    4. repeat step 2 and step 3 until diff is less than threshold
    """
    diff = threshold + 1.0
    _create_random_clusters(dataset, k)
    
    _print_location(clusters)
    
    while diff > threshold:
        _empty_clusters()
        for p in dataset:
            min_dis = sys.maxint
            min_cls = None
            for cl in clusters:
                dis = p.distance(cl.centroid)
                if (min_dis > dis):
                    min_dis = dis
                    min_cls = cl
            min_cls.add(p)
        diff = 0.0
        for cls in clusters:
            diff += cls.update()

def _print_location(clts):
    """ print the centroid location of each cluster """
    print "===================================="
    for cls in clts:
        print "Cluster " + cls.label + " initially at " + str(cls.centroid)
    print "===================================="
    print

def _create_random_clusters(dataset, k):
    """
    I want to create random clusters based on the dataset space,
    if the cluster is far away from the points,
    it won't make any sense.
    """
    minX = sys.maxint
    maxX = -sys.maxint
    minY = sys.maxint
    maxY = -sys.maxint
    
    for p in dataset:
        if p.x < minX: minX = p.x
        if p.x > maxX: maxX = p.x
        if p.y < minY: minY = p.y
        if p.y > maxY: maxY = p.y
    
    while len(clusters) < k:
        px = random.randint(minX, maxX)
        py = random.randint(minY, maxY)
        pt = Point(px, py)
        cluster = Cluster(pt)
        if cluster not in clusters:
            """ never store save clusters """
            label = len(clusters)
            cluster.label = chr(97+label)
            clusters.append(cluster)

def draw_plot(clts):
    """ 
    draw a plot diagram for all clusters.
    it has data points, centroids and domain covers
    """
    plot.title("k-means algorithm")
    plot.axis([0, 20, 0, 20])
    plot.xticks(range(0, 20, 1))
    plot.yticks(range(0, 20, 1))
    for cls in clts:
        color = (random.random(), random.random(), random.random())
        cir = plot.Circle((cls.centroid.x, cls.centroid.y), radius=cls.radius, alpha=0.4, fc=color)
        plot.gca().add_patch(cir)
        plot.plot([cls.centroid.x], [cls.centroid.y], '^')
        plot.text(cls.centroid.x + 0.15, cls.centroid.y + 0.15, cls.label)
        plot.plot([p.x for p in cls.points], [p.y for p in cls.points], 'o')
        plot.grid(True)
    plot.show()


if __name__ == '__main__':
    
    p1 = Point(2, 6)
    p2 = Point(3, 14)
    p3 = Point(4, 5)
    p4 = Point(5, 14)
    p5 = Point(10, 10)
    p6 = Point(11, 9)
    p7 = Point(11, 14)
    p8 = Point(12, 2)
    p9 = Point(14, 14)
    p10 = Point(15, 14)
    p11 = Point(17, 13)
    p12 = Point(16, 7)
    p13 = Point(17, 6)
    
    dataset = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13]
    
    kmeans(dataset, 4)
    
    print "===================================="
    for cl in clusters:
        print "cluster " + cl.label + " " + str(cl.centroid) + " has points: " + str(cl.points)
    print "===================================="
    
    draw_plot(clusters)
    