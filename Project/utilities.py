# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 20:22:36 2017

@author: The Computer
"""

def ConnectToDB(DBurl):
    #connect to MongoDB and throw error if unsuccessful
#    import datetime
    import pymongo
    import time
    import subprocess
    
    maxSevSelDelay = 1
    try:
        client = pymongo.MongoClient(DBurl, serverSelectionTimeoutMS=maxSevSelDelay)
        client.server_info()
        return client
    except pymongo.errors.ServerSelectionTimeoutError as err:
        # do whatever you need
        print('DB Connection Failure: ' + str(err) + '....')
        print('Opening new connection...')
        for numAttempts in range(1,6):
            print('Connection attempt number: ' + str(numAttempts) + '/5')
            try:
                print('Attempting to reconnect to database...')
                subprocess.run('"C:\\Program Files\\MongoDB\\Server\\3.4\\bin\\mongod.exe" --dbpath "C:\\Users\\The Computer\\Documents\\Mongodb\\data"',shell=True, timeout = 10)
            except subprocess.CalledProcessError as err:
                print('Error starting MongoDB: ' + str(err))
            
            try:
                time.sleep(5)
                client = pymongo.MongoClient(DBurl, serverSelectionTimeoutMS=maxSevSelDelay)
                client.server_info()
                print('New connection opened successfully on attempt number ' + str(numAttempts) + '/5')
                return client
            except pymongo.errors.ServerSelectionTimeoutError as err:
                print('DB Connection Failure after ' + str(numAttempts) + '/5' + ' attempts.  Check the server URL.')


def InitializeDB(client,dbname):
#    import pymongo
    db = client[dbname]
    return db


def ExtractHeadlines(DB,searchstring):
    #Extract Data from the database
    searchresult = []
    for scrape in DB.headlines.find():
        count = 0
        for collectedheadlines in scrape['headlines']:
            if searchstring in collectedheadlines:
                searchresult.append([scrape['headlines'][count], scrape['site'], scrape['scrapetime']])
            count = count + 1
    return searchresult