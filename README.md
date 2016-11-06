# fullstack-p2-tournament-results
Udacity Fullstack Nanodegree Project 2
=======

# Fullstack P2 Tournament Results Project

## Quick Start

This quick start assumes that you have virtualbox and vagrant
installed on your machine.  There is nothing in the tournament code
that requires either virtualbox or vagrant so if you run linux and
have PostgreSQL installed you can probably run it anyway, at least I
did !-)

But for the virtual machine case, proceed as follows:

> `$ git clone git@github.com:alcarruth/fullstack-nanodegree-vm.git`
>
> `$ cd fullstack-nanodegree-vm/vagrant`
>
> `$ vagrant up`
>
> `$ vagrant ssh`

At this point you should be logged into the virtual machine
as user `vagrant`.  At the new vm prompt enter the following:

> `$ cd /vagrant/tournament`
>
> `$ psql -f tournament.sql

This will create the `tournament` database its tables and views.
Then you can run the following:

> `$ ./tournament_test.py`
>
> `$ ./tournament_demo.py`

## Description 

This project utilizes the PostgreSQL relational database software and
the python programming language to implement a Swiss Pairings style
tournament database. In addition to the functions specified by the
project assignment, other functionality is included to simulate a
tournament and to pretty print the standings after each round.  See
`tournament_demo.py` for more.

The pairing algorithm pairs players with an equal or almost equal
number of wins.  In the case of an odd number of players, a player
with the least number of wins is paired with a dummy player who always
loses.

The pairing algorithm is guaranteed not to pair players who have
previously played each other.  The algorithm proceeds by producing a
candidate pairing and checking that it includes no previously paired
players.  If it does, the list of players is randomly shuffled and
another candidate pairing is generated.  This is repeated until a
valid pairing is found.

Note that there is no guarantee that this shuffling will arrive at a
valid pairing.  I believe the probability of succes is high, however.
The ethernet protocol behaves in a similar way and it's inventor,
Robert Metcalfe is credited as saying the protocol "works in practice,
but not in theory".  So far, this pairing algorithm seems to work
pretty well "in practice".

## Directory Structure

All files for project P2 are contained within the `vagrant/tournament`
directory.  There is one SQL file:

 * `tournament.sql`

This is used to initialize the tournament database by creating the database,
tables and views used by the program. This can be done from the bash prompt:

> `$ psql -f tournament.sql

There are three tournament python files:

 * `tournament.py`
 * `tournament_test.py`
 * `tournament_demo.py`

The implementation of the tournament program is entirely in
`tournament.py` and `tournament.sql`.  The file `tournament_test.py`
contains the unit test that came with the assignment and the file
`tournament_demo.py` contains some code to run a 16 person tournament
simulation.

In thinking about this swiss pairing stuff I couldn't help but think
there was something familiar about the sizes of the groups when the 
players were grouped by their number of wins after each round.  It 
definitely reminded me of Pascal's triangle.  So I have here `pascal.py`
in which I tried to investigate this relationship.

Nothing much came of the `pascal.py` exercise.  It seemed to only be
applicable in the case where the number of players is a power of two.
That is, when there is a 'full bracket' of players.  But it was fun
none-the-less.
