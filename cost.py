#!/bin/python3
import math
def solve(meal_cost, tip_percent, tax_percent):
    tip = float(tip_percent/100)
    tax = float(tax_percent/100)
    cost = meal_cost * (1 + tip + tax)
    return cost

meal_cost = float(input())
tip_percent = int(input())
tax_percent = int(input())

total_cost = solve (meal_cost, tip_percent, tax_percent)
cost = math.floor(total_cost)
print('The total meal cost is ', end='')
print(cost, end='')
print(' dollars.')