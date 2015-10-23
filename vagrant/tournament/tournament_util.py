#!/usr/bin/env python
#
# Test cases for tournament.py

import math
import psycopg2

# see https://wiki.postgresql.org/wiki/Using_psycopg2_with_PostgreSQL
import psycopg2.extras
import sys

VERBOSE = False

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def query(qs, content=()):
    conn = connect()

    # see https://wiki.postgresql.org/wiki/Using_psycopg2_with_PostgreSQL
    c = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # c = conn.cursor()
    c.execute(qs+';', content)
    try:
        r = c.fetchall()
    except:
        r = None
    conn.commit()
    conn.close()
    return r

def get(table):
    r = query("select * from %s" % table)
    return r

def show(table):
    for row in query("select * from %s" % table):
        print row

def log(msg):
    print msg
    if VERBOSE:
        print 'Players:\n', show('players')
        print 'Matches:\n', show('matches')

def getPlayerID(name):
    r = query("select id from players where name = '%s')" % name) 

def getIDs():
    r = query("select id from players")
    return map(lambda x: x[0], r)

def resetDB():

    query('delete from matches *')
    query("alter sequence matches_match_seq restart with 1")

    query('delete from players *')
    query("alter sequence players_id_seq restart with 1")

def initPlayers(names):
    for name in names:
        query("insert into players values (default, %s)", (name,))

def initMatches():
    ids = getIDs()

    # first round
    i = 0
    while i < len(ids):
        winner = ids[i]
        loser = ids[i+1]
        query("insert into matches values (default, %s, %s)", (winner, loser))
        i += 2

    # second round
    i = 0
    while i < len(ids):
        winner = ids[i]
        loser = ids[i+2]
        query("insert into matches values (default, %s, %s)", (winner, loser))
        winner = ids[i+1]
        loser = ids[i+3]
        query("insert into matches values (default, %s, %s)", (winner, loser))
        i += 4

def count(table):
    return query("select count(*) from %s" % table)[0][0]

def roundsPlayed():
    return (2 * count('matches') / count('players'))

def roundsNecessary():
    return math.log(count('players'), 2)

def winners():
    r = query("select winner from winners order by wins")
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

q3 = '''
select id, name from (%s) as foo
'''

def standings():
    return query(q2 % (q1 % (roundsPlayed(), q0)))

def standings2():
    return query(q3 % q2 % (q1 % (roundsPlayed(), q0)))

def report(rows):
    hdr = " id | %16s | wins | matches "
    fmt = " %2s | %16s |  %2s  |    %2s   "
    line = "----+-%16s-+------+---------" % '----------------'
    print hdr % 'name'
    print line
    for row in rows:
        #print line
        print fmt % (row[0], row[1], row[2], row[3])
    print "(%d rows)" % len(rows)