-- tournament_reset.sql

-- Include this file from the psql command line to drop all the old
-- table and view definitions before you create new ones by including
-- the tournament.sql file. For example:

-- tournament=> \i tournament_reset.sql
-- [...]
-- tournament=> \i tournament.sql
-- [...]

drop table tournaments cascade;
drop table matches cascade;
drop table players_plus cascade;
