
TODO: handle multiple tournaments.

 - add tournament_id field to the tables and views in
   tournament.sql.  I believe we can do this without
   breaking tournament.py - Is that right? 

 - add a tournament_id property in the Tournament class
   In the constructor, the tournament_id needs to be initialized
   and this needs to be done in concert with the database and 
   some serial id generation.  So, I think we need to add a
   tournament table to the db which has as primary key the
   tournament id.  The tournament_id fields in the other tables
   will reference tournament(id)

 - alter the query() method to include the proper reference to
   tournament_id.  Can we do this so that callers of query() don't
   have to reference the tournament_id?  Is it as simple as adding
   'where tournament_id = %s', self.tournament_id to the query
   string?  I think it might be ...  I'm aware of at least one 
   method that deals with psycopg2, without going through query().
   search tournament.py for 'c.execute' to find others.

How to proceed? 

 
