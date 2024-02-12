class Graph:
    def __init__(self, nodes): #constructor for the graph
        self.nodes = nodes #list of nodes
        self.adjacency_list = {node: {} for node in nodes} #creates a dictionary to store adjacency list

####################################################################################################################

    def add_edge(self, node1, node2, weight): 
        self.adjacency_list[node1][node2] = weight
        self.adjacency_list[node2][node1] = weight  # Assuming the graph is undirected, add edge in both directions

####################################################################################################################
        
    def dijkstra(self, start_node):
        shortest_paths = {node: float('infinity') for node in self.nodes} #dictionary with all nodes with distance infinity
        shortest_paths[start_node] = 0 
        previous_nodes = {} #dictionary to store the previous node of each node in the shortest path
        unvisited_nodes = self.nodes.copy() #list of unvisited nodes

####################################################################
        
        while unvisited_nodes: #loop continues till there are unvisited nodes
            current_node = min(unvisited_nodes, key=lambda node: shortest_paths[node]) #node with smallest tentative distance in unvisted_nodes
            unvisited_nodes.remove(current_node) #remove current_node from unvisited_nodes

#############################################################################################

            for neighbor, weight in self.adjacency_list[current_node].items(): #this loop iterates over all unvisited neighbors of current node
                if neighbor in unvisited_nodes: 
                    new_path = shortest_paths[current_node] + weight #calculate distance of neighbor from start_node
                    if new_path < shortest_paths[neighbor]: #if new_path is less than the current distance of neighbor from start_node
                        shortest_paths[neighbor] = new_path #update shortest_path
                        previous_nodes[neighbor] = current_node #update previous_nodes




        return previous_nodes, shortest_paths 

# Example Usage
nodes = ["A", "B", "C", "D", "E"]
graph = Graph(nodes)
graph.add_edge("A", "B", 6)
graph.add_edge("A", "D", 1)
graph.add_edge("D", "B", 2)
graph.add_edge("B", "C", 5)
graph.add_edge("D", "E", 1)
graph.add_edge("E", "C", 5)

start_node = "A"
previous_nodes, shortest_paths = graph.dijkstra(start_node)

print(f"Shortest paths from {start_node}: {shortest_paths}")
print(f"Previous nodes: {previous_nodes}")
print("Shortest path from A to C:" + str(shortest_paths["C"]))
print("Shortest path from A to B:" + str(shortest_paths["B"]))
print("Shortest path from A to D:" + str(shortest_paths["D"]))
print("Shortest path from A to E:" + str(shortest_paths["E"]))
print('adjaency list: ' + str(graph.adjacency_list))