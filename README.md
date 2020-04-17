# Solve Einstein's riddle by linear programming
The content of this repository was implemented for a course taught in the 2020 spring semester at the Budapest Corvinus University.
The purpose of the code here is to show a method to solve Einstein's riddle by linear programming, using the Pulp library.

If you encounter this repository as a downloaded zip version the newest version can be found online at my GitHub page
```
https://github.com/ladjanszki/einstein_lp
```

## Dependencies
The code uses numpy and the frequently used Python linear programming package Pulp. It also uses pandas for presenting the solution of the riddle. 
The development and usage environment can be recreated by using conda package manager.
The repository contains the `environment.yml` file from which the development and testing environment can be rebuilt by invoking the following command
```
conda create -f environment.yml
```

## Usage and solution
The code can be invoked by the following commanfd from the linux command line. 

```
python einstein_lp.py
```

The output generated by the script answers the riddles question by the statement:
__The German owns the fish.__

## Uniqueness of the solution
The answer to the question is unique, in every optimal solution the German owns the fish. However not the whole table is unique. This can be tested in the code by the following setting. 
```Python
uniquenessTest = True
```
This adds some auxiliary constraints not present in the original problem. The table changes but still the German owns the fish.
 
