'''
This file contains my solution for the Einstein's riddle problem.

The code were written for the Operations Research course 
taught in the 2020 fall semester at the Budapest Corvinus University

Istvan Ladjanszki, istvan.ladjanszki@gmail.com

'''
import pulp
import numpy as np

import util

def oneTerm(attr, idx, rhs):
    return pulp.lpSum([(i + 1) * var[attr][i, idx - 1] for i in range(5)]) == rhs

def twoTerm(attr1, idx1, attr2, idx2, rhs):
    return pulp.lpSum([(i + 1) * var[attr1][i, idx1 - 1] for i in range(5)]) - pulp.lpSum([(i + 1) * var[attr2][i, idx2 - 1] for i in range(5)]) == rhs

# Attributes we create matrices for
attributes = ['Nationality', 'Color', 'Drink', 'Pet', 'Cigar']

# Creating the problem
problem = pulp.LpProblem('Einstein', pulp.LpMinimize)

# VARIABLES 
var = {}
for attr in attributes: 
    var[attr] = np.zeros((5, 5), dtype=pulp.LpVariable)
    for i in range(5):
        for j in range(5):
            varName = '_'.join([attr, str(i), str(j)])
            var[attr][i,j] = pulp.LpVariable(varName, 0, 1, cat = 'Integer')


# CONSTRAINTS
# One NATIONALITY to one house & One house to a NATIONALITY 
# One COLOR       to one house & One house to a COLOR 
# One DRINK       to one house & One house to a DRINK
# One PET         to one house & One house to a PET
# One CIGAR       to one house & One house to a CIGAR
for attr in attributes:
    for i in range(5): 
    
        const1 = []
        const2 = []
        for j in range(5):
            const1.append(var[attr][i, j])
            const2.append(var[attr][j, i])
    
        problem += pulp.lpSum(const1) == 1, '{0}_to_house_{1:d}_{2:d}'.format(attr, i, j)   
        problem += pulp.lpSum(const2) == 1, 'house_to_{0}_{1:d}_{2:d}'.format(attr, j, i) 

# Indexing conventions for the matrices
#  British = 1,    Dane = 2,   Norwegian = 3, German = 4, Swedish = 5.
#      red = 1,   green = 2,      yellow = 3,   blue = 4,   white = 5.
#      tea = 1,  coffee = 2,        beer = 3,  water = 4,    milk = 5.
#     bird = 1,   horse = 2,         dog = 3,    cat = 4,    fish = 5
#Pall Mall = 1, Dunhill = 2, Blue Master = 3,  Blend = 4,  Prince = 5.

dictionary = {
'Nationality' : ['British', 'Dane', 'Norwegian', 'German', 'Swedish'],
'Color' : ['red', 'green', 'yellow', 'blue', 'white'],
'Drink' : ['tea', 'coffee', 'beer', 'water', 'milk'],
'Pet' : ['bird', 'horse', 'dog', 'cat', 'fish'],
'Cigar' : ['Pall Mall', 'Dunhill', 'Blue Master', 'Blend', 'Prince'],
}

# Constraints given in the problem description

# Norvegian in the first house
#problem += pulp.lpSum([i * var['Nationality'][i, 2] for i in range(5)]) == 1
problem += oneTerm('Nationality', 3, 1)

# Person in the middle house drinks milk
#problem += pulp.lpSum([i * var['Drink'][i, 4] for i in range(5)]) == 1
problem += oneTerm('Drink', 5, 3)

# The person living in the yellow house smokes Dunhill.
#problem += pulp.lpSum([i * var['Color'][i, 2] for i in range(5)]) - pulp.lpSum([i * var['Cigar'][i, 1] for i in range(5)]) == 0
problem += twoTerm('Color', 3, 'Cigar', 2, 0)

# The person living in green house drinks coffee.
#problem += pulp.lpSum([i * var['Color'][i, 1] for i in range(5)]) - pulp.lpSum([i * var['Drink'][i, 1] for i in range(5)]) == 0
problem += twoTerm('Color', 2, 'Drink', 2, 0)

# The Dane drinks tea.
#problem += pulp.lpSum([i * var['Nationality'][i, 1] for i in range(5)]) - pulp.lpSum([i * var['Drink'][i, 0] for i in range(5)]) == 0
problem += twoTerm('Nationality', 2, 'Drink', 1, 0)

# The German smokes Prince.
#problem += pulp.lpSum([i * var['Nationality'][i, 3] for i in range(5)]) - pulp.lpSum([i * var['Cigar'][i, 4] for i in range(5)]) == 0
problem += twoTerm('Nationality', 4, 'Cigar', 5, 0)

# The Swede has a dog.
#problem += pulp.lpSum([i * var['Nationality'][i, 4] for i in range(5)]) - pulp.lpSum([i * var['Pet'][i, 2] for i in range(5)]) == 0
problem += twoTerm('Nationality', 5, 'Pet', 3, 0)

# The beer drinker smokes BlueMaster.
#problem += pulp.lpSum([i * var['Drink'][i, 2] for i in range(5)]) - pulp.lpSum([i * var['Cigar'][i, 2] for i in range(5)]) == 0
problem += twoTerm('Drink', 3, 'Cigar', 3, 0)

# The bird owner smokes Pall Mall.
#problem += pulp.lpSum([i * var['Pet'][i, 0] for i in range(5)]) - pulp.lpSum([i * var['Cigar'][i, 0] for i in range(5)]) == 0
problem += twoTerm('Pet', 1, 'Cigar', 1, 0)

# The green house is situated immediately to the left of the white house.
#problem += pulp.lpSum([i * var['Color'][i, 1] for i in range(5)]) - pulp.lpSum([i * var['Color'][i, 4] for i in range(5)]) == -1
problem += twoTerm('Color', 2, 'Color', 5, -1)

# The British person lives in the red house.
#problem += pulp.lpSum([i * var['Nationality'][i, 0] for i in range(5)]) - pulp.lpSum([i * var['Color'][i, 0] for i in range(5)]) == 0
problem += twoTerm('Nationality', 1, 'Color', 1, 0)
 
# OBJECTIVE FUNCTION
problem += 0, 'All solutions are equally good'

print(problem)

# Solve and print
problem.solve()

#print(problem.status)
print(pulp.LpStatus[problem.status])

# Print the results
for attr in attributes: 
    for i in range(5):
        for j in range(5):
            actVar = var[attr][i,j].varValue 
            if actVar == 1:
                print(attr + ' of house '  + str(i + 1) + ' is ' + dictionary[attr][j])
            
    print('')

 
  

 




