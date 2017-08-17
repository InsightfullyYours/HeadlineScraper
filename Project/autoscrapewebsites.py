"""
This script automatically scrapes the data into the database.  This can be
set to run automatically on a schedule within the operating system to build up
the database.
"""

from ..Project.scrapedata import scrapedata

DBurl = 'mongodb://localhost:27017/'
DB = scrapedata(DBurl)
