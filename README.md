
###########################################################

My program uses config.ini file. It should look like this:

[DB]
HOST = %your_host%
DATABASE = %your_db%
USER = %your_username%
PASSWORD = %your_password%

###########################################################

POST method expects json like this:

{
    "name": "USA",
    "continent":"North America"
}

###########################################################

PUT method expects json like this:

{
    "id": "1",
	"name": "USA",
    "continent":"North America"
}