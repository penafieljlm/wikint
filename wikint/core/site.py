import mwclient
import wikint.page

class Site:

	def __init__(self, site):
		self.site = mwclient.Site(site)

	def page(self, title):
		content = self.site.pages[title].text()
		return wikint.page.Page(title, content)
