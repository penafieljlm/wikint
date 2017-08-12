import mwclient
import wikint.core.page

class Site:
    '''Represents a Wiki site'''

    def __init__(self, site):
        self.__site = mwclient.Site(site)

    @property
    def site(self):
        '''Returns the primary mwclient Site instance'''
        return self.__site

    def page(self, title):
        '''Retrieves a page from the Wiki site with the provided title'''
        return wikint.core.page.Page(self, unicode(title))
