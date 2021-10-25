eight_ci = []
seven_ci = []
six_ci = []
five_ci = []
four_ci = []

for i in range(0, 30):
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

def is_part_of_ci(number1, number2): # do whole thing
    print("")

def make_graph(w_number, h_number):
    matrix = []
    for i in range(0, 35):
        matrix.append([])

    for line in range(0, 35):
        for column in range(0, 35):
            if line > column:
                matrix[line].append(1)
            else:
                matrix[line].append(0)

    return matrix
    
matrix = make_graph(20, 15)

print(str(matrix).replace("]", "]\n"))
