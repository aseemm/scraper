import sys
from bs4 import BeautifulSoup
import urllib
import requests
from pprint import pprint
from datetime import date, timedelta
import smtplib

"""
scraper [campground] [date] [number_of_days]
return url, available/reserved

todo - cache implementation for better performance/bandwidth usave
todo - better implementation for globals
todo - implement 'non 1' number of days
todo - derive exclude_campsite list rather than manually specify
todo - check yosemite tuolumne meadows info again
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

# global
angel_island_siteid_info = [
   'http://www.reserveamerica.com/campsitePaging.do?contractCode=CA&parkId=120003&startIdx=0',
   ]
angel_island_campsite_url_head = 'http://www.reserveamerica.com/campsiteDetails.do?contractCode=CA&parkId=120003'
angel_island_switch_map = {'table_format': 1, 'exclude_campsites': ['546', '547', '544']}

dl_bliss_siteid_info = [
   'http://www.reserveamerica.com/campsitePaging.do?contractCode=CA&parkId=120099&startIdx=0',
   'http://www.reserveamerica.com/campsitePaging.do?contractCode=CA&parkId=120099&startIdx=25',
   'http://www.reserveamerica.com/campsitePaging.do?contractCode=CA&parkId=120099&startIdx=50',
   'http://www.reserveamerica.com/campsitePaging.do?contractCode=CA&parkId=120099&startIdx=75',
   'http://www.reserveamerica.com/campsitePaging.do?contractCode=CA&parkId=120099&startIdx=100',
   'http://www.reserveamerica.com/campsitePaging.do?contractCode=CA&parkId=120099&startIdx=125',
   ]
dl_bliss_campsite_url_head = 'http://www.reserveamerica.com/campsiteDetails.do?contractCode=CA&parkId=120099'
dl_bliss_switch_map = {'table_format': 1, 'exclude_campsites': ['15002']}

big_basin_siteid_info = [
   'http://www.reserveamerica.com/campsitePaging.do?contractCode=CA&parkId=120009&startIdx=0',
   'http://www.reserveamerica.com/campsitePaging.do?contractCode=CA&parkId=120009&startIdx=25',
   'http://www.reserveamerica.com/campsitePaging.do?contractCode=CA&parkId=120009&startIdx=50',
   'http://www.reserveamerica.com/campsitePaging.do?contractCode=CA&parkId=120009&startIdx=75',
   'http://www.reserveamerica.com/campsitePaging.do?contractCode=CA&parkId=120009&startIdx=100',
   'http://www.reserveamerica.com/campsitePaging.do?contractCode=CA&parkId=120009&startIdx=125',
   ]
big_basin_campsite_url_head = 'http://www.reserveamerica.com/campsiteDetails.do?contractCode=CA&parkId=120009'
big_basin_switch_map = {'table_format': 1, 'exclude_campsites': ['26646', '26642', '26632', '26634', '26647']}

yosemite_lower_pines_siteid_info = [
   'http://www.recreation.gov/campsitePaging.do?contractCode=NRSO&parkId=70928&startIdx=0',
   'http://www.recreation.gov/campsitePaging.do?contractCode=NRSO&parkId=70928&startIdx=25',
   'http://www.recreation.gov/campsitePaging.do?contractCode=NRSO&parkId=70928&startIdx=50',
   ]
yosemite_lower_pines_campsite_url_head = 'http://www.recreation.gov/camping/Lower_Pines/r/campsiteDetails.do?contractCode=NRSO&parkId=70928'
yosemite_lower_pines_switch_map = {'table_format': 0, 'exclude_campsites': []}

yosemite_upper_pines_siteid_info = [
   'http://www.recreation.gov/campsitePaging.do?contractCode=NRSO&parkId=70925&startIdx=0',
   'http://www.recreation.gov/campsitePaging.do?contractCode=NRSO&parkId=70925&startIdx=25',
   'http://www.recreation.gov/campsitePaging.do?contractCode=NRSO&parkId=70925&startIdx=50',
   'http://www.recreation.gov/campsitePaging.do?contractCode=NRSO&parkId=70925&startIdx=75',
   'http://www.recreation.gov/campsitePaging.do?contractCode=NRSO&parkId=70925&startIdx=100',
   'http://www.recreation.gov/campsitePaging.do?contractCode=NRSO&parkId=70925&startIdx=125',
   'http://www.recreation.gov/campsitePaging.do?contractCode=NRSO&parkId=70925&startIdx=150',
   'http://www.recreation.gov/campsitePaging.do?contractCode=NRSO&parkId=70925&startIdx=175',
   'http://www.recreation.gov/campsitePaging.do?contractCode=NRSO&parkId=70925&startIdx=200',
   'http://www.recreation.gov/campsitePaging.do?contractCode=NRSO&parkId=70925&startIdx=225',
   ]
yosemite_upper_pines_campsite_url_head = 'http://www.recreation.gov/camping/Upper_Pines/r/campsiteDetails.do?contractCode=NRSO&parkId=70925'
yosemite_upper_pines_switch_map = {'table_format': 0, 'exclude_campsites': []}

yosemite_north_pines_siteid_info = [
   'http://www.recreation.gov/campsitePaging.do?contractCode=NRSO&parkId=70927&startIdx=0',
   'http://www.recreation.gov/campsitePaging.do?contractCode=NRSO&parkId=70927&startIdx=25',
   'http://www.recreation.gov/campsitePaging.do?contractCode=NRSO&parkId=70927&startIdx=50',
   'http://www.recreation.gov/campsitePaging.do?contractCode=NRSO&parkId=70927&startIdx=75',
   ]
yosemite_north_pines_campsite_url_head = 'http://www.recreation.gov/camping/North_Pines/r/campsiteDetails.do?contractCode=NRSO&parkId=70927'
yosemite_north_pines_switch_map = {'table_format': 0, 'exclude_campsites': []}

yosemite_wawona_siteid_info = [
   'http://www.recreation.gov/campsitePaging.do?contractCode=NRSO&parkId=70924&startIdx=0',
   'http://www.recreation.gov/campsitePaging.do?contractCode=NRSO&parkId=70924&startIdx=25',
   'http://www.recreation.gov/campsitePaging.do?contractCode=NRSO&parkId=70924&startIdx=50',
   'http://www.recreation.gov/campsitePaging.do?contractCode=NRSO&parkId=70924&startIdx=75',
   ]
yosemite_wawona_campsite_url_head = 'http://www.recreation.gov/camping/Wawona/r/campsiteDetails.do?contractCode=NRSO&parkId=70924'
yosemite_wawona_switch_map = {'table_format': 0, 'exclude_campsites': []}

yosemite_crane_flat_siteid_info = [
   'http://www.recreation.gov/campsitePaging.do?contractCode=NRSO&parkId=70930&startIdx=0',
   'http://www.recreation.gov/campsitePaging.do?contractCode=NRSO&parkId=70930&startIdx=25',
   'http://www.recreation.gov/campsitePaging.do?contractCode=NRSO&parkId=70930&startIdx=50',
   'http://www.recreation.gov/campsitePaging.do?contractCode=NRSO&parkId=70930&startIdx=75',
   'http://www.recreation.gov/campsitePaging.do?contractCode=NRSO&parkId=70930&startIdx=100',
   'http://www.recreation.gov/campsitePaging.do?contractCode=NRSO&parkId=70930&startIdx=125',
   'http://www.recreation.gov/campsitePaging.do?contractCode=NRSO&parkId=70930&startIdx=150',
   ]
yosemite_crane_flat_campsite_url_head = 'http://www.recreation.gov/camping/Crane_Flat/r/campsiteDetails.do?contractCode=NRSO&parkId=70930'
yosemite_crane_flat_switch_map = {'table_format': 0, 'exclude_campsites': []}

yosemite_hodgdon_meadow_siteid_info = [
   'http://www.recreation.gov/campsitePaging.do?contractCode=NRSO&parkId=70929&startIdx=0',
   'http://www.recreation.gov/campsitePaging.do?contractCode=NRSO&parkId=70929&startIdx=25',
   'http://www.recreation.gov/campsitePaging.do?contractCode=NRSO&parkId=70929&startIdx=50',
   'http://www.recreation.gov/campsitePaging.do?contractCode=NRSO&parkId=70929&startIdx=75',
   'http://www.recreation.gov/campsitePaging.do?contractCode=NRSO&parkId=70929&startIdx=100',
   ]
yosemite_hodgdon_meadow_campsite_url_head = 'http://www.recreation.gov/camping/Hodgdon_Meadow/r/campsiteDetails.do?contractCode=NRSO&parkId=70929'
yosemite_hodgdon_meadow_switch_map = {'table_format': 0, 'exclude_campsites': []}

yosemite_tuolumne_meadows_siteid_info = [
   'http://www.recreation.gov/campsitePaging.do?contractCode=NRSO&parkId=70926&startIdx=0',
   ]
yosemite_tuolumne_meadows_campsite_url_head = 'http://www.recreation.gov/camping/Tuolumne_Meadows/r/campsiteDetails.do?contractCode=NRSO&parkId=70926'
yosemite_tuolumne_meadows_switch_map = {'table_format': 0, 'exclude_campsites': []}

def send_mail(user, pwd, recipient, subject, body):
    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        # print 'successfully sent the mail'
    except:
        print "failed to send mail"

def send_mail_over_ssl(user, pwd, recipient, subject, body):
    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

    # SMTP_SSL Example
    server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server_ssl.ehlo() # optional, called by login()
    server_ssl.login(gmail_user, gmail_pwd)  
    # ssl server doesn't support or need tls, so don't call server_ssl.starttls() 
    server_ssl.sendmail(FROM, TO, message)
    server_ssl.close()
    # print 'successfully sent the mail'

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

def get_campground_siteids(x):
    return {
        'Angel Island State Park': angel_island_siteid_info,
        'DL Bliss State Park': dl_bliss_siteid_info,
        'Big Basin State Park': big_basin_siteid_info,
        'Yosemite Lower Pines': yosemite_lower_pines_siteid_info,
        'Yosemite Upper Pines': yosemite_upper_pines_siteid_info,
        'Yosemite North Pines': yosemite_north_pines_siteid_info,
        'Yosemite Wawona': yosemite_wawona_siteid_info,
        'Yosemite Crane Flat': yosemite_crane_flat_siteid_info,
        'Yosemite Hodgdon Meadow': yosemite_hodgdon_meadow_siteid_info,
        'Yosemite Tuolumne Meadows': yosemite_tuolumne_meadows_siteid_info,
    }.get(x, angel_island_siteid_info)

def get_campground_campsite_url_head(x):
    return {
        'Angel Island State Park': angel_island_campsite_url_head,
        'DL Bliss State Park': dl_bliss_campsite_url_head,
        'Big Basin State Park': big_basin_campsite_url_head,
        'Yosemite Lower Pines': yosemite_lower_pines_campsite_url_head,
        'Yosemite Upper Pines': yosemite_upper_pines_campsite_url_head,
        'Yosemite North Pines': yosemite_north_pines_campsite_url_head,
        'Yosemite Wawona': yosemite_wawona_campsite_url_head,
        'Yosemite Crane Flat': yosemite_crane_flat_campsite_url_head,
        'Yosemite Hodgdon Meadow': yosemite_hodgdon_meadow_campsite_url_head,
        'Yosemite Tuolumne Meadows': yosemite_tuolumne_meadows_campsite_url_head,
    }.get(x, angel_island_campsite_url_head)

def get_switch_map(x):
    return {
        'Angel Island State Park': angel_island_switch_map,
        'DL Bliss State Park': dl_bliss_switch_map,
        'Big Basin State Park': big_basin_switch_map,
        'Yosemite Lower Pines': yosemite_lower_pines_switch_map,
        'Yosemite Upper Pines': yosemite_upper_pines_switch_map,
        'Yosemite North Pines': yosemite_north_pines_switch_map,
        'Yosemite Wawona': yosemite_wawona_switch_map,
        'Yosemite Crane Flat': yosemite_crane_flat_switch_map,
        'Yosemite Hodgdon Meadow': yosemite_hodgdon_meadow_switch_map,
        'Yosemite Tuolumne Meadows': yosemite_tuolumne_meadows_switch_map,
    }.get(x, angel_island_switch_map)

def check_campground_availability(campground, d, length_of_stay):
    siteid_info = get_campground_siteids(campground)
    campsite_url_head = get_campground_campsite_url_head(campground)
    switch_map = get_switch_map(campground)

    body = ""
    subject = ""
    # extract siteid's for campground
    siteid_list = []
    for url in siteid_info:
       print url
       resp = requests.get(url,proxies=urllib.getproxies())
       soup = BeautifulSoup(resp.text,"html.parser")

       if switch_map['table_format']:
          # dig down further into the table
          soup = soup.find('table', attrs={'id':'calendar'})

       id_name = soup.find_all(attrs={'class':'sitemarker'})
       # print id_name
       for site in id_name:
          if site['id'] not in switch_map['exclude_campsites']:
             # construct url
             url = campsite_url_head + '&siteId=' + site['id'] + '&arvdate=' + d.strftime("%m/%d/%y") + '&lengthOfStay=' + str(length_of_stay)      
             # print url
             campsite_reservation_map = get_campsite_info(url, d) 
             if get_campsite_status(campsite_reservation_map, d, 1):
                subject = campground + ' - ' + 'Campsite Available!!!'
                body = body  + '\n' + d.strftime("%m/%d/%y") + ' | ' + d.strftime("%a") + ' | ' + url
                print campground + ' | ' + 'Campsite Available' + ' | ' + d.strftime("%m/%d/%y") + ' | ' + d.strftime("%a") + ' | ' + url
    if body != "" and subject != "":
        send_mail_over_ssl('bugmenot345@gmail.com', 'suzqUdd6', 'aseemm@gmail.com', subject, body)

def main():
    """Main entry point for the script"""

    # use a named tuple instead?
    input_info = [
       # May
       ["Angel Island State Park", date(2016, 5, 28)],
       ["DL Bliss State Park", date(2016, 5, 28)],
       ["Big Basin State Park", date(2016, 5, 28)],
       ["Yosemite Lower Pines", date(2016, 5, 28)],
       ["Yosemite Upper Pines", date(2016, 5, 28)],
       ["Yosemite North Pines", date(2016, 5, 28)],
       ["Yosemite Wawona", date(2016, 5, 28)],
       ["Yosemite Crane Flat", date(2016, 5, 28)],
       ["Yosemite Hodgdon Meadow", date(2016, 5, 28)],
       ["Yosemite Tuolumne Meadows", date(2016, 5, 28)],
       # June
       ### Father's Day. 6/18
       ["Angel Island State Park", date(2016, 6, 18)],
       ["Yosemite Lower Pines", date(2016, 6, 18)],
       ["Yosemite Upper Pines", date(2016, 6, 18)],
       ["Yosemite North Pines", date(2016, 6, 18)],
       # July
       ### Independence Day, 7/2
       ["DL Bliss State Park", date(2016, 7, 2)],
       # August
       ["Angel Island State Park", date(2016, 8, 6)],
       ["Angel Island State Park", date(2016, 8, 13)],
       ["Angel Island State Park", date(2016, 8, 20)],
       ["Angel Island State Park", date(2016, 8, 27)],
       ["Big Basin State Park", date(2016, 8, 6)],
       ["Big Basin State Park", date(2016, 8, 13)],
       ["Big Basin State Park", date(2016, 8, 20)],
       ["Big Basin State Park", date(2016, 8, 27)],
       # September
       ### Labor Day, 9/3
       ["Big Basin State Park", date(2016, 9, 3)],
        ]

    for entry in input_info:
       campground = entry[0]
       d = entry[1]
       length_of_stay = 1
       print "Scraping " + campground + "...for " + d.strftime("%m/%d/%y") + '...'
       check_campground_availability(campground, d, length_of_stay)

    pass

if __name__ == '__main__':
    sys.exit(main())
