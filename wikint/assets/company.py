import mwparserfromhell
import wikint.assets.list
import wikint.utils.text

INFOBOX = {
    'website': [
        'website',
        'homepage',
    ],
    'brands': [
        'brands',
        'products',
    ],
}

class PageIsNotACompanyException(Exception):
    '''Raised when an attempt is made to interpret the page as a company'''

    def __init__(self, page):
        self.page = page
        self.message = 'The page "{}" is not a company'.format(page.title)

# TODO: make this "Organization"
# Make "organization" alias
class Company:
    '''Represents a company page'''

    def __init__(self, page):
        # Ensure the page being interpreted is a list
        if page.kind != 'company':
            raise PageIsNotACompanyException(page)
        # Initialize attributes
        self.__page = page
        self.__name = ()
        self.__websites = ()
        self.__brands = ()
        self.__products = ()

    @property
    def page(self):
        '''Returns the page being wrapped'''
        return self.__page

    @property
    def name(self):
        '''Returns the name of the company'''
        if self.__name is ():
            self.__name = (None,)
            if 'name' in self.page.infobox.keys():
                self.__name = (self.page.infobox['name'].value,)
        return self.__name[0]

    @property
    def websites(self):
        '''Returns the list of websites of the company'''
        if self.__websites is ():
            websites = set()
            self.__websites = (websites,)
            for name in INFOBOX['website']:
                if name in self.page.infobox.keys():
                    value = mwparserfromhell.parse(
                        self.page.infobox[name].value.strip())
                    for node in value.nodes:
                        if type(node) is mwparserfromhell.nodes.text.Text:
                            websites.update(wikint.utils.text.domains(unicode(node)))
                        elif type(node) is mwparserfromhell.nodes.template.Template:
                            if node.name == 'URL' and node.params:
                                websites.update(wikint.utils.text.domains(unicode(node.params[0])))
        return self.__websites[0]

    @property
    def brands(self):
        '''Returns the list of products and brands of the company'''
        if self.__brands is ():
            # Inspect the infobox for aliases of "brands"
            brands = set()
            for name in INFOBOX['brands']:
                # If the page's infobox contains the current alias
                if name in self.page.infobox.keys():
                    # Extract its value
                    value = mwparserfromhell.parse(
                        self.page.infobox[name].strip())
                    # And iterate over the nodes
                    for node in value.nodes:
                        # If we encounter a wikilink
                        if type(node) is mwparserfromhell.nodes.wikilink.Wikilink:
                            # It's probably a list page
                            page = self.page.site.page(node.title)
                            try:
                                # Parse as a list page and extract elements
                                for e in wikint.assets.list.List(page).elements:
                                    brands.add(e)
                            except wikint.assets.list.PageIsNotAListException:
                                # Pass if the page is not a list page
                                pass
                            # TODO: handle direct links to product articles
            # Initialize the property
            self.__brands = (list(brands),)
        # TODO: look for products section in main article
        # Return the list of brands
        return self.__brands[0]

    @property
    def subsidiaries(self):
        pass

    @property
    def parent(self):
        pass

    def owner(self):
        pass