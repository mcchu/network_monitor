##Filname: browser_monitor.py
##Class: EE554
##Authors: Michael Chu

#!/usr/bin/python

##import time
##from selenium import webdriver
##from selenium.webdriver.common.keys import Keys
##from selenium.webdriver.common.action_chains import ActionChains
##
##browser = webdriver.Firefox()
##type(browser)
##browser.get('http://google.com')
##time.sleep(5)
##timings = browser.execute_script("return window.performance.getEntries();")
##print timings

import psutil
import math
import time
import urllib2


#Function: network_info
#network_info has 6 key,object pairs
#1. Teredo Tunneling Pseud-Interface 
#2. Local Area Connection
#3. isatap.attlocal.net (or whatever ISP you have)
#4. Loopback Pseudo-Interface 1
#5. Ethernet
#6. Wi-fi
#For our network monitor, we will be using Wi-fi connection.
def network_info():
    network_info = psutil.net_io_counters(pernic=True)
    wi_fi_bw = str(network_info.get('Wi-Fi'))
    wi_fi_list = wi_fi_bw.split()

    strt_idx = wi_fi_list[0].find("bytes_sent")
    wi_fi_list[0] = wi_fi_list[0][strt_idx:]

    #print len(wi_fi_list)

    for i in range(len(wi_fi_list)):
        wi_fi_list[i] = wi_fi_list[i].replace(',','')


    print "--Network Monitoring of Wi-Fi--"
    for i in range(len(wi_fi_list)):
        print wi_fi_list[i]

#Function: browser_size
#Input: url (format must be as: 'http://www.google.com'
#Returns size of browser in Bytes
def browser_size(url):
    r = urllib2.urlopen(url)
    return len(r.read()) #prints results
    
def main():
    url_One = 'http://www.google.com'
    url_Two = 'http://www.yahoo.com'
    url_Three = 'http://www.youtube.com'
    url_Four = 'http://www.ifirstrowus.eu'

    print browser_size(url_One)
    print browser_size(url_Two)
    print browser_size(url_Three)
    print browser_size(url_Four)


main()
