from inspect import GEN_CREATED
import random
import matplotlib
import networkx
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout

debugging = False
yes_or_no = input("Are you just testing it? [y/n]")
if yes_or_no == "y":
    debugging = True

while True:
    G=nx.Graph()
    
    # CONFIGURATION:
    number_of_ws_per_vi = 5
    number_of_vis = 4
    
        
    w_sets = []
    
    def w_already_exists(w_sets, w):
        for i in range(0, len(w_sets)):
            for j in range(0, len(w_sets[i])):
                if w_sets[i][j] == w:
                    return True
        return False
    
    amount_of_ws = 0
    for i in range(0, number_of_vis): # SETTING UP W'S
        w_sets.append([])
        for j in range(0, number_of_ws_per_vi):
            new_w_number = random.randint(0, 35)
            while w_already_exists(w_sets, new_w_number) == True:
                new_w_number = random.randint(0, 35)
            w_sets[i].append(new_w_number)
    
    print("W'S: " + str(w_sets))
    
    def vertex_is_a_w(vertex): # CHECKS IF VERTEX IS A NEIGHBOR OF THE VI'S
        found = False
        for i in range(0, len(w_sets)):
            for j in range(0, len(w_sets[i])):
                if vertex == w_sets[i][j]:
                    found = True
        return found
    
    def vertices_in_same_w_set(vertex1, vertex2):
        for i in range(0, len(w_sets)):
            if vertex1 in w_sets[i] and vertex2 in w_sets[i]:
                return True
        return False
    
    def check_common_neighbor(list1, list2):
        found_common = False
        for i in range(0, len(list1)):
            if list1[i] in list2:
                found_common = True
        return found_common
    
    def amount_of_neighbors(vertex, matrix):
        amount = 0
        for i in range(0, len(matrix)):
            if matrix[i][vertex] != 0:
                amount += 1
        return amount
    
    def get_neighbors(vertex, matrix):
        neighbors = []
        for i in range(0, len(matrix[vertex])):
            if matrix[vertex][i] != 0:
                neighbors.append(i)
        return neighbors
    
    def find_triangle(matrix):
        for line in range(len(matrix)): # Initial connections
            for column in range(len(matrix[line])):
                if line == line: # Bottom left corner of matrix
                    # Making sure they are both connected to 2 vertices
                    if matrix[line][column] == 1 and amount_of_neighbors(line, matrix) >= 2 and amount_of_neighbors(column, matrix) >= 2:
                        line_neighbors = get_neighbors(line, matrix)
                        column_neighbors = get_neighbors(column, matrix)
                        for line_neighbor in line_neighbors:
                            if line_neighbor in column_neighbors:
                                return [line, column, line_neighbor]
                        for column_neighbor in column_neighbors:
                            if column_neighbor in line_neighbors:
                                return [line, column, column_neighbor]
    
            
    
    def make_graph_matrix(): # MAKING GRAPH MATRIX, WHERE AVOINDING TRIANGLES MUST HAPPEN
        matrix = []
    
        for i in range(0, 35): # Setting up matrix empty lines
            matrix.append([])
        for i in range(0, 35):
            for j in range(0, 35):
                matrix[i].append(0)
    
        for line in range(0, 35): # MAKING INITIAL CONNECTIONS
            for column in range(0, 35):
                if line != column: # If it's not the diagonal
                    if vertices_in_same_w_set(line, column) == True: # If both vertices are w's in the same set
                        matrix[line][column] = 0
                        matrix[column][line] = 0
                    else: # If it's either 2 h's or a W and an H or 2 W's from different sets
                        neighbors_of_line = get_neighbors(line, matrix)
                        neighbors_of_column = get_neighbors(column, matrix)
                        has_common_neighbor = check_common_neighbor(neighbors_of_line, neighbors_of_column)
    
                        if has_common_neighbor == False and amount_of_neighbors(line, matrix) < 8 and amount_of_neighbors(column, matrix) < 8:
                            matrix[column][line] = 1
                            matrix[line][column] = 1
                        else:
                            matrix[line][column] = 0
                            matrix[column][line] = 0
                else: # If it is the diagonal
                    matrix[line][column] = 0
                    matrix[column][line] = 0
    
        return matrix
    
    def draw_graph(matrix):
        for line in range(0, len(matrix)):
            print("Drawing graph at line " + str(line))
            for column in range(0, len(matrix[line])):
                if line != column: # If it's not in the diagonal
                    color = 0
                    if matrix[line][column] != 0:
                        if matrix[line][column] == 1:
                            color = 'blue'
                        vertex1_name = str(line)
                        vertex2_name = str(column)
    
                        if vertex_is_a_w(line) == True:
                            vertex1_name = "W" + str(line)
                        else:
                            vertex1_name = "h" + str(line)
                        
                        if vertex_is_a_w(column) == True:
                            vertex2_name = "W" + str(column)
                        else:
                            vertex2_name = "h" + str(column)
    
                        G.add_edge(vertex1_name, vertex2_name, color=color, weight=1)
    
    def color_vertices(vertex_color_map):
        for node in G:
            node_name = str(node)
            if "W" in node_name:
                node_number = str(node_name).replace("W", "")
                if int(node_number) in w_sets[0]:
                    vertex_color_map.append('purple')
                if int(node_number) in w_sets[1]:
                    vertex_color_map.append('yellow')
                if int(node_number) in w_sets[2]:
                    vertex_color_map.append('orange')
                if int(node_number) in w_sets[3]:
                    vertex_color_map.append('limegreen')
            else:
                vertex_color_map.append('blue')
    
    matrix = make_graph_matrix()
    
    for i in range(0, 35):
       print(str(i) + " has " + str(amount_of_neighbors(i, matrix)) + " neighbors")
    
    failed_to_fix_all = False
    
    for line in range(0, 34): # making sure all vertices have 8 neighbors
        amount_of_neighbors_line = amount_of_neighbors(line, matrix)
        if amount_of_neighbors_line != 8:
            print("Trying to get vertex " + str(line) + " with " + str(amount_of_neighbors_line) + " neighbors fixed")
            amount_of_tries = 0
            while amount_of_neighbors(line, matrix) != 8:
                if amount_of_tries > 200:
                    failed_to_fix_all = True
                    print("Tried too many times, quitting")
                    break
                amount_of_tries += 1
                possible_new_neighbor = random.randint(0, 34)
    
                neighbors_of_line = get_neighbors(line, matrix)
                neighbors_of_new_neighbor = get_neighbors(possible_new_neighbor, matrix)
                has_common_neighbor = check_common_neighbor(neighbors_of_line, neighbors_of_new_neighbor)
    
                if has_common_neighbor == False and possible_new_neighbor != line and vertices_in_same_w_set(line, possible_new_neighbor) == False and amount_of_neighbors(possible_new_neighbor, matrix) < 8:
                    matrix[line][possible_new_neighbor] = 1
                    matrix[possible_new_neighbor][line] = 1
    
    for i in range(0, 35):
       print(str(i) + " has " + str(amount_of_neighbors(i, matrix)) + " neighbors")
    
    draw_graph(matrix)
    
    triangle = find_triangle(matrix)
    # k10 = find_k10(matrix)
    
    pos = nx.circular_layout(G)
    edges = G.edges()
    colors = [G[u][v]['color'] for u,v in edges]
    weights = [G[u][v]['weight'] for u,v in edges]
    
    # FINDING CI'S and stuff
    
    for i in range(0, 35):
       print(str(i) + " has " + str(amount_of_neighbors(i, matrix)) + " neighbors")
    
    
    print("Triangle: " + str(triangle))
    # print("K10: " + str(k10))
    
    print(str(matrix).replace("]", "\n"))
    
    vertex_color_map = []   
    
    color_vertices(vertex_color_map)
    
    nx.draw(G, pos, edge_color=colors, width=1, with_labels=True, node_color=vertex_color_map)
    
    if failed_to_fix_all == False:
        plt.show()

    if debugging:
        plt.show()

    plt.clf()
    G.clear()
