import re
import nltk

# TODO: research top 100 section names
# https://en.wikipedia.org/wiki/Wikipedia:Manual_of_Style/Layout

# List of common Wikipedia sections
EXCLUSIONS = [
    'SEE ALSO',
    'REFERENCES',
    'EXTERNAL LINKS',
]

class PageIsNotAListException(Exception):
    '''Raised when an attempt is made to interpret the page as a list'''

    def __init__(self, page):
        self.page = page
        self.message = 'The page "{}" is not a list'.format(page.title)

class List:
    '''Represents a list page'''

    def __init__(self, page):
        # Ensure the page being interpreted is a list
        if not page.title.strip().lower().startswith('list of'):
            raise PageIsNotAListException(page)
        # Initialize attributes
        self.__page = page
        self.__elements = ()

    @property
    def page(self):
        return self.__page

    @property
    def elements(self):
        '''Return the elements listed in the page'''
        # TODO: try to detect if the list page is alphabetical,
        # TODO: category-based, etc.
        if self.__elements is ():
            # Initialize the property
            elements = list()
            self.__elements = (elements,)
            # Acquire each of the page's sections
            for name, section in self.page.section.sections.iteritems():
                # If the section is to be excluded
                if name in EXCLUSIONS:
                    continue
                # Iterate over the section's bullets
                for bullet in section.bullets:
                    # Extract the bullet's contents
                    text = bullet.text.split('. ')[0].strip()
                    # Extract named entities from the bullet
                    tokens = nltk.word_tokenize(text)
                    tags = nltk.pos_tag(tokens)
                    chunks = nltk.ne_chunk(tags)
                    # Extract the first named entity
                    entity = list()
                    for chunk in chunks.leaves():
                        data, tag = chunk
                        if tag == 'NNP':
                            entity.append(data)
                        else:
                            break
                    entity = ' '.join(entity)
                    # Append the element in the list
                    element = entity
                    elements.append(element)
        # Return the elements
        return self.__elements[0]