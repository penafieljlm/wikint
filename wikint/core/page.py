import mwparserfromhell
import wikint.core.section

class PageNotFoundException(Exception):
    '''Raised when a page can't be found'''

    def __init__(self, page):
        self.page = page
        self.message = 'A page titled "{}" was not found'.format(page)


class Page:
    '''Class for extracting content from Wikipedia pages'''

    def __init__(self, site, title):
        content = site.site.pages[title].text()
        if not content: raise PageNotFoundException(title)
        self.__site = site
        self.__title = title
        self.__content = content
        self.__code = ()
        self.__kind = ()
        self.__infobox = ()
        self.__section = ()
        self.__asset = ()

    @property
    def site(self):
        '''Returns the site that this page belongs to'''
        return self.__site

    @property
    def title(self):
        '''Returns the title of the page'''
        return self.__title

    @property
    def content(self):
        '''Returns the text content of the page'''
        return self.__content

    @property
    def code(self):
        '''Returns the parsed contents of the page'''
        if self.__code is ():
            self.__code = (mwparserfromhell.parse(self.content),)
        return self.__code[0]

    @property
    def kind(self):
        '''Returns the entity kind discussed in the page'''
        if self.__kind is ():
            self.__kind = self.infobox['__kind']
        return self.__kind[0]

    @property
    def infobox(self):
        '''Returns the first infobox template on the page as a dict'''
        if self.__infobox is ():
            # Initialize property
            infobox = dict()
            self.__infobox = (infobox,)
            # Go over the list of templates in the page
            for node in self.code.filter_templates():
                # Canonicalize the name and split by space
                name = node.name.strip().split()
                # Determine entity kind and include in infobox dict
                infobox['__kind'] = name[1:]
                # Handle ecnountered infobox template
                if name and name[0].lower() == 'infobox':
                    # Go over the infobox's parameters
                    for param in node.params:
                        # Extract infobox keys and values
                        pname = param.name.strip()
                        pvalue = param.value
                        # Add to the infobox dictionary
                        infobox[pname] = pvalue
                    # Stop looking for another infobox
                    break
        # Return the infobox dictionary
        return self.__infobox[0]

    @property
    def section(self):
        '''Returns the page as a section object to allow traversal of
        sections and subsections'''
        if self.__section is ():
            # Initialize property
            section = wikint.core.section.Section(
                    self, None, 0, self.title, self.content)
            self.__section = (section,)
        # Return sections and contents
        return self.__section[0]