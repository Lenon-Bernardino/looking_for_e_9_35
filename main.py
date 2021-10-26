from inspect import GEN_CREATED
import random
import matplotlib
import networkx
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout

eight_ci = []
seven_ci = []
six_ci = []
five_ci = []
four_ci = []

w_five_ci1 = []
w_five_ci2 = []
w_five_ci3 = []
w_five_ci4 = []

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

def is_part_of_ci(number1, number2): # Check if two numbers are in an independent set
    ci_list = [eight_ci, seven_ci, six_ci, five_ci, four_ci, w_five_ci1, w_five_ci2, w_five_ci3, w_five_ci4]

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
    return False

def make_graph(w_number, h_number):
    matrix = []
    for i in range(0, w_number+h_number):
        matrix.append([])
    w_vertices = []


    for line in range(0, w_number+h_number):
        for column in range(0, w_number+h_number):
            if line > column: # Bottom left corner of matrix
                if is_part_of_ci(line, column) == False:
                    # THIS IS WHERE THINGS MUST HAPPEN

                    # GET SOME RANDOM VERTICES TO MAKE THE W'S

                    # THEN ESTABLISH ANOTHER 4 LISTS OF 5-CI'S

                    # ADD THEM TO THE LISTS AT THE TOP

                    # MAKE THE IS PART OF CI BS RECEIVE THEM

                    # WELL ACTUALLY, MAKE SURE TO MAKE THE NUMBER OF NEIGHBOS OF EACH VI CUSTOMIZABLE
                    # SO THAT THERE IS THE POSSIBILITY FOR MORE COMBINATIONS

                    # IK ITS HARD BUT JUST MAKE A LIST OF LISTS, IN WHICH THERE WILL BE THE LISTS OF W (NEIGHBORS OF VI)
                    # THEN MAKE A FOR LOOP THAT ADDS THEM TO THE CI LIST IN THE is_part_of_ci FUNCTION
                    blue_or_red = random.choice([1, 2])
                    matrix[line].append(blue_or_red)
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
                    G.add_edge(line, column, color=color, weight=2)

pos = nx.kamada_kawai_layout(G)
edges = G.edges()
colors = [G[u][v]['color'] for u,v in edges]
weights = [G[u][v]['weight'] for u,v in edges]

nx.draw(G, pos, edge_color=colors, width=1, with_labels=True)
plt.show()
