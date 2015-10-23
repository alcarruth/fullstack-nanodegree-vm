#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *
import math

def getPlayerID(name):
    r = query("select id from players where name = '%s')" % name) 

def getIDs():
    r = query("select id from players")
    return map(lambda x: x[0], r)

def resetDB():

    deleteMatches()
    query("alter sequence matches_match_seq restart with 1")

    deletePlayers()
    query("alter sequence players_id_seq restart with 1")

def initPlayers():

    registerPlayer("Markov Chaney")
    registerPlayer("Joe Malik")
    registerPlayer("Mao Tsu-hsi")
    registerPlayer("Atlanta Hope")

    registerPlayer("Twilight Sparkle")
    registerPlayer("Fluttershy")
    registerPlayer("Applejack")
    registerPlayer("Pinkie Pie")

    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")

    registerPlayer("Chandra Nalaar")
    registerPlayer("Melpomene Murray")
    registerPlayer("Randy Schwartz")
    registerPlayer("Udacious Ulysses")

def initMatches():
    ids = getIDs()
    # first round
    i = 0
    while i < len(ids):
        winner = ids[i]
        loser = ids[i+1]
        #print "reportMatch(%d,%d)" % (winner, loser)
        reportMatch(winner, loser)
        i += 2
    # second round
    i = 0
    while i < len(ids):
        winner = ids[i]
        loser = ids[i+2]
        #print "reportMatch(%d,%d)" % (winner, loser)
        reportMatch(winner, loser)
        winner = ids[i+1]
        loser = ids[i+3]
        #print "reportMatch(%d,%d)" % (winner, loser)
        reportMatch(winner, loser)
        i += 4

def standings():

    # select winner, count(*) as num from (
    r = query('''
    select winner from players left join matches
    on players.id = winner
    ''')
    # ) as results
    # group by winner
    # order by num desc
    print "\nstandings:"
    for row in r:
        print row

def count(table):
    return query("select count(*) from %s" % table)[0][0]

def roundsPlayed():
    return (2 * count('matches') / count('players'))

def roundsNecessary():
    return math.log(count('players'), 2)

def winners():
    r = query("select winner from winners order by wins")
    return map(lambda x: x[0], r)

def losers():
    r = query("select * from losers")
    return map(lambda x: x[0], r)

def pairs(xs):
    return [ (xs[i], xs[i+1]) for i in range(0, len(xs), 2)]        

q0 = '''
select winner, count(*) as wins 
from matches group by winner
'''
q1 = '''
select id, name, coalesce(wins,0) as wins, %d as matches
from players left join (%s) as foo on id = winner
'''

q2 = '''
select * from (%s) as foo order by wins desc
'''

def standings():
    return query(q2 % (q1 % (roundsPlayed(), q0)))

def report(rows):
    for row in rows:
        print row

if __name__ == '__main__':
    resetDB()
    initPlayers()
    initMatches()
    report(standings())

    
