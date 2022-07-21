import sqlite3
CREATE_RATINGS_TABLE = """
CREATE TABLE if NOT EXISTS RATINGS (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, type TEXT, genre TEXT, year INT, comments TEXT, rating REAL);
"""

INSERT_INTO_RATINGS_TABLE = """
INSERT INTO RATINGS (name, type, genre, year, rating, comments) values (?,?,?,?,?,?);
"""

GET_ALL_RATINGS = """
SELECT * FROM RATINGS;
"""

DELETE_RATINGS = """
DROP TABLE RATINGS;
"""

GROUP_BY_GENRE = """
SELECT genre, AVG(RATING) FROM RATINGS GROUP BY genre;
"""

GROUP_BY_TYPE = """
SELECT type, AVG(RATING) FROM RATINGS GROUP BY type;
"""

DATE_RELEASED = """
SELECT * FROM RATINGS ORDER BY year
"""
QUERY_NAME = """
SELECT * FROM RATINGS WHERE name LIKE
"""

def query_by_name(connection, param):
    query_string = "'%" + param + "%'"
    query = QUERY_NAME + query_string
    with connection:
        return connection.execute(query).fetchall()



def groupbyratings(connection, category_integer):
    with connection:
        if category_integer == 0:
            return connection.execute(GROUP_BY_TYPE).fetchall()
        else:
            return connection.execute(GROUP_BY_GENRE).fetchall()

def simple_query_by_category(connection, cat, catname):
    return "SELECT * FROM RATINGS WHERE "+cat+"="+catname+" ORDER BY rating DESC;"

def group_by_cat(connection, cat):
    return "SELECT "+cat+", AVG(rating) FROM RATINGS GROUP BY " +cat +";"

def delete_table(connection):
    connection.execute(DELETE_RATINGS)

def ratings_by_review_string(order):
    if order == 'h':
        return "SELECT * FROM RATINGS ORDER BY rating DESC LIMIT 5"
    else:
        return "SELECT * FROM RATINGS ORDER BY rating ASC LIMIT 5"

def date_released_query(connection, query):
    qs = DATE_RELEASED
    if query == 'n':
        qs += " ASC;"
    else:
        qs+= " DESC;"

    with connection:
        return connection.execute(qs).fetchall()


def connect():
    return sqlite3.connect("ShowsMoviesReviews.db")

def createRatingsTable(connection):
    with connection:
        connection.execute(CREATE_RATINGS_TABLE)
        # print("done")

def insertIntoRatingsTable(connection, name, type, genre, year, rating, comments):
    with connection:
         connection.execute(INSERT_INTO_RATINGS_TABLE, (name, type, genre, year, rating, comments))

def getRatings(connection):
    with connection:
        print("in get ratings")
        return connection.execute(GET_ALL_RATINGS).fetchall()

def filter_ratings_by_review(connection, order):
    with connection:
        return connection.execute(ratings_by_review_string(order)).fetchall()