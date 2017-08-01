import mwclient
import mwparserfromhell
import unidecode
import wikint.utils.text

def kind():
    return 'company'

def create(page):
    return Company(page)

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

# TODO: research top 100 section names
MISC_SECTIONS = [
    'see also',
    'references',
    'external links',
]

# TODO: make this "Organization"
# Make "organization" alias
class Company:

    def __init__(self, page):
        self.page = page
        self.__name = ()
        self.__websites = ()
        self.__brands = ()
        self.__products = ()

    @property
    def name(self):
        if self.__name is ():
            self.__name = (None,)
            if 'name' in self.page.params:
                self.__name = (self.page.infobox.get('name').value,)
        return self.__name[0]

    @property
    def websites(self):
        if self.__websites is ():
            websites = set()
            self.__websites = (websites,)
            for name in INFOBOX['website']:
                if name in self.page.params:
                    value = mwparserfromhell.parse(
                        self.page.infobox.get(name).value.strip())
                    for node in value.nodes:
                        if type(node) is mwparserfromhell.nodes.text.Text:
                            websites.update(wikint.utils.text.extract_domains(unicode(node)))
                        elif type(node) is mwparserfromhell.nodes.template.Template:
                            if node.name == 'URL' and node.params:
                                websites.update(wikint.utils.text.extract_domains(unicode(node.params[0])))
        return self.__websites[0]

    @property
    def brands(self):
        if self.__brands is ():
            brands = set()
            self.__brands = (brands,)
            for name in INFOBOX['brands']:
                if name in self.page.params:
                    value = mwparserfromhell.parse(
                        self.page.infobox.get(name).value.strip())
                    for node in value.nodes:
                        if type(node) is mwparserfromhell.nodes.wikilink.Wikilink:
                            page = self.page.site.page(node.title)
                            for section in page.lists:
                                if not section['node'].title.strip().lower() in MISC_SECTIONS:
                                    for item in section['list']:
                                        itemwords = list()
                                        for itemnode in item.nodes:
                                            if type(itemnode) is mwparserfromhell.nodes.text.Text:
                                                itemwords.append(unicode(itemnode).strip())
                                            elif type(itemnode) is mwparserfromhell.nodes.wikilink.Wikilink:
                                                itemwords.append(unicode(itemnode.title).strip())
                                            elif type(itemnode) is mwparserfromhell.nodes.template.Template:
                                                itemname = itemnode.name.strip().lower().split()
                                                if itemname and itemname[0] == 'anchor':
                                                    if itemnode.params:
                                                        itemwords.append(unicode(itemnode.params[0]).strip())
                                        itemtext = unidecode.unidecode(' '.join(itemwords).strip().split('.')[0])
                                        # TODO: filter second-level lists
                                        # TODO: get first noun of item
                                        # TODO: create list handler class
                                        # TODO: List(page)
                                        brands.add(itemtext)
        return self.__brands[0]

    @property
    def subsidiaries(self):
        pass

    @property
    def parent(self):
        pass

    def owner(self):
        pass