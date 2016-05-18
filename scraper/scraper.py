import sys
from bs4 import BeautifulSoup
import urllib
import requests
from pprint import pprint
from datetime import date, timedelta

# soup.select("title")                              # get title tag
# soup.select("body a")                             # all 'a' tags inside body
# soup.select("html head title")                    # html->head->title
# soup.select("head > title")                       # head->title
# soup.select("p > a")                              # all 'a' tags inside 'p'
# soup.select("body > a")                           # all 'a' tags inside 'body'
# soup.select(".sister")                            # select by class
# soup.select("#link1")                             # select by id
# soup.select('a[href="http://example.com/elsie"]') # find tags by attribute value 
# soup.select('a[href^="http://example.com/"]')     # find tags by attribute value, all contains 'http://example.com/'
# soup.select('p[lang|=en]')                        # match language code

def get_campsite_info(url, d):
    url = url + '&arvdate=' + d.strftime("%m/%d/%y") + '&lengthOfStay=1'
    resp = requests.get(url,proxies=urllib.getproxies())
    soup = BeautifulSoup(resp.text,"html.parser")
    # print soup.prettify().encode('utf-8')
    
    data = []
    table = soup.find('table', attrs={'id':'calendar'})
    table_body = table.find('tbody')

    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele]) # get rid of empty values
    print cols[0]
    return cols[0]

def check_latest_status(status, url, d):
    for index in range(len(status)):
        d = d + timedelta(days=index)
        if status[index] == "A":
            print(status[index] + " " + d.strftime("%m/%d/%y") + " " + d.strftime("%a") + " " + url)

def main():
    """Main entry point for the script"""

    campsites_url = [
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=535&contractCode=CA&parkId=120003',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=536&contractCode=CA&parkId=120003',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=537&contractCode=CA&parkId=120003'
        ]

    dates_url = [
        date(2016, 8, 6),
        date(2016, 8, 20)
        ]

    d = date(2016, 8, 6)
    url = 'http://www.reserveamerica.com/campsiteDetails.do?siteId=535&contractCode=CA&parkId=120003' + '&arvdate=' + d.strftime("%m/%d/%y") + '&lengthOfStay=1'
    resp = requests.get(url,proxies=urllib.getproxies())
    soup = BeautifulSoup(resp.text,"html.parser")

    # r = urllib.urlopen('http://www.reserveamerica.com/campsiteDetails.do?siteId=535&contractCode=CA&parkId=120003&arvdate=08/6/2016&lengthOfStay=1').read()
    # soup = BeautifulSoup(r, "html.parser")

    # print type(soup)
    # print soup.prettify().encode('utf-8')

    # pprint(soup.select("#calendar"))
    
    data = []
    table = soup.find('table', attrs={'id':'calendar'})
    # table_head = table.find('thead')
    table_body = table.find('tbody')

    # rows = table_head.find_all('tr')
    # for row in rows:
    #     cols = row.find_all('th')
    #     cols = [ele.text.strip() for ele in cols]
    #     if cols: # get rid of month, prev, next week header
    #         data.append([ele for ele in cols if ele])# get rid of empty values

    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele]) # get rid of empty values

    for index in range(len(cols)):
        d = d + timedelta(days=index)
        if cols[index] == "A":
            print(cols[index] + " " + d.strftime("%m/%d/%y") + " " + d.strftime("%a") + " " + url)

    # table = soup.find("table", { "id" : "calendar" })
    # for row in table.findAll("tr"):
    #     cells = row.findAll("td")
    #     print cells

    # print soup.title
    # print soup.title.string
    # pprint(soup.select("title"))

    # print soup.a
    # all_links = soup.find_all("a")
    # for link in all_links:
    #    print link.get("href")

    # all_tables = soup.find_all("table")
    # for table in all_tables:
    #    print table

    print "Scraping..."
    for url in campsites_url:
        for d in dates_url:
            check_latest_status(get_campsite_info(url, d), url, d)
    pass

if __name__ == '__main__':
    sys.exit(main())
