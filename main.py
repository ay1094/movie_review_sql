import database
from tabulate import tabulate

user_home_page = """
1) Create New User
"""
MAIN_MENU = """
1) Add a Review
2) View Reviews
3) Find/Filter Reviews
4) EXIT
"""

head = ["Title", "Type", "Genre", "Year", "Comments", "Rating"]
TYPES = ["Movie", "TV Show"]
GENRES = ["Comedy", "Documentary", "Drama", "Horror", "Action", "Mystery", "Animated", "Crime", "Science Fiction",
          "Fantasy"]

QUERY_HIGHEST_LOWEST = "Highest/Lowest Ratings"
FILTER_BY_TYPE = "Filter by Type"
FILTER_BY_GENRE = "Filter by Genre"
AVERAGE_RATING_BY_GENRE = "Average Rating by Genre"
AVERAGE_RATING_BY_TYPE = "Average Rating by Type"
DATE_RELEASED = "Date Released"
QUERY_BY_NAME = "Query by Name"
QUERY_OPTIONS = [QUERY_HIGHEST_LOWEST, FILTER_BY_TYPE, FILTER_BY_GENRE, AVERAGE_RATING_BY_GENRE, AVERAGE_RATING_BY_TYPE,
                 DATE_RELEASED, QUERY_BY_NAME]

def add_rating(connection):
    title = get_title()
    year = get_year()
    genre = get_cat(GENRES)
    type = get_cat(TYPES)
    comments = get_comments()
    rating = get_rating()
    database.insertIntoRatingsTable(connection, title, type, genre, year, rating, comments)


def get_cat(cat):
    while True:
        for i in range(len(cat)):
            print(str(i) + ") " + cat[i])
        res = 0
        try:
            res = int(input("Select From Above: "))
        except:
            print("Invalid input")
        if res < 0 or res >= len(cat):
            print("Invalid input")
        else:
            return cat[res]


def get_comments():
    return input("Enter Comments: ")


def get_title():
    title = ""
    while title == "":
        title = input("Enter title: ")
    return title


def get_year():
    year = 0.5
    while True:
        try:
            year = int(input("Enter Year: "))
            return year
        except:
            print("Invalid input")


def get_rating():
    rating = -1.0
    while True:
        rating = input("Enter rating (0-100): ")
        try:
            rating = float(rating)
            if 0 <= rating <= 100:
                return rating
            print("Must be a decimal number between 0 and 100")
        except:
            print("Invalid input")


def display_results(dataframe, headers):
    print(tabulate(dataframe, headers=headers, tablefmt="grid"))


def query_screen(connection):
    for i in range(len(QUERY_OPTIONS)):
        print(str(i) + ") " + QUERY_OPTIONS[i])
    while True:
        try:
            res = int(input("Enter Query Option"))
            option = QUERY_OPTIONS[res]
            print(option)
            #1st option
            if option == QUERY_HIGHEST_LOWEST:
                sortby = input("sort by (h)ighest/(l)owest")
                df = database.filter_ratings_by_review(connection, sortby)
                display_results(df, head)
                break
            #2nd option
            elif option == FILTER_BY_TYPE:
                res = get_cat(TYPES)
                df = database.simple_query_by_category(connection, "type", TYPES[res])
                display_results(df, head)
                break
            #3rd option
            elif option == FILTER_BY_GENRE:
                res = get_cat(GENRES)
                df = database.simple_query_by_category(connection, "genre", GENRES[res])
                display_results(df, head)
                break
            elif option == AVERAGE_RATING_BY_TYPE:
                df = database.groupbyratings(connection, 0)
                display_results(df, ['Type', 'Rating'])
                break
            elif option == AVERAGE_RATING_BY_GENRE:
                print("should print")
                df = database.groupbyratings(connection, 1)
                display_results(df, ['Genre', 'Rating'])
                break
            elif option == DATE_RELEASED:
                sortby = input("sort by (n)ewest/(o)ldest")
                df = database.date_released_query(connection, sortby)
                display_results(df, head)
                break

            elif option == QUERY_BY_NAME:
                res = input("Enter search string to query by: ")
                df = database.query_by_name(connection, res)
                display_results(df, head)
                break
            else:
                break
        except:
            print("Invalid input")


def initiate():
    connection = database.connect()
    database.createRatingsTable(connection)
    print("Welcome to Movie/TV Show Review Hub")
    while True:
        try:
            user_input = int(input(MAIN_MENU))
            if user_input == 1:
                add_rating(connection)
            elif user_input == 2:
                df = database.getRatings(connection)
                display_results(df, head)
            elif user_input == 3:
                query_screen(connection)
            else:
                break
        except:
            print("Invalid input")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    initiate()
    print("Thanks for visiting")
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
