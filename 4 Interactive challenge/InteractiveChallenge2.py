import networkx as nx
import matplotlib.pyplot as plt
import heapq
import random
import tkinter as tk
from tkinter import simpledialog

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

def create_random_graph():
    num_nodes = random.randint(6, 8)
    g = Graph()
    nodes = [chr(i) for i in range(65, 65 + num_nodes)]  # A, B, C...

    for i in range(num_nodes):
        for j in range(i+1, num_nodes):
            if random.random() < 0.5:
                weight = random.randint(1, 10)
                g.add_edge(nodes[i], nodes[j], weight)

    return g, nodes

def select_challenging_nodes(g, nodes):
    max_dist = 0
    farthest_nodes = (None, None)
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            path, dist = g.shortest_path(nodes[i], nodes[j])
            if dist < float('inf') and dist > max_dist:
                max_dist = dist
                farthest_nodes = (nodes[i], nodes[j])
    return farthest_nodes

def draw_graph(g, pos):
    plt.clf()
    nx.draw(g.graph, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10)
    labels = nx.get_edge_attributes(g.graph, 'weight')
    nx.draw_networkx_edge_labels(g.graph, pos, edge_labels=labels)
    plt.title("Click on any two nodes to explore paths")
    plt.draw()

def ask_path_through_gui(correct_path, dist):
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    print(f"\nChallenge: Enter the shortest path between the selected nodes.")
    print(f"Total cost: {dist}")
    print("You must enter nodes one by one in order.")

    for i, correct_node in enumerate(correct_path):
        answer = simpledialog.askstring("Path Input", f"Enter node {i+1} of {len(correct_path)}:")
        if answer is None:
            print("User cancelled.")
            return
        if answer != correct_node:
            print("Wrong answer!")
            return
    print("✅ Correct! You followed the correct shortest path.")

def onclick(event, g, pos):
    if event.xdata is None or event.ydata is None:
        return

    closest_node = min(pos, key=lambda node: (pos[node][0] - event.xdata) ** 2 + (pos[node][1] - event.ydata) ** 2)
    selected_nodes.append(closest_node)
    print(f"Node selected: {closest_node}")

    if len(selected_nodes) == 2:
        source, target = selected_nodes
        path, dist = g.shortest_path(source, target)
        print(f"\nNow enter the shortest path from {source} to {target}")
        ask_path_through_gui(path, dist)
        selected_nodes.clear()

def main():
    global selected_nodes
    selected_nodes = []

    g, nodes = create_random_graph()
    source, target = select_challenging_nodes(g, nodes)

    if source is None or target is None:
        print("⚠️ Couldn't find a path. Try rerunning the script.")
        return

    print(f"🔍 Problem: Find the shortest path from {source} to {target}")

    pos = nx.spring_layout(g.graph)
    fig, ax = plt.subplots()
    draw_graph(g, pos)
    fig.canvas.mpl_connect('button_press_event', lambda event: onclick(event, g, pos))
    plt.show()

main()
