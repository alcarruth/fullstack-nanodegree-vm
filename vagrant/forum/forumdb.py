#
# Database access functions for the web forum.
# 

import time
import psycopg2

#  http://bleach.readthedocs.org/en/latest/
import bleach

BLEACH_INPUT = False
BLEACH_OUTPUT = True

## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''
    DB = psycopg2.connect("dbname=forum")
    c = DB.cursor()
    c.execute("SELECT time, content FROM posts ORDER BY time DESC")
    results = c.fetchall()
    DB.close()

    posts = []
    for row in results:
        post_content = str(row[1])
        post_time = str(row[0])
        if BLEACH_OUTPUT:

            # GOTCHA ALERT:
            # Without the .encode the server was spitting out
            # "AssertionError: write() argument must be string"
            # Looking at the source for wsgiref and searching for the
            # error I found that it was checking that the content was
            # 'StringType' and now it's not, it's 'Unicode' or
            # something.  So now we have the original string encoded
            # in web safe utf-8, and then coded back into ASCII.  It
            # seems like the wsgiref handler should just assert utf-8,
            # but what do I know?
            #
            post_content = bleach.clean(post_content).encode('utf-8')
            post_time = bleach.clean(post_time).encode('utf-8')
        posts.append({
            'content': post_content, 
            'time': post_time})

    # TODO: 
    # I re-arranged the original tuple-comprehension while trying
    # to debug the 'utf-8' issue.  I could probably put it back
    # like it was now.
    #
    return (p for p in posts)

## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    DB = psycopg2.connect("dbname=forum")
    c = DB.cursor()
    if BLEACH_INPUT: 
        content = bleach.clean(content)
        
    # use python tuple to prevent SQL injection attack
    # http://initd.org/psycopg/docs/usage.html
    query = "INSERT INTO posts (content) VALUES (%s)"
    content = (content,)

    c.execute(query, content)
    DB.commit()
    DB.close()


