-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

create table players (
       id serial primary key,
       name text
       );

create table matches (
       match serial primary key,
       -- it seems the following three would suffice as primary key
       -- but for now I'm sticking with id.
       winner integer references players(id),
       loser integer references players(id)
       );
