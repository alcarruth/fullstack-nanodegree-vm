#!/usr/bin/python -i
# -*- coding: utf-8 -*-

import math

# Pascal's Triangle
#
def pascal(n):
    if n==0:
        return [1]
    else:
        prev = pascal(n-1)
        xs = map(lambda i: prev[i] + prev[i+1], range(len(prev)-1))
    return [1] + xs + [1]


# Pascal's Triangle - another way
#
def pascal2(row, col):
    if col == 0 or col == row:
        return 1
    else:
        return p2(row-1, col-1) + p2(row-1, col)



def tournament_groups(n):
    for k in range(n):
        m = 2**(k+1)
        print '\nTournament of %d:' % m
        groups(m)

def groups_row(n, r):
    # n = number of players
    # r = round, starting at 0
    p = pascal(r)
    s = 0
    for i in range(len(p)):
        s += p[i]
    return map (lambda x: n*x/s, p)
    
def groups(n):
    # n = number of players
    # prints normalized pascal triangle 
    r = 0
    g = groups_row(n, r)
    while g[0] > 1:
        print g
        r +=  1
        g = groups_row(n, r)
    print g
    

if __name__ == '__main__':
    tournament_groups(7)


