
class WebScrapers(object):
    # The webscrapers.  The class takes in a BeautifulSoup object and parses it appropriately.
    
    def __init__(self, url):
        #Create the object around the specific URL
        self.url = url

    def OpenWebsite(self):
        # Connect to the url, download the html, and convert it into a BeautifulSoup object
        from urllib.request import urlopen
        from urllib.error import HTTPError
        from bs4 import BeautifulSoup

        #Connect to URL and extract HTML, with error catching
        try:
            html = urlopen(self.url)
        except HTTPError:
            print('>>> Error 404: cannot be accessed!\n')
            raise
        except socket.timeout:
            print(" ".join(("can't access", self.url, "due to connection timeout!")))
            raise
        
        #Convert the html into a BeautifulSoup object, with error catching
        try:
            bsObj = BeautifulSoup(html.read(), 'lxml')
        except AttributeError as e:
            print('BeautifulSoup could not process the html.')
            raise
        return bsObj

    def NYTParse(self,bsObj):
        #Parse the New York Times website
        import datetime
        from bs4 import BeautifulSoup
        
        #Extract all articles
        articleList = bsObj.findAll({'h1','h2','h3','h4'},{'class':'story-heading'})
        
        #Create a set of just the article headlines
        headline = set()
        for article in articleList:
            headline.add(article.get_text().strip())
                   
        return {'site':'NYTimes', 'scrapetime': datetime.datetime.now(), 'headlines': list(headline)}
    
    def FOXParse(self,bsObj):
        # Parse the Fox News website
        import datetime
        from bs4 import BeautifulSoup        
        
        #Extract all the articles
        articleList = bsObj.findAll({'li','h3','h2','h1'})
        
        #Create a set of just the article headlines
        headline = set()
        for article in articleList:
            #ignore "articles" that are actually links to other sections.
            if len(str(article)) >= 100:
                headline.add(article.get_text().strip())
        
        return {'site':'Fox News', 'scrapetime': datetime.datetime.now(), 'headlines': list(headline)}
    
    def CNNParse(self,bsObj):
        # Parse the MSNBC website
        import datetime
        from bs4 import BeautifulSoup  
        import re
        
        #Extract all the articles
     #   articleList = bsObj.findAll({'h3','h2','h1'})
        articleList = bsObj.findAll(text=re.compile('headline'))
        print(articleList)
    
    #span class="featured-slider-menu__item__link__title
    
    

        
        #Create a set of just the article headlines
        headline = set()
        for article in articleList:
            print(article)
            print('>>>>>' + article.get_text().strip())
            print('-------------------------------------')
            
            headline.add(article.get_text().strip())
        
        return {'site':'CNN', 'scrapetime': datetime.datetime.now(), 'headlines': list(headline)}
   
    
    
    def MSNBCParse(self,bsObj):
        # Parse the MSNBC website
        import datetime
        from bs4 import BeautifulSoup        
        
        #Extract all the articles
        articleList = bsObj.findAll({'a','h3','h2','h1'})
    
    #span class="featured-slider-menu__item__link__title
    

        #Create a set of just the article headlines
        headline = set()
        for article in articleList:
            print(article)
            print('>>>>>' + article.get_text().strip())
            print('-------------------------------------')
            
            headline.add(article.get_text().strip())
        
        return {'site':'MSNBC', 'scrapetime': datetime.datetime.now(), 'headlines': list(headline)}

#test = OpenWebsite('http://www.nytimes.com')

#print(test)
