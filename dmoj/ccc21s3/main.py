from sys import exit
from collections import defaultdict
az = 'abcdefghijklmnopqrstuvwxyz'
splii = lambda: map(int, input().split())
ii = lambda: int(input())
# --- Boilerplate ---

"""
strategy: construct a polynomial for each one, sum, and find minimum point of final function
insights:
each student can be represented by: n = max(0,|(c - p)| - d) * w
max() can be represented by: 0.5((x^2)^0.5 + x) or smthn?
abs() can be represented by: (x^2)^0.5
# https://www.desmos.com/calculator/w9kkjgk1wt
# becomes: 
# https://www.desmos.com/calculator/sapgpc0ek2
# becomes: 


son i just realized that sympy can differentiate max() and abs()

holy shit! does dmoj support it tho? im gonna try it out
nope, unfortunately I got  	IR (ModuleNotFoundError)


"""

from sympy import Symbol
x = Symbol('x', real=True)
y = x**2 + 1
yprime = y.diff(x)
print(yprime.subs(x, 5))

