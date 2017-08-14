# This file performs unit testing on the program
from Project.main import main
from Project.scrapers import WebScrapers
from Project.utilities import ConnectToDB, InitializeDB, ExtractHeadlines

out = main()
print(out)
