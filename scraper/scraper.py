import sys
from bs4 import BeautifulSoup
import urllib
import requests
from pprint import pprint
from datetime import date, timedelta

"""
scraper [campground] [date] [number_of_days]
return url, available/reserved

todo - cache implementation for better performance/bandwidth usave
todo - better implementation for url structures
todo - implement 'non 1' number of days
"""

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

def is_campsite_available(campground, date, number_of_days):
    pass

def get_campsite_info(url, d):
    print "Scraping..." + url 

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
    return cols

def get_campsite_status(campsite_status_array, d, number_of_days):
    for index in range(len(campsite_status_array)):
        date_var = d + timedelta(days=index)
        # if campsite_status_array[index] == "A":
        #    print(campsite_status_array[index] + " " + date_var.strftime("%m/%d/%y") + " " + date_var.strftime("%a"))
        if campsite_status_array[index] == "A" and index == 0:
            return True
        else:
            return False

def main():
    """Main entry point for the script"""

    campground_names = [
        "Angel Island State Park, CA"
        ]

    campsites_url = [
       'http://www.reserveamerica.com/campsiteDetails.do?siteId=535&contractCode=CA&parkId=120003',
       'http://www.reserveamerica.com/campsiteDetails.do?siteId=536&contractCode=CA&parkId=120003',
       'http://www.reserveamerica.com/campsiteDetails.do?siteId=537&contractCode=CA&parkId=120003'
        ]

    dates_url = [
        date(2016, 8, 6),
        date(2016, 8, 20),
        date(2016, 8, 24)
        ]

    for url in campsites_url:
        for d in dates_url:
            url_var = url + '&arvdate=' + d.strftime("%m/%d/%y") + '&lengthOfStay=1'
            if get_campsite_status(get_campsite_info(url_var, d), d, 1):
                print 'Campground' + ' ' + 'Campsite Available' + ' ' + d.strftime("%m/%d/%y") + ' ' + d.strftime("%a") + ' ' + url_var
    pass

if __name__ == '__main__':
    sys.exit(main())
