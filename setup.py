try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Wikipedia-based organisation-centric OSINT',
    'author': 'John Lawrence M. Penafiel',
    'url': 'https://github.com/penafieljlm/wikint',
    'download_url': 'https://github.com/penafieljlm/wikint',
    'author_email': 'penafieljlm@gmail.com',
    'version': '0.1',
    'install_requires': [
        'mwclient',
        'mwparserfromhell',
    ],
    'packages': find_packages(),
    'scripts': ['inq'],
    'name': 'inquisitor'
}

setup(**config)