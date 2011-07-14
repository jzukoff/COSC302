import random
import math
import heapq
import copy
import codecs


"""
    Proof of correctness and Running time:
    
    My fastist trip algorithm basically runs Dijkstra's algorithm and then runs through the path generated until the end is reached.
    The variability of the path lengths does not really change the way Dijkstra's algorithm needs to be run. This is because at each
    step the algorithm still chooses the next best option. For instance, at the first stem the shortest edge is taken and the time at that
    edge is updated. Now the blob has grown and the next best option is taken. The only extra thing needed to consider is that further back
    in the blob, the time value is different which is used to compute the new distances. This is easily kept track of and so the problem
    really just boils down to running the generic Dijkstra's algorithm. The formal proof in the book still holds. Namely: after ach iteration
    of the loop 1) all nodes that are in the blob have a distance (time) less than or equal to some value t, 2) for each node the distance (time)
    to that node is the length of the shortest path from the start to that node only going through nodes in the blob.

    The running time is O((|V| + |E|)log|V|) because the python implementation of a heap is a binary heap.
"""
class Node():
    def __init__(self,value):
        self.value = value
        # infinity
        self.dist = float('inf')
        self.prev = None
        self.parent = self
        self.rank = 0
    def __lt__(self, other):
        result = self.dist < other.dist
        return result
    
def makeSet(x):
    x.parent = x
    x.rank = 0

def union(x,y):
    xRoot = find(x)
    yRoot = find(y)
    if xRoot.rank > yRoot.rank:
        yRoot.parent = xRoot
    elif xRoot != yRoot:
        xRoot.parent = yRoot
        if xRoot.rank == yRoot.rank:
            yRoot.rank = yRoot.rank + 1

def find(x):
    if x.parent == x:
        return x
    else:
        x.parent = find(x.parent)
        return x.parent


def clustering(movies,moviesActors, distFunct, k):
    verteces = {}
    edges = []
    for vertex in movies:
        node = Node(vertex)
        verteces[vertex] = node
        makeSet(node)
        for edge in movies:
            edges.append((distFunct(vertex,edge,movies,moviesActors),vertex,edge))
        
    edges.sort()
    for edge in edges:
        if find(verteces[edge[1]]) != find(verteces[edge[2]]):
            union(verteces[edge[1]], verteces[edge[2]])
            clusters = []
            for v in verteces:
                v = verteces[v]
                if find(v) not in clusters:
                   clusters.append(find(v))
            if len(clusters) == k:
                break
    
    clust = {}        
    for ver in verteces:
        parent = verteces[ver].parent.value
        curr = verteces[ver].value
        if parent not in clust:
            clust[parent] = [curr]
        else:
            clust[parent] += [curr]
    clustList = []
    for item in clust:
        clustList.append(clust[item])
    return clustList



# generates random graphs of n nodes
def gen_travel_graph(n):
    G = {0: [], 1: []}
    for i in range(2, n):
        G[i] = []
        for j in range(2, n):
            if i != j and random.random() < 0.6:
                if j not in G[i]:
                    G[i].append(j)

    while len(G[0]) <= math.ceil(n/4):
        nextNode = random.randint(2, n-1)
        if nextNode not in G[0]:
            G[0].append(nextNode)

    count = 0
    while count <= math.ceil(n/4):
        r = random.randint(2, n-1)
        if 1 not in G[r]:
            G[r].append(1)
            count += 1

    return G

# can be used as an edge-timing function
def edge_time(i, j, t):
    r = (i * j) % 3
    if r == 0:
        return t + 1 + math.sqrt(i + (j%3) + t)
    elif r == 1:
        return t + 1 + math.log(i**2 + j**2 + t**2 + 1, 2)
    else:
        return t + 1 + 1.1 * t

    
def fastest_trip(G, f):
    Nodes = Dijkstra(G,0,1,f)
    Path = []
    end = 1
    start = 0
    while True:
        Path.append(end)
        if end == start:
            break
        end = Nodes[end].prev.value
    Path.reverse()
    return Path
        

def Dijkstra(G,start,end,f):
    Nodes = []
    H = []
    t = 0
    start = Node(start)
    start.dist = 0
    Nodes.append(start)
    H.append(start)
    for vertex in G:
        if vertex != 0:
            vertex = Node(vertex)
            vertex.dist = float('inf')
            vertex.prev = None
            vertex.definite = False
            Nodes.append(vertex)
            H.append(vertex)
    heapq.heapify(H)
    while len(H) > 0:
        u = heapq.heappop(H)
        t = u.dist
        neighbors = G[u.value]
        for v in neighbors:
            nextDist = f(u.value,v,t)
            for node in H:
                if node.value == v:
                    v = node
                    break
            if type(v) == type(1):
                pass
            elif  v.dist > u.dist + nextDist:
                v.dist = u.dist + nextDist
                v.prev = u
                

    return Nodes

def distNumActors(movie1,movie2,movies,movieActors):
    return(len(movieActors[movie2])-len(movieActors[movie1]))

def distTitleChars(movie1,movie2,movies,movieActors):
    num = 0
    for char in movie1:
        if char in movie2:
            num+=1
    return num

def movieActorParse(infile):
    movieDict = {}
    infile = codecs.open(infile, 'r','utf-16')
    for line in infile:
        x = line.split('/')
        movie = x[0]
        movieDict[movie] = x[1:]
    return movieDict
    

def actorMovieParse(infile):
    actorDict = {}
    infile = codecs.open(infile, 'r','utf-16')
    for line in infile:
        x = line.split('/')
        movie = x[0]
        actors = x[1:]
        for actor in actors:
            if actor not in actorDict:
                actorDict[actor] = [movie]
            else:
                actorDict[actor] += [movie]
        break
    return actorDict

def movieParse(infile):
    movies = []
    infile = codecs.open(infile, 'r','utf-16')
    for line in infile:
        x = line.split('/')
        movie = x[0]
        movies.append(movie)

    return movies
        
def main():
    G = gen_travel_graph(10)
    print (G)
    path = fastest_trip(G, edge_time)
    print (path)

    infile = input("What is the name of the file: ")
    moviesActors = movieActorParse(infile)
    movies = movieParse(infile)

    # clusters the movies into clusters based on how many actors they have starring
    numActorCluster = clustering(movies,moviesActors,distNumActors,4)

    # clusters the movies into clusters based on how many characters their titles have in common
    titleCharsCommon = clustering(movies,moviesActors,distTitleChars,4)
    print ((numActorCluster))
    print ('\n')
    print ((titleCharsCommon))
if __name__=='__main__':
    main()
