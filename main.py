from inspect import GEN_CREATED
import random
import matplotlib
import networkx
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout

# Things to do:
# turn graph into a tree
# Make triangle and 10-CI detector based on finding clumps of vertices

eight_ci = []
seven_ci = []
six_ci = []
five_ci = []
four_ci = []

run_time_cis = []

vi_neighbors_list = [[], [], [], []]

# Blue triangle and Red K10 R(3, 10)
# No edge = 0
# Blue = 1
# Red = 2

for i in range(0, 30): # Adding the numbers to each independent set
    if i < 8:
        eight_ci.append(i)
    if i > 7 and i < 15:
        seven_ci.append(i)
    if i > 14 and i < 21:
        six_ci.append(i)
    if i > 20 and i < 26:
        five_ci.append(i)
    if i > 25 and i < 30:
        four_ci.append(i)

def vertex_is_a_w(vertex):
    found = False
    for i in range(0, len(vi_neighbors_list)):
        for j in range(0, len(vi_neighbors_list[i])):
            if vertex == vi_neighbors_list[i][j]:
                found = True
    return found

def is_part_of_ci(number1, number2): # Check if two numbers are in an independent set
    ci_list = [eight_ci, seven_ci, six_ci, five_ci, four_ci, run_time_cis]
    for i in range(0, len(vi_neighbors_list)):
        ci_list.append(vi_neighbors_list[i])

    for i in range(0, len(ci_list)):
        number1_is_in_ci = False
        number2_is_in_ci = False
        for j in range(0, len(ci_list[i])):
            if number1 == ci_list[i][j]:
                number1_is_in_ci = True
            if number2 == ci_list[i][j]:
                number2_is_in_ci = True
            if number1_is_in_ci == True and number2_is_in_ci == True:
                return True
    print(str(number1) + " and " + str(number2) + " aren't in " + str(ci_list))
    return False

def amount_of_neighbors(vertex, matrix):
    amount = 0
    for i in range(0, len(matrix[vertex])):
        if matrix[vertex][i] != 0:
            amount += 1
    return amount

def get_neighbors(vertex, matrix):
    neighbors = []
    for i in range(0, len(matrix[vertex])):
        if matrix[vertex][i] != 0:
            neighbors.append(i)
    return neighbors

def make_graph(w_number, h_number):
    matrix = []
    for i in range(0, w_number+h_number):
        matrix.append([])

    for vi in range(0, len(vi_neighbors_list)):
        number_of_neighbors = 0

        while number_of_neighbors != 5: # ADDING W'S
            random_number = random.randint(0, w_number+h_number-1)
            found_it_in_vi = False
            for i in range(0, len(vi_neighbors_list)):
                for j in range(0, len(vi_neighbors_list[i])):
                    if random_number == vi_neighbors_list[i][j]:
                        found_it_in_vi = True
            if found_it_in_vi == False:
                vi_neighbors_list[vi].append(random_number)
                number_of_neighbors += 1

    print("VI NEIGHBOR LIST: " + str(vi_neighbors_list))

    for line in range(0, w_number+h_number):
        for column in range(0, w_number+h_number):
            if line > column: # Bottom left corner of matrix
                if is_part_of_ci(line, column) == False:
                    # THIS IS WHERE THINGS MUST HAPPEN
                    if amount_of_neighbors(line, matrix) == 8 or amount_of_neighbors(column, matrix) == 8:
                        matrix[line].append(0)
                    else:
                        blue_or_red = random.choice([0, 1])
                        matrix[line].append(blue_or_red)
                        neighbors_of_line = get_neighbors(line, matrix)
                        neighbors_of_column = get_neighbors(column, matrix)
                        if len(neighbors_of_line) > 1:
                            run_time_cis.append(neighbors_of_line)
                        if len(neighbors_of_column) > 1:
                            run_time_cis.append(neighbors_of_column)
                else:
                    matrix[line].append(0)
            else:
                matrix[line].append(0)

    return matrix

matrix = make_graph(20, 15)

print(str(matrix).replace("]", "]\n"))
file = open("matrix.txt", "w")
file.write(str(matrix).replace("]", "]\n"))
file.close()

# Making a graph out of the matrix (unrelated to how the matrix is generated)

G=nx.Graph()

for line in range(0, len(matrix)):
        for column in range(0, len(matrix[line])):
            if line > column: # Bottom left corner of matrix
                color = 0
                if matrix[line][column] != 0:
                    if matrix[line][column] == 1:
                        color = 'blue'
                    if matrix[line][column] == 2:
                        color = 'red'
                    if vertex_is_a_w(line) == True and vertex_is_a_w(column) == True:
                        G.add_edge("W" + str(line), "h" + str(column), color=color, weight=2)
                    elif vertex_is_a_w(line) == False and vertex_is_a_w(column) == False:
                        G.add_edge("h" + str(line), "h" + str(column), color=color, weight=2)
                    
                    elif vertex_is_a_w(line) == False and vertex_is_a_w(column) == True:
                        G.add_edge("h" + str(line), "W" + str(column), color=color, weight=2)
                    elif vertex_is_a_w(line) == True and vertex_is_a_w(column) == False:
                        G.add_edge("W" + str(line), "h" + str(column), color=color, weight=2)

vertex_color_map = []   

for node in G:
    node_name = str(node)
    if "W" in node_name:
        node_number = str(node_name).replace("W", "")
        if int(node_number) in vi_neighbors_list[0]:
            vertex_color_map.append('purple')
        if int(node_number) in vi_neighbors_list[1]:
            vertex_color_map.append('yellow')
        if int(node_number) in vi_neighbors_list[2]:
            vertex_color_map.append('orange')
        if int(node_number) in vi_neighbors_list[3]:
            vertex_color_map.append('limegreen')
    else:
        vertex_color_map.append('blue')

pos = nx.circular_layout(G)
edges = G.edges()
colors = [G[u][v]['color'] for u,v in edges]
weights = [G[u][v]['weight'] for u,v in edges]

# FINDING CI'S and stuff




nx.draw(G, pos, edge_color=colors, width=1, with_labels=True, node_color=vertex_color_map)
plt.show()
