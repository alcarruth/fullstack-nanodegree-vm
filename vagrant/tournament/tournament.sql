-- Table definitions for the tournament project.

-- We start with a clean slate
--
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament


-- table 'players_plus'
--
-- This table is called 'players_plus' because it is contains
-- all the players _plus_ a dummy player who is a 'born loser'
-- and loses every match he plays.  This additional player has
-- id = 0 and whatever name that given it in tournament.py.
--
-- All modifications to the roster should be made directly to this
-- this table.  At this time, I believe only the registerPlayer() and
-- deletePlayers() methods modify players_plus.
--
-- In order to read from the roster of players one should select from
-- the view 'players' (see below).
--
CREATE TABLE players_plus (
       id SERIAL PRIMARY KEY,
       name TEXT NOT NULL
       );


-- table 'matches'
--
-- Table 'matches' contains the outcomes of the matches played.
-- Since (winner, loser) is the primary key, rematches are 
-- automatically rejected by the database.
--
CREATE TABLE matches (
       winner INTEGER REFERENCES players_plus(id) ON DELETE CASCADE,
       loser INTEGER REFERENCES players_plus(id) ON DELETE CASCADE,
       PRIMARY KEY (winner, loser),
       CHECK (winner <> loser)
       );


-- view 'players'
--
-- View 'players' presents a view of players_plus without the
-- dummy bye loser player.  In a sense this is the real roster
-- of players.
-- 
-- Initially we did not have this view and 'players' was a table with
-- no dummy bye loser player.  The problem was that when the loser lost
-- and the match was reported it was rejected because matches(loser)
-- referenced players(id) and there was no player registered with dummy 
-- born loser's id.
--
CREATE VIEW players AS
       SELECT * FROM players_plus WHERE id>0;


-- view 'wins'
--
-- View 'wins' returns a table of players with their id and 
-- their number of wins BUT only for players with at least one win.
--
-- It's probably only used by the view 'results' below and, if that's
-- the case, the 'order by' clause is superfluous since 'results'
-- does its own ordering.
--
CREATE VIEW wins AS
       SELECT winner AS id, COUNT(*) AS wins 
       FROM matches GROUP BY winner
       ORDER BY wins DESC;


-- view 'results'
--
-- View 'results' provides the first three columns of the 
-- 'standings' view, without the 'matches' column.  This
-- view does most of the heavy lifting (for a PostgreSQL
-- novice, anyway).

-- The left join ensures that players without a win are included,
-- but only with a value of 'null' for their 'wins' column.
--
-- The 'coalesce(wins, 0) as wins' replaces the nulls with 0s.
-- (Thank you stackoverflow.com !!)
--
-- In 'order by wins desc, random()' the 'random()' was added 
-- to shuffle the players within a group and is relied upon
-- by the swissPairings1() method to find a pairing with no
-- rematches.  So repeated queries referencing this view will
-- likely produce different orderings of the players.
--
-- The swissPairings2() method does the shuffling in python
-- and does not rely on this randomness here.
--
CREATE VIEW results AS
       SELECT players.id, name, COALESCE(wins,0) AS wins
       FROM players LEFT JOIN wins ON players.id = wins.id
       ORDER BY wins DESC, random();


-- view 'rounds_played'
--
-- Returns a single row with a single field which contains
-- the number of rounds played in the tournament so far.
-- As far as I know this is only used to provide the 'matches'
-- field in the 'standings' view (see below).
--
CREATE VIEW rounds_played AS
       SELECT COALESCE(MAX(wins),0) AS matches FROM wins;


-- view 'standings'
--
-- Provides a view suitable for use in the playerStandings()
-- method as specified by the P2 assignment.  The final field
-- 'matches' is the total number of matches played and is the
-- same for all players.
--
-- TODO: whoops!! I just realized that by assuming 'matches'
-- is the same for all players that means standings should
-- not be viewed except _between_ rounds.  Is that a problem?
-- I don't know but I don't like it.
--
CREATE VIEW standings AS
       SELECT id, name, wins, matches 
       FROM results, rounds_played;
