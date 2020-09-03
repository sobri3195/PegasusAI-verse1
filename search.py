from queue import Queue, PriorityQueue
import re
import sys
#from Queue import Queue
from queue import PriorityQueue
from heapq import heappush, heappop
import time
start_time = time.time()

#as PriorityQueue is not present in python 2.4 so, a class was created
# class PriorityQueue(Queue):
#     def _init(self, maxsize):
#         self.maxsize = maxsize
#         self.queue = []
#     def _put(self, item):
#         return heappush(self.queue, item)
#     def _get(self):
#         return heappop(self.queue)

#from queue import PriorityQueue
def create_graph(filename):
  graph = {}
  graphDfs ={}
  file = {}
  try:	
   file = open(filename).read().splitlines()
  except IOError:
    print("Error: File does not appear to exist.")
    file = "graph.txt"
    file = open(filename).read().splitlines()
  for line in file:
    if line == "":
        return graph
    line = line.replace(":"," ")
    baş = line[:line.index("{")]
    baş = baş.strip(" ")
    matches = re.findall('[a-zA-Z] [1-9]', line)
    if matches == "":
        print("Doğru formatta giriniz")
        return graph
    while matches:
        line = baş + " " + matches.pop(0)
        nodeA, nodeB, d = line.split()
        graph.setdefault(nodeA, []).append((nodeB, d))
        graph.setdefault(nodeB, []).append((nodeA, d))
  return graph


def create_graphDfs(filename):
  file = {}
  graph = {}
  graphDfs ={}
  try:	
   file = open(filename).read().splitlines()
  except IOError:
    print("Error: File does not appear to exist.")
    file = "graph.txt"
    file = open(filename).read().splitlines()
  for line in file:
    if line == "":
        return graphDfs
    line = line.replace(":"," ")
    baş = line[:line.index("{")]
    baş = baş.strip(" ")
    matches = re.findall('[a-zA-Z] [1-9]', line)
    if matches == "":
        print("Doğru formatta giriniz")
        return graphDfs
    while matches:
        line = baş + " " + matches.pop(0)
        nodeA, nodeB, d = line.split()
        graphDfs.setdefault(nodeA, []).append((nodeB))
  return graphDfs

#############

def bfs_shortest_path(graph, start, goal):
    # keep track of explored nodes
    explored = []
    # keep track of all the paths to be checked
    queue = [[start]]

    # return path if start is goal
    if start == goal:
        return "That was easy! Start = goal"

    # keeps looping until all possible paths have been checked
    while queue:
        # pop the first path from the queue
        path = queue.pop(0)
        # get the last node from the path
        node = path[-1]
        if node not in explored:
            neighbours = graph[node]
            # go through all neighbour nodes, construct a new path and
            # push it into the queue
            for neighbour in neighbours:
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)
                # return path if neighbour is goal
                if neighbour == goal:
                    return new_path

            # mark node as explored
            explored.append(node)

    # in case there's no path between the 2 nodes
    return "So sorry, but a connecting path doesn't exist :("


def bfs_path(graph, start, end):
    """
    Compute DFS(Depth First Search) for a graph
    :param graph: The given graph
    :param start: Node to start BFS
    :param end: Goal-node
    """
    frontier = Queue()
    frontier.put(start)
    explored = []

    while True:
        if frontier.empty():
            raise Exception("No way Exception")
        current_node = frontier.get()
        explored.append(current_node)

        # Check if node is goal-node
        if current_node == end:
            return explored

        for node in graph[current_node]:
            if node not in explored:
                frontier.put(node)



route=[]
visited=[]

def dfs(graph,start,destination):
     route.append(start)
     while len(route)>0:
         vertex=route.pop(len(route)-1)
         if vertex not in visited:
             visited.append(vertex)
             route.extend(set(graph[vertex])-set(visited))
         if visited.__contains__(destination):
            return  visited
     return visited


def dfs_path(graph,start,end):
    result = []
    dfsall(graph,start,end,[],result)
    return result

def dfsall(graph,start,end,path,result):
    path+=[start]
    if start == end:
        result.append(path)
    else:
        for node in graph[start]:
            if node not in path:
                dfsall(graph,node,end,path[:],result)

######$$$$$$$#################


def uniformed_cost_search(graph, start, goal): 
  visited = set() #keeps track of all visited nodes
  path = [] #stores the path for each iteration
  queue = PriorityQueue() #stores and sorts all neighbours
  queue.put((0, [start]))
  while queue:

    #if there is no path between two nodes
    if queue.empty():
      print ('distance: infinity\nroute:\nnone')
      print("--- %s seconds ---" % (time.time() - start_time))
      return

    cost, path = queue.get()
    node = path[len(path)-1]
    if node not in visited:
      visited.add(node)
      if node == goal:
        path.append(cost) #the shortest path is found
        return path

      for x in neighbors(graph, node):
        if x not in visited:
          total_cost = cost + int(get_cost(graph, node, x))
          temporary = path[:]
          temporary.append(x)
          queue.put((total_cost, temporary)) #creating queue such that it has all the values for path

def neighbors(graph,node):
  #finding neighbors in graph
  elements = graph[node]
  return [x[0] for x in elements]

def get_cost(graph, from_node, to_node):
  #calc. cost of each edge
  position = [x[0] for x in graph[from_node]].index(to_node)
  return graph[from_node][position][1]

def display_path(graph,path):
  #display in proper format
  print("UCS : ", end = '')
  for x in path[:-1]:
      if x == path[-2]:
        print(str(x))
      else:
        print(str(x)+" - ", end = '')
  distance = path[-1]
  print ('distance: %s'%(distance))
  print ('route: ')
  for x in path[:-2]:
    y = path.index(x)
    position = [z[0] for z in graph[x]].index(path[y+1])
    cost = graph[x][position][1]
    print ('%s to %s, %s km' %(x,path[y+1],cost))#str(x) + ' to ' +str(path[y+1])+',' + ' '+ str(cost) + ' km' #


  print("--- %s seconds ---" % (time.time() - start_time))

def main():
  #reading all arguments
  print("Your graph file must be this format : A:{A:0, B:6, C:4, D:3, E:0, F:0, G:0}")
  filename = "graph.txt"
  try:
   filename = sys.argv[1]
  except:
   filename = "graph.txt"

  start = input("Please enter the start state : (Must be UpperCase letter) ")
  goal = input("Please enter the goal state : (Must be UpperCase letter) ")

  #create Graph (from input file)
  graph = {}
  graphDfsBfs = {}
  graph = create_graph(filename)
  graphDfsBfs = create_graphDfs(filename)

  print("##############################################")
  bfs = bfs_shortest_path(graphDfsBfs, start,goal) # {'E', 'D', 'F', 'A', 'C', 'B'}
  print("BFS : ", end=" ")
  j=0
  for i in bfs:
    if i == bfs[-1]:
      print(bfs[j]+ " (Shortest path of BFS)")
    else:
      print(bfs[j] +" - " , end=" ")
      j+=1

  print("##############################################")

  dfss = dfs(graphDfsBfs, start,goal) # {'E', 'D', 'F', 'A', 'C', 'B'}
  print("DFS : ", end=" ")
  j=0
  for i in dfss:
    if i == dfss[-1]:
      print(dfss[j] + " (Randomly Selected every time)")
    else:
      print(dfss[j] +" - " , end=" ")
      j+=1



  dfsall = dfs_path(graphDfsBfs, start,goal) # {'E', 'D', 'F', 'A', 'C', 'B'}
  print("All possibilities for DFS : ", end=" ")
  j=0
  for i in dfsall:
    if i == dfsall[-1]:
      print()
    else:
      print(str(dfsall[j]) +" - " , end=" ")
      j+=1


  #print(repr([path for path in dfs_paths(graphDfsBfs, 'A', 'F')]))
  print("##############################################")



#checking for exceptions
  if start not in graph.keys():
    print ('wrong  start point')
    sys.exit()
  if goal not in graph.keys():
    print ('wrong goal node')
    sys.exit()

  #finding path and cost using Uniformed Cost Search
  path = []
  path = uniformed_cost_search(graph, start, goal)

  #Display path (if exists)
  if path:
    display_path(graph,path)


if __name__ == '__main__': 
  main()
