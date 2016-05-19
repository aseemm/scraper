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

def is_campsite_available(campground, campsites, d, number_of_days):
    for url in campsites:
        url_var = url + '&arvdate=' + d.strftime("%m/%d/%y") + '&lengthOfStay=1'
        # print url_var
        campsite_reservation_map = get_campsite_info(url_var, d) 
        if get_campsite_status(campsite_reservation_map, d, 1):
            print campground + ' - ' + 'Campsite Available' + ' ' + d.strftime("%m/%d/%y") + ' ' + d.strftime("%a") + ' - ' + url_var

def get_campsite_info(url, d):
    # print "Scraping..." + url 
    resp = requests.get(url,proxies=urllib.getproxies())
    soup = BeautifulSoup(resp.text,"html.parser")
    # print soup.prettify().encode('utf-8')
    
    data = []
    table = soup.find('table', attrs={'id':'calendar'})

    try: 
        table_body = table.find('tbody')
    except AttributeError:
        return []
        
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele]) # get rid of empty values
    return cols

def get_campsite_status(campsite_reservation_map, d, number_of_days):
    for index in range(len(campsite_reservation_map)):
        date_var = d + timedelta(days=index)
        # if campsite_reservation_map[index] == "A":
        #    print(campsite_reservation_map[index] + " " + date_var.strftime("%m/%d/%y") + " " + date_var.strftime("%a"))
        if campsite_reservation_map[index] == "A" and index == 0:
            return True
        else:
            return False

def main():
    """Main entry point for the script"""

    input_info = [
        ["DL Bliss State Park, CA", date(2016, 8, 6)],
        ["DL Bliss State Park, CA", date(2016, 8, 13)],
        ["DL Bliss State Park, CA", date(2016, 8, 20)],
        ["DL Bliss State Park, CA", date(2016, 8, 27)],
        ["Angel Island State Park, CA", date(2016, 8, 6)],
        ["Angel Island State Park, CA", date(2016, 8, 13)],
        ["Angel Island State Park, CA", date(2016, 8, 20)],
        ["Angel Island State Park, CA", date(2016, 8, 24)],
        ["Angel Island State Park, CA", date(2016, 8, 27)],
        ]

    campground_info = [
        "Angel Island State Park, CA"
        ]

    angel_island_campsite_info = [
       'http://www.reserveamerica.com/campsiteDetails.do?siteId=535&contractCode=CA&parkId=120003',
       'http://www.reserveamerica.com/campsiteDetails.do?siteId=536&contractCode=CA&parkId=120003',
       'http://www.reserveamerica.com/campsiteDetails.do?siteId=537&contractCode=CA&parkId=120003',
       'http://www.reserveamerica.com/campsiteDetails.do?siteId=538&contractCode=CA&parkId=120003',
       'http://www.reserveamerica.com/campsiteDetails.do?siteId=539&contractCode=CA&parkId=120003',
       'http://www.reserveamerica.com/campsiteDetails.do?siteId=540&contractCode=CA&parkId=120003',
        ]

    dl_bliss_campsite_info = [
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2455&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2456&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2457&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2458&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2459&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2460&contractCode=CA&parkId=120099',

        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2461&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2462&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2463&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2464&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2465&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2466&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2467&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2468&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2469&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2470&contractCode=CA&parkId=120099',

        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2471&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2472&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2473&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2474&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2475&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2476&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2477&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2478&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2479&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2480&contractCode=CA&parkId=120099',

        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2481&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2482&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2483&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2484&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2485&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2486&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2487&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2488&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2489&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2490&contractCode=CA&parkId=120099',

        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2491&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2492&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2493&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2494&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2495&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2496&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2497&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2498&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2499&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2500&contractCode=CA&parkId=120099',

        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2501&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2502&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2503&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2504&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2505&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2506&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2507&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2508&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2509&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2510&contractCode=CA&parkId=120099',

        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2511&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2512&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2513&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2514&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2515&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2516&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2517&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2518&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2519&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2520&contractCode=CA&parkId=120099',

        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2521&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2522&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2523&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2524&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2525&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2526&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2527&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2528&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2529&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2530&contractCode=CA&parkId=120099',

        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2531&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2532&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2533&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2534&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2535&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2536&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2537&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2538&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2539&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2540&contractCode=CA&parkId=120099',

        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2541&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2542&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2543&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2544&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2545&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2546&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2547&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2548&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2549&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2550&contractCode=CA&parkId=120099',

        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2551&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2552&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2553&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2554&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2555&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2556&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2557&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2558&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2559&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2560&contractCode=CA&parkId=120099',

        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2561&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2562&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2563&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2564&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2565&contractCode=CA&parkId=120099',
        'http://www.reserveamerica.com/campsiteDetails.do?siteId=2566&contractCode=CA&parkId=120099',
        ]

    for input_var in input_info:
        if input_var[0] == "Angel Island State Park, CA":
            is_campsite_available(input_var[0], angel_island_campsite_info, input_var[1], 1)
        if input_var[0] == "DL Bliss State Park, CA":
            is_campsite_available(input_var[0], dl_bliss_campsite_info, input_var[1], 1)

    pass

if __name__ == '__main__':
    sys.exit(main())
