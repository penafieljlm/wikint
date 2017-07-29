import mwclient
import mwparserfromhell

def type():
	return 'company'

def create(page):
	return Company(page)

class Company:

	def __init__(self, page):
		self.page = page
		# TODO: to be continue

	@property
	def name(self):
		pass

	@property
	def website(self):
		pass

	@property
	def former_name(self):
		pass

	@property
	def predecessor(self):
		pass

	@property
	def brands(self):
		pass

	@property
	def products(self):
		pass

	@property
	def subsidiaries(self):
		pass

	@property
	def parent(self):
		pass

	def owner(self):
		pass