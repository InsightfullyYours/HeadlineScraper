def scrapedata(DBurl):
    """
    This function is the main website scraper.  It scrapes the data from the
    web and loads it into the database.

    Input:
        DBurl: The URL of the headline database.
    Output:
        DB: The constructed DB object
    """

    from ..Project.scrapers import WebScrapers
    from ..Project.utilities import ConnectToDB, InitializeDB
    import sys

    client = ConnectToDB(DBurl)

    if not client:
        sys.exit('Connection Failure: Quitting')
    else:
        # Access the database
        DBname = 'NewsHeadlines'
        DB = InitializeDB(client, DBname)

        # Check NYTimes
        nytimes = WebScrapers('http://www.nytimes.com')
        data = nytimes.OpenWebsite()
        DB.headlines.insert_one(nytimes.NYTParse(data))

        # Check Foxnews
        foxnews = WebScrapers('http://www.foxnews.com/')
        data = foxnews.OpenWebsite()
        DB.headlines.insert_one(foxnews.FOXParse(data))

        return DB
        # # Check CNN
        # cnn = WebScrapers('http://www.cnn.com/')
        # data = cnn.OpenWebsite()
        # poll_id = DB.headlines.insert_one(cnn.CNNParse(data))
