try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Campsite Scraper',
    'author': 'Aseem Maheshwari',
    'url': 'URL to get it at.',
    'download_url': 'Where to download it.',
    'author_email': 'aseemm@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['scraper'],
    'scripts': [],
    'name': 'scraper'
}

setup(**config)
