# This file performs unit testing on the program
from ..Project.main import *
from ..Project.scrapers import *
from ..Project.utilities import *
import pytest
from bs4 import BeautifulSoup
from urllib.error import HTTPError, URLError
import datetime

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
    nytimes = WebScrapers('http://www.nytimes.com')
    data = nytimes.OpenWebsite()
    
    assert isinstance(nytimes, WebScrapers)
    assert isinstance(data, BeautifulSoup)
    assert isinstance(nytimes.NYTParse(data), dict)
    assert isinstance(nytimes.NYTParse(data).get('headlines'), list)
    assert isinstance(nytimes.NYTParse(data).get('site'), str)
    assert isinstance(nytimes.NYTParse(data).get('scrapetime'), datetime.datetime)
    
    foxnews = WebScrapers('http://www.foxnews.com')
    data = foxnews.OpenWebsite()
    
    assert isinstance(foxnews, WebScrapers)
    assert isinstance(data, BeautifulSoup)
    assert isinstance(foxnews.FOXParse(data), dict)
    assert isinstance(foxnews.FOXParse(data).get('headlines'), list)
    assert isinstance(foxnews.FOXParse(data).get('site'), str)
    assert isinstance(foxnews.FOXParse(data).get('scrapetime'), datetime.datetime)
    
def test_database():
    
    
    
    
#    nytimes = WebScrapers('http://www.nytimes.com') isinstance
#    data = nytimes.OpenWebsite()
#    poll_id = DB.headlines.insert_one(nytimes.NYTParse(data))
#
#
#
#    test_perfect_number_data = [(6,True),(28,True),(496,True),(8,False)]
#@pytest.mark.parametrize('x,expected',test_perfect_number_data)
#def test_perfect_number(x,expected, num):
#    #num = Numbers()
#ssert num.perfect_number(x) == expected
