import networkx as nx
import matplotlib.pyplot as plt

# Havel-Hakimi Algorithm to check if sequence is graphical
def havel_hakimi(seq):
    seq.sort(reverse=True)
    while seq and seq[0] == 0:
        seq.pop(0)
    if sum(seq) % 2 != 0:
        return False  # Not a graphic sequence
    while seq:
        d = seq.pop(0)
        if d > len(seq):
            return False
        for i in range(d):
            seq[i] -= 1
        seq.sort(reverse=True)
    return True

# Check if the graph is Eulerian
def is_eulerian(G):
    return nx.is_eulerian(G)

# Fleury’s Algorithm for finding Eulerian path
def fleury_algorithm(G):
    if not is_eulerian(G):
        return None
    euler_path = list(nx.eulerian_circuit(G)) if nx.is_eulerian(G) else None
    return euler_path

# Assign user input weights to edges
def assign_user_weights(G):
    for (u, v) in G.edges():
        weight = int(input(f"Enter weight for edge ({u}, {v}): "))
        G.edges[u, v]['weight'] = weight

# Dijkstra’s algorithm to find shortest paths from source vertex
def dijkstra_shortest_path(G, source):
    return nx.single_source_dijkstra_path_length(G, source, weight='weight')

# Prim's algorithm to find Minimum Spanning Tree
def minimum_spanning_tree(G):
    mst = nx.minimum_spanning_tree(G, algorithm='prim')
    return mst

# Plot graph with edge weights
def plot_graph(G):
    pos = nx.spring_layout(G)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=700)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title("Original Graph")
    plt.show()

# Plot the Minimum Spanning Tree
def plot_mst(mst):
    pos = nx.spring_layout(mst)
    edge_labels = nx.get_edge_attributes(mst, 'weight')
    nx.draw(mst, pos, with_labels=True, node_color='lightgreen', node_size=700)
    nx.draw_networkx_edge_labels(mst, pos, edge_labels=edge_labels)
    plt.title("Minimum Spanning Tree")
    plt.show()

# Find fundamental cutsets and circuits with respect to MST
def fundamental_cutsets_and_circuits(G, mst):
    cutsets = []
    circuits = []
    
    for edge in G.edges():
        if edge not in mst.edges():
            cutsets.append(edge)  # Cutset is the edge not in MST

    for edge in cutsets:
        u, v = edge
        # Create a circuit by adding the edge back to the MST and finding a cycle
        new_mst = mst.copy()
        new_mst.add_edge(u, v)
        # Find all circuits in the graph
        circuits.extend(list(nx.simple_cycles(new_mst)))

    return cutsets, circuits

# Calculate the vertex connectivity manually
def vertex_connectivity(G):
    min_conn = float('inf')
    for node in G.nodes():
        # Create a copy of the graph without the current node
        temp_graph = G.copy()
        temp_graph.remove_node(node)
        # Check if the graph is still connected
        if not nx.is_connected(temp_graph):
            return 1  # If the graph is not connected, the connectivity is at least 1
        # Count the number of connected components
        conn = list(nx.connected_components(temp_graph))
        min_conn = min(min_conn, len(conn) - 1)
    return min_conn if min_conn != float('inf') else 0

# Get user input for the degree sequence
seq = list(map(int, input("Enter the degree sequence (space-separated integers): ").split()))

if havel_hakimi(seq[:]):
    G = nx.havel_hakimi_graph(seq)  # Generate graph using Havel-Hakimi
    assign_user_weights(G)  # Assign user-provided weights to edges
    plot_graph(G)  # Plot the graph

    # Check if the graph is Eulerian
    if is_eulerian(G):
        print("The graph is Eulerian.")
        euler_path = fleury_algorithm(G)
        if euler_path:
            print("Euler Path/Circuit:", list(euler_path))
    else:
        print("The graph is not Eulerian.")
    
    # Get source vertex from user for shortest path computation
    source_vertex = int(input("Enter the source vertex: "))
    
    if source_vertex in G.nodes():
        shortest_paths = dijkstra_shortest_path(G, source_vertex)
        print("\nShortest distances from vertex", source_vertex, "to all other vertices:")
        for vertex, distance in shortest_paths.items():
            print(f"Vertex {vertex}: Distance {distance}")
    else:
        print("Invalid source vertex.")

    # Find Minimum Spanning Tree
    mst = minimum_spanning_tree(G)
    print("\nMinimum Spanning Tree (edges and weights):")
    for edge in mst.edges(data=True):
        print(f"Edge {edge[0]}-{edge[1]}: Weight {edge[2]['weight']}")

    # Plot the Minimum Spanning Tree
    plot_mst(mst)

    # Find fundamental cutsets and circuits
    cutsets, circuits = fundamental_cutsets_and_circuits(G, mst)
    
    print("\nFundamental Cutsets:")
    for cutset in cutsets:
        print(f"Cutset: {cutset}")

    print("\nFundamental Circuits:")
    for circuit in circuits:
        print(f"Circuit: {circuit}")

    # Calculate edge connectivity
    edge_conn = nx.edge_connectivity(G)
    # Calculate vertex connectivity
    vertex_conn = vertex_connectivity(G)

    print("\nEdge Connectivity of the graph:", edge_conn)
    print("Vertex Connectivity of the graph:", vertex_conn)

    # Determine K-connected value
    k_connected_value = min(edge_conn, vertex_conn)
    print("Value of K for which the graph is K-connected:", k_connected_value)

else:
    print("Not a valid graphic sequence.")
