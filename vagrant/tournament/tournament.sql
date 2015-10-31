-- tournament.sql

-- Author: Al Carruth
-- Submitted for the Udacity Fullstack Developer Nanodegree
-- Project 2: Tournament Results

-- Start with a brand new database
--
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament


-- table 'tournaments'
--
-- Table tournaments is included to enable the multiple tournament
-- capability.  The methods of the Tournament class in tournament.py
-- need to qualify their non-multi queries to include 
-- 'WHERE tournament = %s' % self.id 
-- (or something similar) to eliminate rows belonging to other
-- tournaments.  I'd like to make this transparent to the python
-- tournament instance so that the methods could 'pretend' they
-- own the database.
--
CREATE TABLE tournaments (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
    );


-- table 'players'
--
-- This table contains all the players plus an additional dummy player
-- who is guaranteed to lose every match he plays.  This additional
-- player has id = 0 and whatever name given it in tournament.py.
--
CREATE TABLE players (
    id SERIAL,
    name TEXT NOT NULL,
    tournament INTEGER REFERENCES tournaments(id),
    PRIMARY KEY (id, tournament)
    );


-- table 'matches'
--
-- Table 'matches' contains the outcomes of the matches played.  Since
-- (winner, loser) is the primary key, rematches are automatically
-- rejected by the database.
--
CREATE TABLE matches (
    winner INTEGER,
    loser INTEGER,
    tournament INTEGER REFERENCES tournaments(id),
    FOREIGN KEY (winner, tournament) 
         REFERENCES players(id, tournament) ON DELETE CASCADE,
    FOREIGN KEY (loser, tournament) 
         REFERENCES players(id, tournament) ON DELETE CASCADE,
    PRIMARY KEY (winner, loser, tournament),
    CHECK (winner <> loser)
    );


-- view 'wins'
--
-- View 'wins' returns a table of players with their id and their
-- number of wins BUT only for players with at least one win.
--
CREATE VIEW wins AS
    SELECT tournament, winner AS id, COUNT(*) AS wins 
    FROM matches GROUP BY tournament, winner;


-- view 'results'
--
-- View 'results' provides the first three columns of the 'standings'
-- view, without the 'matches' column.  This view does most of the
-- heavy lifting (for a PostgreSQL novice, anyway).

-- The left join ensures that players without a win are included, but
-- only with a value of 'null' for their 'wins' column.  The
-- 'coalesce(wins, 0) as wins' replaces the nulls with 0s.  (Thank you
-- stackoverflow.com !!)
--
CREATE VIEW results AS
    SELECT players.tournament, players.id, name, COALESCE(wins,0) AS wins
    FROM players LEFT JOIN wins
    ON players.tournament = wins.tournament
    AND players.id = wins.id
    WHERE players.id > 0
    ORDER BY wins DESC;


-- view 'rounds_played'
--
-- Returns a single row with a single field which contains
-- the number of rounds played in the tournament so far.
-- As far as I know this is only used to provide the 'matches'
-- field in the 'standings' view (see below).
--
CREATE VIEW rounds_played AS
    SELECT tournament, COALESCE(MAX(wins),0) AS matches 
    FROM wins GROUP BY tournament;


-- view 'standings'
--
-- Provides a view suitable for use in the playerStandings() method as
-- specified by the P2 assignment.  The final field 'matches' is the
-- total number of matches played and is the same for all players.
--
-- TODO: whoops!! I just realized that by assuming 'matches' is the
-- same for all players that means standings should not be viewed
-- except _between_ rounds.  Is that a problem?  I don't know but I
-- don't like it.
--
CREATE VIEW standings AS
    SELECT results.tournament, id, name, wins, COALESCE(matches, 0) AS matches
    FROM results LEFT JOIN rounds_played
    ON results.tournament = rounds_played.tournament;
