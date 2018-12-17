#Book Review for Existing Books in Database

**Pre requisites**
1. running postgres database
2. good reads api key

**How to run the application**

1. create the config.ini file in the project1 directory which has to be look like this

`; config.ini
[GOODREADS]
API_KEY = Your Good Reads API Key

[POSTGRES]
DATABASE_URL = postgres://USER_NAME:DB_PASSWORD@DB_HOST:DB_PORT/DB_NAME`

2. Now create the required tables for this application by running the create.py file
3. Now import the data of books by running import.py file

once above steps done we can run our application.

For the flask application to run we need to set the environment variable FLASK_APP poiniting to application.py

once all set we can run our application by using the command `flask run`


