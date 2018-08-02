
###########################################################

My program uses config.ini file. It should look like this:

[DB]
HOST = %your_host%
PORT = %your_port%
DATABASE = %your_db%
USER = %your_username%
PASSWORD = %your_password%

###########################################################

POST method expects json like this:

{
    "title": "The Godfather",
    "year": 1972,
	"country": "USA",
	"genre": "drama"
}

###########################################################

PUT method must be sent to an address like this "movies/7" (7 is movie's ID)
It expects json like this:

{
	"title": "The Godfather II",
    "year": 1974,
	"country": "USA"
}