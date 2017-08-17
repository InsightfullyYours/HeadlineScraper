# This file performs unit testing on the program
from ..Project.mainquery import mainquery
from ..Project.scrapers import WebScrapers
from ..Project.scrapedata import scrapedata
from ..Project.utilities import ConnectToDB, InitializeDB, ExtractHeadlines
import pytest
from bs4 import BeautifulSoup
from urllib.error import URLError
import datetime
import pymongo
import bson
import pandas


def test_webscraper_class():
    # Test initialization
    assert isinstance(WebScrapers('http://www.nytimes.com'), WebScrapers)
    assert isinstance(WebScrapers('x'), WebScrapers)

    # Test OpenWebsite()
    nytimes = WebScrapers('http://www.nytimes.com')
    assert isinstance(nytimes, WebScrapers)
    assert isinstance(nytimes.OpenWebsite(), BeautifulSoup)
    assert str(nytimes.OpenWebsite())[0:15] == '<!DOCTYPE html>'

    with pytest.raises(UnboundLocalError) as err:
        assert WebScrapers('m').OpenWebsite() in str(err)

    with pytest.raises(URLError) as err:
        assert WebScrapers('http:/nyimes.com').OpenWebsite() in str(err)


def test_parsers():
    # Test the website parsers
    nytimes = WebScrapers('http://www.nytimes.com')
    data = nytimes.OpenWebsite()

    assert isinstance(nytimes, WebScrapers)
    assert isinstance(data, BeautifulSoup)
    assert isinstance(nytimes.NYTParse(data), dict)
    assert isinstance(nytimes.NYTParse(data).get('headlines'), list)
    assert isinstance(nytimes.NYTParse(data).get('site'), str)
    assert isinstance(nytimes.NYTParse(data).get('scrapetime'),
                      datetime.datetime)

    foxnews = WebScrapers('http://www.foxnews.com')
    data = foxnews.OpenWebsite()

    assert isinstance(foxnews, WebScrapers)
    assert isinstance(data, BeautifulSoup)
    assert isinstance(foxnews.FOXParse(data), dict)
    assert isinstance(foxnews.FOXParse(data).get('headlines'), list)
    assert isinstance(foxnews.FOXParse(data).get('site'), str)
    assert isinstance(foxnews.FOXParse(data).get('scrapetime'),
                      datetime.datetime)


def test_database():
    # Test all the database interaction utilities

    DBurl = 'mongodb://localhost:27017/'
    client = ConnectToDB(DBurl)
    DBname = 'NewsHeadlines'
    DB = InitializeDB(client, DBname)

    # Test connection to non-existant database
    DBurl = 'Not a database'
    assert ConnectToDB(DBurl) is None
    with pytest.raises(TypeError) as err:
        assert InitializeDB(ConnectToDB(DBurl), 'Arbitrary') in str(err)

    # Test connection to actual database
    DBurl = 'mongodb://localhost:27017/'
    client = ConnectToDB(DBurl)
    DBtable = DB.headlines
    assert isinstance(client, pymongo.mongo_client.MongoClient)
    assert isinstance(DBtable.find_one().get('headlines'), list)

    # Connect to a non-existant table
    DBname = 'NewDatabase'
    DB = InitializeDB(client, DBname)
    DBtable = DB.test
    assert isinstance(DB, pymongo.database.Database)

    # insert data
    poll_id = DBtable.insert_one({'headlines': ['this is a test',
                                                'this is a test2'],
                                  'site': 'testsite',
                                  'scrapetime':
                                  datetime.datetime.now()}).inserted_id
    assert isinstance(poll_id, object)

    # extract data
    output = DBtable.find_one()
    assert isinstance(output, dict)
    assert output.get('headlines') == ['this is a test', 'this is a test2']
    assert isinstance(output.get('_id'), bson.objectid.ObjectId)

    # test ExtractHeadlines(collection, searchstring)
    result = ExtractHeadlines(DBtable, 'this')
    assert result[1][1] == 'testsite'
    assert isinstance(result[0][2], datetime.datetime)

    result = ExtractHeadlines(DBtable, 'Not Present')
    assert isinstance(result, list)
    assert len(result) == 0

    # clean up database by deleting test database.
    # Hard coded to make sure it doesn't drop the production database.
    client.drop_database('NewDatabase')


def test_mainquery():
    DBurl = 'mongodb://localhost:27017/'
    DB = scrapedata(DBurl)
    DBtable = DB.headlines
    # Test the main function.
    output = mainquery(DBtable, ' ')  # because all headlines will have spaces.

    assert isinstance(output, pandas.core.frame.DataFrame)
