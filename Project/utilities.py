"""
This file is for utilities used by the database scraper program.
The utilities include:
    ConnectToDB: Takes a databaseURL, creates the connection, and connects.
        Returns the database client
    InitializeDB: Initialize the DB connection object for pushing and pulling
        data.  Returns that object.
    ExtractHeadlines: Takes the DB connection object and the search string,
        searches the database for matching headlines.  Returns all matches
        along with metadata.
    """
import pymongo
import time
import subprocess


def ConnectToDB(DBurl):
    # connect to MongoDB and throw error if unsuccessful

    maxDelay = 1
    try:
        client = pymongo.MongoClient(DBurl,
                                     serverSelectionTimeoutMS=maxDelay)
        client.server_info()
        return client
    except pymongo.errors.ServerSelectionTimeoutError as err:
        # do whatever you need
        print('DB Connection Failure: ' + str(err) + '....')
        print('Opening new connection...')
        for numAttempts in range(1, 6):
            print('Connection attempt number: ' + str(numAttempts) + '/5')
            try:
                print('Attempting to reconnect to database...')
                subprocess.run('"C:\\Program Files\\MongoDB\\Server\\3.4\\bin\\mongod.exe" --dbpath "C:\\Users\\The Computer\\Documents\\Mongodb\\data"', shell=True, timeout=10) # noqa
            except subprocess.CalledProcessError as err:
                print('Error starting MongoDB: ' + str(err))

            try:
                time.sleep(.1)
                client = pymongo.MongoClient(DBurl,
                                             serverSelectionTimeoutMS=maxDelay)
                client.server_info()
                print('New connection opened successfully on attempt number ' +
                      str(numAttempts) + '/5')
                return client
            except pymongo.errors.ServerSelectionTimeoutError as err:
                print('DB Connection Failure after ' + str(numAttempts) + '/5'
                      + ' attempts.  Check the server URL.')


def InitializeDB(client, dbname):
    # import pymongo
    db = client[dbname]
    return db


def ExtractHeadlines(collection, searchstring):
    # Extract Data from the database
    searchresult = []
    for scrape in collection.find():
        count = 0
        for collectedheadlines in scrape['headlines']:
            if searchstring in collectedheadlines:
                searchresult.append([scrape['headlines'][count],
                                     scrape['site'], scrape['scrapetime']])
            count = count + 1
    return searchresult
