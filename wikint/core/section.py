import mwparserfromhell
import wikint.core.bullet

class SectionLevelLessThanChildException(Exception):
    '''Raised when a child section's level is greater than its parent'''

    def __init__(self, section, title, level):
        self.section = section
        self.message = ('A section titled "{}" with level {} was found under '
                        'a section title "{}" with level {}').format(
                            section.title,
                            section.level,
                            title,
                            level
                        )

class Section:
    '''Represents the contents of a page section'''

    def __init__(self, page, parent, level, title, content):
        self.__page = page
        self.__parent = parent
        self.__level = level
        self.__title = title.strip().upper()
        self.__content = content
        self.__code = ()
        self.__bullets = ()
        self.__sections = ()

    @property
    def page(self):
        '''Returns the page that contains this section'''
        return self.__page

    @property
    def parent(self):
        '''Returns the parent section of this section'''
        return self.__parent

    @property
    def level(self):
        '''Returns the depth of this section'''
        return self.__level

    @property
    def title(self):
        '''Returns the title of this section'''
        return self.__title

    @property
    def content(self):
        '''Returns the text content of this section'''
        return self.__content

    @property
    def code(self):
        '''Returns the parsed contents of this section'''
        if self.__code is ():
            self.__code = (mwparserfromhell.parse(self.content),)
        return self.__code[0]

    @property
    def bullets(self):
        '''Returns bullets contained within this section'''
        if self.__bullets is ():
            # Initialize the property
            bullets = list()
            self.__bullets = (bullets,)
            # Extract bullets from the content
            history = list()
            for line in self.content.split('\n'):
                line = line.strip()
                # Handle bullets
                if line.startswith('*'):
                    # Calculate bullet level
                    level = 0
                    for c in line:
                        if c == '*':
                            level += 1
                        else:
                            break
                    # Find parent bullet
                    parent = None
                    for bullet in reversed(history):
                        if bullet.level < level:
                            parent = bullet
                            break
                    # Create bullet
                    bullet = wikint.core.bullet.Bullet(
                        self, parent, level, line[1:].strip())
                    # Append to history
                    history.append(bullet)
                    # Append bullet to parent or list of bullets
                    if parent:
                        parent.children.append(bullet)
                    else:
                        bullets.append(bullet)
                # Handle everything else
                else:
                    # Reset history
                    history = list()
        # Return bullets
        return self.__bullets[0]

    @property
    def sections(self):
        '''Returns the list of child sections under this section'''
        if self.__sections is ():
            # Initialize the property
            sections = dict()
            self.__sections = (sections,)
            # Determine next section level
            level = None
            for node in self.code.nodes:
                # Handle heading
                if type(node) is mwparserfromhell.nodes.heading.Heading:
                    # Assert that child level is greater than parent level
                    if node.level <= self.level:
                        raise SectionLevelLessThanChildException(
                            self, node.title.strip().upper(), node.level)
                    # Try to determine the lowest child level
                    if not level or node.level < level:
                        level = node.level
            # Collect child section nodes
            current = None
            nodes = None
            for node in self.code.nodes:
                # Handle heading
                if (type(node) is mwparserfromhell.nodes.heading.Heading 
                        and node.level == level): 
                    # Commit current collection as a section
                    if current is not None and nodes is not None:
                        section = Section(self.page, self,
                            current.level, current.title, ''.join([
                                unicode(n) for n in nodes]))
                        sections[section.title] = section
                    # Initialize next collection
                    current = node
                    nodes = list()
                # Handle everything else
                elif current:
                    nodes.append(node)
            # Commit current collection as a section
            if current is not None and nodes is not None:
                section = Section(self.page, self,
                    current.level, current.title, ''.join([
                        unicode(n) for n in nodes]))
                sections[section.title] = section
        # Return sections
        return self.__sections[0]