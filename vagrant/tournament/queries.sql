
--  __init__()

   INSERT INTO tournaments 
   VALUES (DEFAULT, %s) 
   RETURNING ID;


-- report(table)

   SELECT * FROM %s 
   WHERE tournament = self.ID


-- playersWinning(n)

   SELECT id, name FROM standings 
   WHERE wins = %s AND tournament = %s

-- simulateTournament(names, display=True)

   SELECT MAX(wins) FROM results
   WHERE tournament = %s

   SELECT id, name FROM results 
   WHERE wins=%s AND tournament = %s

-- deleteMatches()

    DELETE FROM matches *
    WHERE tournament = %s

-- deletePlayers()

    DELETE FROM players_plus
    WHERE tournament = %s

    INSERT INTO players_plus 
    VALUES (0, %s, %s)

-- registerPlayer(name)

    INSERT INTO players_plus 
    VALUES (DEFAULT, %s, %s)

-- playerStandings()

    SELECT id, name, wins, matches FROM standings
    WHERE tournament = %s

-- reportMatch(winner, loser)

    INSERT INTO matches VALUES (%s, %s, %s)

-- rankPlayers()

    SELECT id, name FROM results
    WHERE tournament = %s

-- priorMatches(pair)

    SELECT winner, loser FROM matches
    WHERE ((winner=%(p1)s AND loser=%(p2)s)
    OR (winner=%(p2)s AND loser=%(p1)s))
    AND tournament = %(ID)s

-- swissPairings2()

    SELECT * FROM matches WHERE tournament = %s



-----------------------------------------------



    table tournaments
    table players
    table matches

    view wins
    view results
    view rounds_played
    view standings: results, rounds_played



    INSERT INTO tournaments 

    INSERT INTO players
    DELETE FROM players

    INSERT INTO matches
    DELETE FROM matches
    SELECT FROM matches

    SELECT * FROM %s 
    SELECT FROM results
    SELECT FROM standings 




