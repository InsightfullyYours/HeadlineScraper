"""
This function runs a script that both scrapes the websites of major News
outlets for their headlines and then searches those headlines for a
user-supplied search string.  This allows the user to compare coverage of
the same events between sources.

Every time this is run, it adds the scrapes to the database.  In this way
the utilization of the function by users is what generates the database.

"""

from ..Project.scrapedata import scrapedata
from ..Project.mainquery import mainquery

DBurl = 'mongodb://localhost:27017/'

DB = scrapedata(DBurl)

searchstring = input('Please enter the search string: ')

DBtable = DB.headlines
result = mainquery(DBtable, searchstring)
