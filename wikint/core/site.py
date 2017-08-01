import mwclient
import wikint.core.page

class Site:

    def __init__(self, site):
        self.site = mwclient.Site(site)

    def page(self, title):
        return wikint.core.page.Page(self, unicode(title))
