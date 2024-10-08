import networkx as nx
import matplotlib.pyplot as plt
import heapq
import random

class Graph:
    def __init__(self):
        self.graph = nx.Graph()

    def add_edge(self, u, v, weight):
        self.graph.add_edge(u, v, weight=weight)

    def dijkstra(self, source):
        dist = {node: float('inf') for node in self.graph.nodes}
        dist[source] = 0
        priority_queue = [(0, source)]
        prev = {node: None for node in self.graph.nodes}

        while priority_queue:
            current_dist, current_node = heapq.heappop(priority_queue)

            if current_dist > dist[current_node]:
                continue

            for neighbor, attributes in self.graph[current_node].items():
                distance = attributes['weight']
                new_dist = current_dist + distance

                if new_dist < dist[neighbor]:
                    dist[neighbor] = new_dist
                    prev[neighbor] = current_node
                    heapq.heappush(priority_queue, (new_dist, neighbor))

        return dist, prev

    def shortest_path(self, source, target):
        dist, prev = self.dijkstra(source)
        path = []
        node = target
        while node is not None:
            path.append(node)
            node = prev[node]
        path.reverse()
        return path, dist[target]

# Create a random graph with 6 to 8 nodes and random weights
def create_random_graph():
    num_nodes = random.randint(6, 8)  # Random number of nodes between 6 and 8
    g = Graph()
    
    nodes = [chr(i) for i in range(65, 65 + num_nodes)]  # A, B, C, etc.

    # Randomly generate edges with weights between nodes
    for i in range(num_nodes):
        for j in range(i+1, num_nodes):
            if random.random() < 0.5:  # 50% chance of edge between any two nodes
                weight = random.randint(1, 10)  # Random weight between 1 and 10
                g.add_edge(nodes[i], nodes[j], weight)
    
    return g, nodes

# Function to select two nodes that are relatively far from each other
def select_challenging_nodes(g, nodes):
    max_dist = 0
    farthest_nodes = (None, None)
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            path, dist = g.shortest_path(nodes[i], nodes[j])
            if dist > max_dist:
                max_dist = dist
                farthest_nodes = (nodes[i], nodes[j])
    return farthest_nodes

# Set the layout for node positions
def draw_graph(g, pos):
    plt.clf()
    nx.draw(g.graph, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10)
    labels = nx.get_edge_attributes(g.graph, 'weight')
    nx.draw_networkx_edge_labels(g.graph, pos, edge_labels=labels)
    plt.title("Click on two nodes to find the shortest path")
    plt.draw()

# Function to handle mouse click events
def onclick(event, g, pos):
    if event.xdata is None or event.ydata is None:
        return

    # Find the closest node to the click position
    closest_node = min(pos, key=lambda node: (pos[node][0] - event.xdata) ** 2 + (pos[node][1] - event.ydata) ** 2)
    selected_nodes.append(closest_node)
    print(f"Node selected: {closest_node}")

    if len(selected_nodes) == 2:
        source, target = selected_nodes
        path, dist = g.shortest_path(source, target)
        print(f"Cost of shortest path from {source} to {target}: {dist}")
        
        # Let the students input nodes one by one
        input_nodes_for_path(path, dist)
        selected_nodes.clear()

# Function to handle student input and check for correctness
def input_nodes_for_path(path, dist):
    print(f"Cost of shortest path: {dist}")
    print(f"Please follow the path by inputting the nodes one by one:")
    for i in range(len(path)):
        node_input = input(f"Enter node {i + 1} in the path: ")
        if node_input != path[i]:
            print("Wrong answer!")
            return
    print("Congratulations, you followed the correct path!")

# Main function to generate a new graph and start the interaction
def main():
    # Generate random graph
    g, nodes = create_random_graph()
    
    # Find two nodes that are far apart to make the problem challenging
    source, target = select_challenging_nodes(g, nodes)
    print(f"Problem for student: Find the shortest path between {source} and {target}")

    # Set up the figure and draw the graph
    pos = nx.spring_layout(g.graph)
    fig, ax = plt.subplots()
    draw_graph(g, pos)

    # Connect the click event to the onclick function
    cid = fig.canvas.mpl_connect('button_press_event', lambda event: onclick(event, g, pos))

    plt.show(block=True)

# Initialize variables
selected_nodes = []

# Run the main function
main()
