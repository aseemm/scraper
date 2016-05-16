import sys
from bs4 import BeautifulSoup
import urllib

def main():
    """Main entry point for the script"""
    print "Hello World!"

    r = urllib.urlopen('https://en.wikipedia.org/wiki/List_ofstate_and_union_territory_capitals_in_India').read()
    soup = BeautifulSoup(r, "html.parser")

    # print type(soup)
    # print soup.prettify().encode('utf-8')
    # print soup.title
    print soup.title.string

    print soup.a
    all_links = soup.find_all("a")
    for link in all_links:
        print link.get("href")

    all_tables = soup.find_all("table")
    for table in all_tables:
        print table

    pass

if __name__ == '__main__':
    sys.exit(main())
