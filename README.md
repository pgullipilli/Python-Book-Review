# Book Review for Existing Books in Database

## Pre requisites
1. Running postgres database
2. Good reads api key

## How to run the application

1. Create the config.ini file in the project1 directory which has to be look like this
```
; config.ini
[GOODREADS]
API_KEY = Your Good Reads API Key

[POSTGRES]
DATABASE_URL = postgres://USER_NAME:DB_PASSWORD@DB_HOST:DB_PORT/DB_NAME
```
2. Now create the required tables for this application by running the create.py file
`python create.py`
3. Now import the data of books by running import.py file
`python import.py`

once above steps done we can run our application.

For the flask application to run we need to set the environment variable FLASK_APP poiniting to application.py

I used powershell so in it we can set it as follows
`$env:FLASK_APP="application.py"`

once all set we can run our application by using the command `flask run`

## How application works

1. user need to register in order to write a review for a book
2. once registred you can log in to the application
3. once you logged into the application you landed on search page where you can search for a book
4. if the searched book exist in our database it shows the details of the book and form to fill the review
5. each user is allowed to write a review to the particular book only once so if you already write a review for the book searched you can not write review again you have only option to see your review for that book.
6. if you want to logout of the application you can use the logout button in search page


