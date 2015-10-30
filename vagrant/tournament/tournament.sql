-- Table definitions for the tournament project.


create table tournaments (
       id serial primary key,
       name text
       );


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
create table players_plus (
       id serial,
       name text,
       tournament integer references tournaments(id),
       primary key (id, tournament)
       );


-- table 'matches'
--
-- Table 'matches' contains the outcomes of the matches played.
-- Since (winner, loser) is the primary key, rematches are 
-- automatically rejected by the database.
--
create table matches (
       winner integer,
       loser integer,
       tournament integer references tournaments(id),
       foreign key (winner, tournament) references players_plus(id, tournament),
       foreign key (loser, tournament) references players_plus(id, tournament),
       primary key (winner, loser, tournament)
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
create view players as
       -- * includes tournament
       select * from players_plus where id>0;


-- view 'wins'
--
-- View 'wins' returns a table of players with their id and 
-- their number of wins BUT only for players with at least one win.
--
-- It's probably only used by the view 'results' below and, if that's
-- the case, the 'order by' clause is superfluous since 'results'
-- does its own ordering.
--
create view wins as
       select tournament, winner as id, count(*) as wins 
       from matches group by tournament, winner
       order by wins desc;


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
create view results as
       select players.tournament, players.id, name, coalesce(wins,0) as wins
       from players left join wins 
       on players.tournament = wins.tournament
       and players.id = wins.id
       order by wins desc, random();


-- view 'rounds_played'
--
-- Returns a single row with a single field which contains
-- the number of rounds played in the tournament so far.
-- As far as I know this is only used to provide the 'matches'
-- field in the 'standings' view (see below).
--
create view rounds_played as
       select tournament, coalesce(max(wins),0) as matches 
       from wins
       group by tournament;


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
create view standings as
       select results.tournament, id, name, wins, coalesce(matches, 0) as matches
       from results left join rounds_played
       on results.tournament = rounds_played.tournament;
