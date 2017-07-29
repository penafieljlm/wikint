import mwparserfromhell
import wikint.assets.company

ASSET_TYPES = [
	wikint.assets.company,
]

class PageNotFoundException(Exception):

	def __init__(self, title):
		self.page = page
		self.message = 'A page titled "{}" was not found'.format(page)


class Page:

	def __init__(self, title, content):
		# Verify
		if not content: raise PageNotFoundException(title)
		# Attributes
		self.title = title
		self.content = content
		self.code = mwparserfromhell.parse(self.content)
		self.templates = self.code.filter_templates()
		# Properties
		self.__infobox = ()
		self.__type = ()
		self.__asset = ()

	@property
	def infobox(self):
		if self.__infobox is ():
			for template in self.templates:
				name = template.name.strip().split()
				if name and name[0] == 'Infobox':
					self.__infobox = (template)
					break
			self.__infobox = (None)
		return self.__infobox[0]

	@property
	def type(self):
		if self.__type is ():
			self.__type = (' '.join(self.infobox.name.strip().split()[1:]))
		return self.__type[0]

	@property
	def asset(self):
		if self.__asset is ():
			for asset_type in ASSET_TYPES:
				if asset_type.type() == self.type:
					self.__asset = (asset_type.create(self))
		return self.__asset[0]
