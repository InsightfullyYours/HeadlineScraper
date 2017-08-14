def main():

    # This is the overall program that runs
    from Project.scrapers import WebScrapers
    from Project.utilities import ConnectToDB, InitializeDB, ExtractHeadlines
    import sys
    # import numpy as np
    import pandas as pd

    DBurl = 'mongodb://localhost:27017/'
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
        poll_id = DB.headlines.insert_one(nytimes.NYTParse(data))

        # Check Foxnews
        foxnews = WebScrapers('http://www.foxnews.com/')
        data = foxnews.OpenWebsite()
        poll_id = DB.headlines.insert_one(foxnews.FOXParse(data))

        # # Check CNN
        # cnn = WebScrapers('http://www.cnn.com/')
        # data = cnn.OpenWebsite()
        # poll_id = DB.headlines.insert_one(cnn.CNNParse(data))

        print('Scraping finished.')
        searchstring = input('Please enter the search string you want to search headlines for: ') # noqa

        queryresult = ExtractHeadlines(DB, searchstring)

        print('The Headlines that match your search string are:')
    #    print(queryresult)

        df = pd.DataFrame.from_records(queryresult, columns=['Headline', 'Source', 'Scrape Timestamp']) # noqa

        return df
