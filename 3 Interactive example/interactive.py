import networkx as nx
import matplotlib.pyplot as plt
import heapq

# Define the graph class with Dijkstra's algorithm
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

# Create a Graph instance and add edges
g = Graph()

edges = [
    ('A', 'B', 1), ('A', 'C', 4),
    ('B', 'C', 2), ('B', 'D', 5),
    ('C', 'D', 1), ('D', 'E', 3)
]

for u, v, weight in edges:
    g.add_edge(u, v, weight)

# Set the layout for node positions
pos = nx.spring_layout(g.graph)

# Global list to store selected nodes
selected_nodes = []

# Function to draw the graph
def draw_graph():
    plt.clf()
    nx.draw(g.graph, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10)
    labels = nx.get_edge_attributes(g.graph, 'weight')
    nx.draw_networkx_edge_labels(g.graph, pos, edge_labels=labels)
    plt.title("Click on two nodes to find the shortest path")
    plt.draw()

# Function to handle mouse click events
def onclick(event):
    if event.xdata is None or event.ydata is None:
        return

    # Find the closest node to the click position
    closest_node = min(pos, key=lambda node: (pos[node][0] - event.xdata) ** 2 + (pos[node][1] - event.ydata) ** 2)
    selected_nodes.append(closest_node)
    print(f"Node selected: {closest_node}")

    # When two nodes are selected, calculate and draw the shortest path
    if len(selected_nodes) == 2:
        source, target = selected_nodes
        path, dist = g.shortest_path(source, target)
        print(f"Shortest path from {source} to {target}: {path}, Distance: {dist}")
        draw_path(path)
        selected_nodes.clear()

# Function to highlight the shortest path
def draw_path(path):
    plt.clf()
    nx.draw(g.graph, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10)
    nx.draw_networkx_nodes(g.graph, pos, nodelist=path, node_color='green')
    nx.draw_networkx_edges(g.graph, pos, edgelist=list(zip(path, path[1:])), edge_color='red', width=2)
    labels = nx.get_edge_attributes(g.graph, 'weight')
    nx.draw_networkx_edge_labels(g.graph, pos, edge_labels=labels)
    plt.draw()

# Set up the figure and enable interactive mode
fig, ax = plt.subplots()
draw_graph()

# Connect the click event to the onclick function
fig.canvas.mpl_connect('button_press_event', onclick)

plt.show(block=True)
