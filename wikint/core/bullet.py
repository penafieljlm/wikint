import mwparserfromhell
import unidecode

class Bullet:
    '''Represents a bullet found within a page's/section's content'''

    def __init__(self, section, parent, level, content):
        self.__section = section
        self.__parent = parent
        self.__level = level
        self.__children = list()
        self.__content = content
        self.__code = ()
        self.__text = ()

    @property
    def section(self):
        '''Returns the section that contains this bullet'''
        return self.__section

    @property
    def parent(self):
        '''Returns the parent bullet of this bullet'''
        return self.__parent

    @property
    def level(self):
        '''Returns the level of this bullet'''
        return self.__level

    @property
    def children(self):
        '''Returns the list of children of this bullet'''
        return self.__children

    @property
    def content(self):
        '''Returns the content of this bullet'''
        return self.__content

    @property
    def code(self):
        '''Return parsed contents of this bullet'''
        if self.__code is ():
            # Initialize this property
            code = mwparserfromhell.parse(self.content)
            self.__code = (code,)
        # Return the code
        return self.__code[0]

    @property
    def text(self):
        '''Transform the templates, tags, links, etc. in the bullet's contents
        into plain text'''
        if self.__text is ():
            # Gather the list of words in the bullet
            words = list()
            for node in self.code.nodes:
                # Handle text nodes
                if type(node) is mwparserfromhell.nodes.text.Text:
                    words.append(unicode(node).strip())
                # Handle link nodes
                elif type(node) is mwparserfromhell.nodes.wikilink.Wikilink:
                    words.append(unicode(node.title).strip())
                # Handle template nodes
                elif type(node) is mwparserfromhell.nodes.template.Template:
                    # Handle anchor templates
                    name = node.name.strip().lower().split()
                    if name and name[0] == 'anchor':
                        if node.params:
                            words.append(unicode(node.params[0]).strip())
            # Combine the words present in the list element
            text = unidecode.unidecode(' '.join(words).strip())
            # Initialize the property
            self.__text = (text,)
        # Return the text
        return self.__text[0]

    def __str__(self):
        return self.code.__str__()

    def __repr__(self):
        return self.code.__repr__()