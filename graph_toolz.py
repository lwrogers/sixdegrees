import os
from collections import deque

class Graph(object):
    # Initializing empty graph
    def __init__(self):
        self.adj_list = dict()    # Initial adjacency list is empty dictionary
        self.vertices = set()    # Vertices are stored in a set
        self.degrees = dict()    # Degrees stored as dictionary

    # Checks if (node1, node2) is edge of graph. Output is 1 (yes) or 0 (no).
    def isEdge(self,node1,node2):
        if node1 in self.vertices:        # Check if node1 is vertex
            if node2 in self.adj_list[node1]:    # Then check if node2 is neighbor of node1
                return 1            # Edge is present!

        if node2 in self.vertices:        # Check if node2 is vertex
            if node1 in self.adj_list[node2]:    # Then check if node1 is neighbor of node2
                return 1            # Edge is present!

        return 0                # Edge not present!

    # Add undirected, simple edge (node1, node2)
    def addEdge(self,node1,node2):

        # print('Called')
        if node1 == node2:            # Self loop, so do nothing
            # print('self loop')
            return
        if node1 in self.vertices:        # Check if node1 is vertex
            nbrs = self.adj_list[node1]        # nbrs is neighbor list of node1
            if node2 not in nbrs:         # Check if node2 already neighbor of node1
                nbrs.add(node2)            # Add node2 to this list
                self.degrees[node1] = self.degrees[node1]+1    # Increment degree of node1

        else:                    # So node1 is not vertex
            self.vertices.add(node1)        # Add node1 to vertices
            self.adj_list[node1] = {node2}    # Initialize node1's list to have node2
            self.degrees[node1] = 1         # Set degree of node1 to be 1

        if node2 in self.vertices:        # Check if node2 is vertex
            nbrs = self.adj_list[node2]        # nbrs is neighbor list of node2
            if node1 not in nbrs:         # Check if node1 already neighbor of node2
                nbrs.add(node1)            # Add node1 to this list
                self.degrees[node2] = self.degrees[node2]+1    # Increment degree of node2

        else:                    # So node2 is not vertex
            self.vertices.add(node2)        # Add node2 to vertices
            self.adj_list[node2] = {node1}    # Initialize node2's list to have node1
            self.degrees[node2] = 1         # Set degree of node2 to be 1

    # Give the size of the graph. Outputs [vertices edges wedges]
    #
    def size(self):
        n = len(self.vertices)            # Number of vertices

        m = 0                    # Initialize edges/wedges = 0
        wedge = 0
        for node in self.vertices:        # Loop over nodes
            deg = self.degrees[node]      # Get degree of node
            m = m + deg             # Add degree to current edge count
            wedge = wedge+deg*(deg-1)/2        # Add wedges centered at node to wedge count
        return [n, m, wedge]            # Return size info

    # Print the graph
    def output(self,fname,dirname):
        os.chdir(dirname)
        f_output = open(fname,'w')

        for node1 in list(self.adj_list.keys()):
            f_output.write(str(node1)+': ')
            for node2 in (self.adj_list)[node1]:
                f_output.write(str(node2)+' ')
            f_output.write('\n')
        f_output.write('------------------\n')
        f_output.close()

    def path(self, src, dest):
        """ implement your shortest path function here """
        shortest_path = []    # initialize shortest_path to be an empty array

        visited = {src}    # initialize visited as empty set
        pred = dict()    # initialize and pred as empty sets
        pred[src] = None
        Q = deque()    # make an empty deque object called Q
        Q.append(src)    # appends the src into the tree
        current = src
        while len(Q) != 0:    # while the queue is not empty meaning it still has neighbors
           current = Q.popleft()     # pop current element from the left of queue so it maintains first in first out
           
           if current == dest:    # if the person is found we break the loop
                break
           
           for nbr in self.adj_list[current]:    # iterate over the neighbors of the current node
                if nbr not in visited:    # if the neighbor hasn't been visited we can proceed 
                    visited.add(nbr)    # first thing we do is add it to visited since it has now been visited
                    pred[nbr] = current    # this establishes predecessors of each node so we have a backwards traceable path
                    Q.append(nbr)    # this appends onto the right of the queue the neighbor so it may be assessed in a future loop
        
        while current != None:    # if the current node is not equal to none that means there's still a predecessor to find and write to shortest path
            shortest_path = [current] + shortest_path    # we append current which is the predecessor of the previous current onto the head of the list
            current = pred[current]    # we set current to be the predecessor of itself
        
        return shortest_path    # in the end we return shortest_path which is then handled by six-degrees.py

    def levels(self, src):
        """ implement your level set code here """
        level_sizes = []
        visited = {src}    # initialize visited as empty set
        dist = dict()
        dist[src] = 0
        Q = deque()    # make an empty deque object called Q
        Q.append(src)    # appends the src into the tree
        level_sizes.append(1)    # 1 is the very first level so we append it and ignore that case
        count = 0
        level = 0
        while len(Q) != 0:    # while the queue is not empty meaning it still has neighbors
            current = Q.popleft()    # pop current element from the left of queue so it maintains first in first out
            
            if dist[current] != level and level != 6:   # if the queue has moved on to a node in the next level and it's level isn't 6 then
                    level_sizes.append(count)    # we append the count of the previous level neighbors
                    count = 0    # we reset count to 0
                    level = dist[current]    # we update the level to be that of the distance of the current node
            
            for nbr in self.adj_list[current]:    # iterate over the neighbors of the current node
                if nbr not in visited:    # if the neighbor hasn't been visited we can proceed
                    count += 1    # increment the count by one
                    visited.add(nbr)    # add the neighbor to visited since it has now been visited
                    dist[nbr] = dist[current]+1    # this set the distance of the neighbor to be one more than the node it was a neighbor of
                    Q.append(nbr)    # this appends onto the right of the queue the neighbor so it may be assessed in a future loop
                        
        if level != 6:    # if the level isn't 6
            level_sizes.append(count)    # we can append on the final count
        while len(level_sizes) < 7:    # while length of level sized isn't 7
            level_sizes.append(0)    # we append zeros so it fits formatting
        
        return level_sizes    # we return the array of level sizes 
