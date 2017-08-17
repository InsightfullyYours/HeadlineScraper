
class WebScrapers(object):
    """
    The webscrapers.  The class takes in a website and creates an instance
    specific to the website.

    Input: Website as string ('http://www.example.com')
    Output: WebScraper instance centered around that URL

    Operation:
    OpenWebsite(): Opens the input URL and returns a BeautifulSoup object.
    NYTParse(bsObj): Parses a BeautifulSoup object as if it were NYTimes
    FOXParse(bsObj): Parses a BeautifulSoup object as if it were FOX News
    CNNParse(bsObj): Parses a BeautifulSoup object as if it were CNN
    MSNBCParse(bsObj): Parses a BeautifulSoup object as if it were MSNBC
    """

    def __init__(self, url):
        # Create the instance around the specific URL
        self.url = url

    def OpenWebsite(self):
        # Connect to the url, download the html, and convert it into a
        # BeautifulSoup object
        from urllib.request import urlopen
        from urllib.error import HTTPError
        import socket
        from bs4 import BeautifulSoup

        # Connect to URL and extract HTML, with error catching
        try:
            html = urlopen(self.url)
        except HTTPError as err:
            print('Error 404: cannot be accessed!')
            raise
        except socket.timeout:
            print(" ".join(("can't access", self.url,
                            "due to connection timeout!")))
            raise
        except AttributeError as err:
            print('Input format or other error: ' + str(err))
            raise
        except ValueError as err:
            print('Value error: ' + str(err))
        except UnboundLocalError as err:
            print('Other error: ' + str(err))
            raise

        # Convert the html into a BeautifulSoup object, with error catching
        try:
            bsObj = BeautifulSoup(html.read(), 'lxml')
        except AttributeError as e:
            print('BeautifulSoup could not process the html.')
            raise
        return bsObj

    def NYTParse(self, bsObj):
        # Parse the New York Times website
        import datetime
        # from bs4 import BeautifulSoup

        # Extract all articles
        articleList = bsObj.findAll({'h1', 'h2', 'h3', 'h4'},
                                    {'class': 'story-heading'})

        # Create a set of just the article headlines
        headline = set()
        for article in articleList:
            headline.add(article.get_text().strip())

        return {'site': 'NYTimes', 'scrapetime': datetime.datetime.now(),
                'headlines': list(headline)}

    def FOXParse(self, bsObj):
        # Parse the Fox News website
        import datetime
        # from bs4 import BeautifulSoup

        # Extract all the articles
        articleList = bsObj.findAll({'li', 'h3', 'h2', 'h1'})

        # Create a set of just the article headlines
        headline = set()
        for article in articleList:
            # ignore "articles" that are actually links to other sections.
            if len(str(article)) >= 100:
                headline.add(article.get_text().strip())

        return {'site': 'Fox News', 'scrapetime': datetime.datetime.now(),
                'headlines': list(headline)}

    def CNNParse(self, bsObj):
        # Parse the MSNBC website
        import datetime
        # from bs4 import BeautifulSoup
        import re

        # Extract all the articles
        # articleList = bsObj.findAll({'h3','h2','h1'})
        articleList = bsObj.findAll(text=re.compile('headline'))
        print(articleList)

    # span class="featured-slider-menu__item__link__title

        # Create a set of just the article headlines
        headline = set()
        for article in articleList:
            print(article)
            print('>>>>>' + article.get_text().strip())
            print('-------------------------------------')

            headline.add(article.get_text().strip())

        return {'site': 'CNN', 'scrapetime': datetime.datetime.now(),
                'headlines': list(headline)}

    def MSNBCParse(self, bsObj):
        # Parse the MSNBC website
        import datetime
        # from bs4 import BeautifulSoup

        # Extract all the articles
        articleList = bsObj.findAll({'a', 'h3', 'h2', 'h1'})

    # span class="featured-slider-menu__item__link__title

        # Create a set of just the article headlines
        headline = set()
        for article in articleList:
            print(article)
            print('>>>>>' + article.get_text().strip())
            print('-------------------------------------')

            headline.add(article.get_text().strip())

        return {'site': 'MSNBC', 'scrapetime': datetime.datetime.now(),
                'headlines': list(headline)}

# test = OpenWebsite('http://www.nytimes.com')

# print(test)
