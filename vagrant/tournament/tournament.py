#!/usr/bin/python -i
# -*- coding: utf-8 -*-

# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

# We use random to shuffle the decks in method swissPairings()
# and to flip a coin in simulateRound().
import random

# The python module 'prettytable' enables pretty printing of tables.
# We use it in the report() method below.  It was installed already
# in the udacity vagrant image, but if not already installed in 
# your ubuntu, it can be with:
#
#    sudo apt-get install python-prettytable
#
import prettytable

class Tournament:

    def __init__(self, names=[], display=False, pairing_algorithm=2):
        """Create a new instance of the Tournament class.
        
        Args:
            names: list of players to be initally registered
            display: boolean to print a pretty table of initial standings
            pairing_algorithm: algorithm for pairing, 1 or 2
        """
        self.dbname="tournament" 
        self.initDB(names, display)
        self.pairingAttempts = 0
        self.pairing_algorithm = pairing_algorithm

    def initDB(self, names, display=False):
        """Initialize the database to include only players in names and no matches.

        Args:
            names: list of players to be initally registered
            display: boolean to print a pretty table of initial standings
        """
        self.deleteMatches()
        self.deletePlayers()
        for name in names:
            self.registerPlayer(name)
        if display:
            self.show('standings')

    def connect(self):
        """Connect to the PostgreSQL database.  Returns a database connection."""
        return psycopg2.connect("dbname=" + self.dbname)

    def query(self, qs, content=()):
        """Open a connection to the PostgreSQL database, obtain a cursor,
        execute the query specified by the querystring qs, commit the transaction and 
        close the connection.  Returns the value returned by fetchall() or 'None'.

        Args:
            qs: a query string containing %s placeholders. Note: no semi-colon !
            content: a tuple of strings to fill placeholders in qs
        """
        # Argument 'content' must be of type tuple to guard against SQL injection attacts.
        # We don't handle any exceptions raised.  (The way to 'handle' it is for me to
        # edit the culprit below to tuple-fy it.)
        # Well, it turns out that it doesn't _have_ to be a tuple, it can be a list.
        ctype = type(content)
        assert ctype == tuple or ctype == list

        conn = self.connect()
        c = conn.cursor()

        # Note that we add a semi-colon here so it must not be included in
        # the qs argument.  I have a reason for doing this, but I don't think
        # it's worth attempting an explanation here !-)
        c.execute(qs+';', content)

        # Not all queries produce something to fetch.  If this one does,
        # fetch it and return it.  If it does not, we return 'None'.
        try:
            r = c.fetchall()
        except:
            r = None

        # But before we can return, we finish with the database.  Again,
        # not all interactions with the database require a commit, but we
        # don't do any harm and I don't think we lose too much by executing
        # the commit() anyway.  We waste a function call but I'm sure
        # for PostgreSQL it's a no-op.
        conn.commit()
        conn.close()
        return r

    def report(self, table):
        """Generate a prettytable object for table."""

        # Here we don't use the query() method above because prettytable has a 
        # that will create the pretty string directly from the database cursor.
        conn = self.connect()
        c = conn.cursor()

        # Regarding psycopg2's cursor.execute() method we have from
        # http://initd.org/psycopg/docs/usage.html#query-parameters:
        # 
        # "Only variable values should be bound via this method: it
        # shouldn’t be used to set table or field names. For these
        # elements, ordinary string formatting should be used before
        # running execute()."

        # grab the whole table
        c.execute("select * from %s;" % table)

        # produce the prettyprint object
        x = prettytable.from_db_cursor(c)
        conn.close()

        # Now we can set some options.  If they don't apply
        # to the current table it's no big deal.
        x.align['name'] = 'l'
        x.align['winner'] = 'l'
        x.align['loser'] = 'l'
        x.align['id'] = 'r'
        return x

    def show(self, table):
        """Print the prettyprint object returned by report()."""
        print '\n' + table + ':'
        print self.report(table)

    def playersWinning(self, n):
        """Consult the database to return the number of players who have won n games.

        Args:
            n: number of wins by which to select players
        """
        xs = self.query("select id, name from standings where wins = %s", (n,))
        return xs

    def groupPlayers(self):
        """Return a list of lists of players.  This is a partitioning of the players
        into groups of players having the same number of wins.  The list is sorted
        by wins descending.  That is, the first group in the list contains the players
        with the most wins and the last group contains the players with zero wins.
        """

        # TODO:
        # I suspect this can be done in a single db query, but I don't know how 
        # to do this yet.  I noticed in the docs that PostgreSQL allows programmers
        # (I mean 'database administrators' !-) to define their own aggregate functions.
        # Surely with one sweep of the table you could produce the required partitioning.

        n = 0
        groups = []
        group = self.playersWinning(n)

        # TODO: (moot if above TODO is done)
        # I'm relying on a conjecture that there are no 'holes' in the partitioning.
        # That is, if some player has n wins then for all m such that 0 <= m < n 
        # some player has m wins.  Otherwise the following loop would terminate
        # pre-maturely upon encountering the 'hole'.  Another way would be to stop
        # when the sum of the lengths of the groups equals the total number of players.

        while group != []:
            groups.append(group)
            n += 1
            group = self.playersWinning(n)
        return groups

    def simulateRound(self, display=False):
        """Simulate a round of match play.  Players are swiss paired, a winner
        is randomly selected for each pair and the outcome is entered into the
        database using reportMatch().

        Args:
            display: pretty print standings if True
        """
        for pair in self.swissPairings():

            # TODO:
            # add log() method and a verbosity property which can be
            # adjusted to the user's preference.

            # print pair

            # If the id of the second player is 0, then it is a bye so we
            # give the first player the win.  Otherwise we flip a coin.
            # Remember: a pair has the form (id_1, name_1, id_2, name_2).
            #
            if pair[3] == 0:
                self.reportMatch(pair[0], 0)
            else:
                ids = [pair[0], pair[2]]
                random.shuffle(ids)
                self.reportMatch(ids[0], ids[1])

        # Ain't it beautiful?
        if display:
            self.show('standings')

    def simulateTournament(self, names, display=True):
        """Simulate a complete tournament.  We initialize the database and then
        simulate a round of matches, by calling simulateRound(), until the group
        of players with the most wins contains just a single player.

        Args:
            names: the list of players for the tournament.
            display: show standings initially and after each round.
        """
        self.initDB(names, display)
        done = False

        # count these for an idea how well our randomized re-attempt approach
        # to the swiss pairing algorithm is working.
        self.pairingAttempts = 0

        while not done:
            self.simulateRound(display)

            # TODO: 
            # Shouldn't max_wins be the same as the number of rounds played?
            # We could have a 'round_number' variable initialized to zero
            # and incremented each time through the loop.  (Making the change
            # should be easier than writing this comment !-)

            # maximum number of wins for any player (so far)
            max_wins = self.query('select max(wins) from results')[0][0]

            # TODO:
            # leaders is the same as the first group in the list returned
            # by groupPlayers() which currently executes a number of queries
            # to the database.  But a TODO item in groupPlayers() suggests
            # that it possibly could be done in just one query.  If that
            # is implemented then we'd have no reason for max_wins or to
            # make this query here.

            # group of players with the maximum number of wins so far
            leaders = self.query("select id, name from results where wins=%s", (max_wins,))

            done = len(leaders) == 1

        print "We have a winner!"
        print "Congratulations to %s" % leaders[0][1]
        print "Total pairing attempts = %d" % self.pairingAttempts

    def deleteMatches(self):
        """Remove all the match records from the database."""
        self.query('delete from matches *')

    def deletePlayers(self):
        """Remove all the player records from the database."""

        # reset this tournament's internal count.
        self.numberPlayers = 0

        # delete all players from the database
        self.query('delete from players_plus *')

        # but then add back the dummy 'bye' player with id 0
        self.query("insert into players_plus values (0, %s)", ('_',))

        # reset the serial generator for id to 1
        self.query("alter sequence players_plus_id_seq restart with 1")

    def countPlayers(self):
        """Returns the number of players currently registered."""
        # I know this is supposed to execute the query which is 
        # commented out below but it just didn't seem to make sense 
        # since the answer is already at hand.
        return self.numberPlayers
        # return self.query('select count(*) from players')[0][0]

    def registerPlayer(self,name):
        """Adds a player to the tournament database.

        The database assigns a unique serial id number for the player.  (This
        should be handled by your SQL database schema, not in your Python code.)

        Args:
            name: the player's full name (need not be unique).
        """
        self.numberPlayers += 1
        self.query("insert into players_plus values (default, %s)", (name,))

    def playerStandings(self):
        """Returns a list of the players and their win records, sorted by wins.

        The first entry in the list should be the player in first place, or a player
        tied for first place if there is currently a tie.

        Returns:
        A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
        """
        return self.query('select * from standings')

    def reportMatch(self, winner, loser):
        """Records the outcome of a single match between two players.

        Args:
            winner:  the id number of the player who won
            loser:  the id number of the player who lost
        """
        # TODO:
        # implement logging() method and use that.
        #print "winner: %s, loser: %s" % (winner, loser)
        self.query("insert into matches values (%s, %s)", (winner, loser))
 
    def rankPlayers(self):
        """Returns a list of all players, sorted by the number of matches
        they have won in descending order.  If the number of players is odd
        we even it out by adding the bye dummy.
        """

        # Note: rankPlayers() is used by swissPairings1() but not by
        # swissPairings2().

        xs = self.query('select id, name from results')
        #xs = self.query('select id, name from results order by wins desc')
        # add a dummy bye player if number of players is odd
        # (that's different than saying 'number of odd players' !-)
        if self.numberPlayers % 2:
            xs.append((0, '_'))
        return xs

    def priorMatches(self, pair):
        """Returns a list of prior matches for a pair of players

        Args:
            pair: a pair of players as a tuple (id_1, name_1, id_2, name_2)
        """
        # Note: rankPlayers() is used by swissPairings1() but not by
        # swissPairings2().  It is an inefficient way to go and should
        # be done away with.

        # the id's for the two players
        p1 = pair[0]
        p2 = pair[2]

        return self.query("""
        select winner, loser from matches
        where winner=%s and loser=%s
        or winner=%s and loser=%s
        """, (p1, p2, p2, p1))

    def swissPairings(self):
        if self.pairing_algorithm == 1:
            return self.swissPairings1()
        else:
            # There's not much point in crapping out on a
            # bad value here.  If it's not 1 use 2.
            return self.swissPairings2()

    def swissPairings1(self):
        """Returns a list of pairs of players for the next round of a match.

        Assuming that there are an even number of players registered, each player
        appears exactly once in the pairings.  Each player is paired with another
        player with an equal or nearly-equal win record, that is, a player adjacent
        to him or her in the standings.

        Returns:
            A list of tuples, each of which contains (id1, name1, id2, name2)
            id1: the first player's unique id
            name1: the first player's name
            id2: the second player's unique id
            name2: the second player's name
        """
        success = False
        limit = 100
        i = 0

        while i < limit and not success:
            xs = self.rankPlayers()

            # Construct a pairing in the simplest way possible, given that
            # the length of xs is even.  This is ensured by rankPlayers().
            pairs = [ tuple(xs[j] + xs[j+1]) for j in range(0, len(xs), 2)]

            # Pairing is successful if no two paired players have played before
            success = all(map(lambda x: not tournament.priorMatches(x), pairs))

            # TODO:
            # The above line is really slow since it does a separate query 
            # (via priorMatches()) for each pair in the list.
            # Figure out how to do this in one query by constructing a where
            # clause from the candidate pairing.  I know SQL offers sets and
            # arrays.  Do that and test for membership or something !-)

            i += 1
        self.pairingAttempts += i
        #print "pairing attempts = %d" % i
        return pairs

    def swissPairings2(self):
        """Returns a list of pairs of players for the next round of a match.

        Assuming that there are an even number of players registered, each player
        appears exactly once in the pairings.  Each player is paired with another
        player with an equal or nearly-equal win record, that is, a player adjacent
        to him or her in the standings.

        Returns:
            A list of tuples, each of which contains (id1, name1, id2, name2)
            id1: the first player's unique id
            name1: the first player's name
            id2: the second player's unique id
            name2: the second player's name
        """

        # groups is a list of lists, where each sublist contains the (id, name)
        # pair for players who have all won the same number of games.
        groups = self.groupPlayers()

        # We use a python dictionary to implement a set of all matches played.
        # The set is symmetric in that ((a,b) in d)  iff  ((b,a) in d).

        d = {}
        for x in self.query('select * from matches'):
            d[x] = True
            d[(x[1],x[0])] = True

        success = False

        # Seems like we should have some limit on the number of tries before
        # we give up.  Not that we give up gracefully.  What happens if we
        # reach the limit is that we just try to reportMatch() a pair of players
        # who have already played each other.  This will be rejected by 
        # postgresql/psycopg2 since (winner, loser) is a primary key for matches.

        limit = 200
        i = 0

        while i < limit and not success:

            # shuffle each n-win group
            map(random.shuffle, groups)

            # Join the groups together into one list of players.
            # This list is sorted by wins desc.
            xs = reduce(lambda x,y: x+y, groups)

            # even up the list if necessary
            if self.numberPlayers % 2:
                xs.append((0, '_'))

            # get a candidate pairing
            pairs = [ tuple(xs[j] + xs[j+1]) for j in range(0, len(xs), 2)]

            # The pairing is successful if no two paired players have played before.
            # Here in swissPairngs2() we use our set d to check for prior meetings.
            success = all(map(lambda x: (x[0],x[2]) not in d, pairs))
            i += 1

        # Update the total number of pairing attempts for the tournament.
        self.pairingAttempts += i

        # Log the number of attempts for this call to swissPairings2()
        # print "pairing attempts = %d" % i

        return pairs

# The P2 specification doesn't know anything about our object-oriented
# design and it expects module level function definitions.
#
# We simulate that here by creating a tournament instance and setting
# the function names required for the P2 specification to their
# respective methods in our tournament instance.

# Also, the Tournament class provides two versions of swissPairings() 
# which we can specify with the optional 'pairing_algorithm' argument
# to the Tournament constructor.  The default is 2.

tournament = Tournament() # default

#tournament = Tournament(pairing_algorithm=1)
#tournament = Tournament(pairing_algorithm=2)

deleteMatches = tournament.deleteMatches
deletePlayers = tournament.deletePlayers
countPlayers = tournament.countPlayers
registerPlayer = tournament.registerPlayer
playerStandings = tournament.playerStandings
reportMatch = tournament.reportMatch
swissPairings = tournament.swissPairings


if __name__ == '__main__':
    from tournament_demo import *
