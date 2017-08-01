import mwparserfromhell
import wikint.assets
import wikint.assets.company

class PageNotFoundException(Exception):

    def __init__(self, title):
        self.page = page
        self.message = 'A page titled "{}" was not found'.format(page)


class Page:

    def __init__(self, site, title):
        content = site.site.pages[title].text()
        if not content: raise PageNotFoundException(title)
        self.site = site
        self.title = title
        self.content = content
        self.__code = ()
        self.__nodes = ()
        self.__templates = ()
        self.__wikilinks = ()
        self.__sections = ()
        self.__lists = ()
        self.__infobox = ()
        self.__params = ()
        self.__kind = ()
        self.__asset = ()

    @property
    def code(self):
        if self.__code is ():
            self.__code = (mwparserfromhell.parse(self.content),)
        return self.__code[0]

    @property
    def nodes(self):
        if self.__nodes is ():
            self.__nodes = (self.code.nodes,)
        return self.__nodes[0]

    @property
    def templates(self):
        if self.__templates is ():
            self.__templates = (self.code.filter_templates(),)
        return self.__templates[0]

    @property
    def wikilinks(self):
        if self.__wikilinks is ():
            self.__wikilinks = (self.code.filter_wikilinks(),)
        return self.__wikilinks[0]        

    @property
    def sections(self):
        if self.__sections is ():
            sections = list()
            self.__sections = (sections,)
            current = None
            for node in self.nodes:
                if type(node) is mwparserfromhell.nodes.heading.Heading: 
                    current = {
                        'node': node,
                        'content': list(),
                    }
                    sections.append(current)
                elif current:
                    current['content'].append(node)
        return self.__sections[0]

    @property
    def lists(self):
        if self.__lists is ():
            lists = list()
            self.__lists = (lists,)
            for section in self.sections:
                nodelist = list()
                node = {
                    'node': section['node'],
                    'list': nodelist,
                }
                content = ''.join([unicode(c) for c in section['content']])
                for line in content.split('\n'):
                    line = line.strip()
                    if line.startswith('*'):
                        nodelist.append(mwparserfromhell.parse(line[1:].strip()))
                lists.append(node)
        return self.__lists[0]

    @property
    def infobox(self):
        if self.__infobox is ():
            self.__infobox = (None,)
            for template in self.templates:
                name = template.name.strip().split()
                if name and name[0].lower() == 'infobox':
                    self.__infobox = (template,)
                    break
        return self.__infobox[0]

    @property
    def params(self):
        if self.__params is ():
            params = list()
            self.__params = (params,)
            for param in self.infobox.params:
                params.append(param.name.strip())                
        return self.__params[0]

    @property
    def kind(self):
        if self.__kind is ():
            self.__kind = (' '.join(self.infobox.name.strip().split()[1:]),)
        return self.__kind[0]

    @property
    def asset(self):
        if self.__asset is ():
            self.__asset = (None,)
            for asset_kind in wikint.assets.MODULES:
                if asset_kind.kind() == self.kind:
                    self.__asset = (asset_kind.create(self),)
        return self.__asset[0]
