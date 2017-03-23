#!/usr/bin/python

import time
import urllib2
import os
import re
import selenium.webdriver as webdriver
from random import randint
from __builtin__ import str
from timeout import timeout

THRESHOLD = 5
FILEHANDLE = None
fileOpened = False

adwareList = ["www.liveadexchanger.com",
              ]

localhostString = "127.0.0.1"
TERMINATEPAGELIST = []
URLLIST = []
task1Period = 3
task2Period = 3
task3Period = 3
task4Period = 3

def downloadWebpage(urlString):
    
    response = urllib2.urlopen(urlString)
    htmlSource = response.read()
    
    return htmlSource

def launchWebpage(webdriver, htmlCode, htmlFileName):
    
    global FILEHANDLE, fileOpened
    
    htmlFileName += '.html'
    path = os.path.abspath(htmlFileName)
    url = 'file://' + path
    print "Creating htmlfile with filename: " + url
    
    fileOpened = True
    with open(path, 'w') as FILEHANDLE:
        FILEHANDLE.write(htmlCode)
        
    webdriver.execute_script("window.open('','_blank');")
    webdriver.switch_to.window(webdriver.window_handles[-1])
    webdriver.get(url)
    FILEHANDLE.close()
    fileOpened = False

def bandwidthAnalyzer(URLLIST):
    
    bandWidthList = []
    
    for URL in URLLIST:
        bandwidth = randint(0, 10)
        bandWidthList.append((URL, bandwidth))
        print URL + ": " + str(bandwidth)
    
    return bandWidthList        
        
##### end of bandwidthAnalyzer() ########

def getCurrentURLs(webDriver):
    
    for windowHandle in webDriver.window_handles:
        webDriver.switch_to.window(windowHandle)
        print webDriver.current_url
        URLLIST.append(webDriver.current_url)

##### end of getCurrentURLs() ########

def codeOptimization(URL):
    
    htmlSource = downloadWebpage(URL)
    
    for adware in adwareList:
        htmlSource = htmlSource.replace(adware, localhostString)
    
    return htmlSource

##### end of codeOptimization() ########

def task4(webDriver):

    global FILEHANDLE, fileOpened
    
    # Return handle to the last opened tab
    print "Returning handle to last opened tab"
    webDriver.switch_to.window(webDriver.window_handles[-1])
    
    #clear any previous list
    while len(URLLIST) > 0 : URLLIST.pop()
    
    #clear any previous list
    while len(URLLIST) > 0 : TERMINATEPAGELIST.pop()
    
    #close file handler if left opened
    if fileOpened: FILEHANDLE.close()

    
##### end of task4() ########            
    
def task3(webDriver):

    '''
        Match any website on terminatePageList with a website
        name on URLLIST and when a match is found terminate that
        webpage by closing the handle on the webDriver
    '''  
    
    terminatePagesListLength = len(TERMINATEPAGELIST)
    URLlistLength = len(URLLIST)
    y = 0
    
    print "Terminating webpages:"
    
    while y < terminatePagesListLength:
        i = 0
        breakFlag = False
        while i < URLlistLength:
            if TERMINATEPAGELIST[y] == URLLIST[i]:
                terminatePage = TERMINATEPAGELIST.pop(y)
                URLLIST.pop(i)
                #since we removed an item from TERMINATEPAGELIST, we need to adjust the offset
                terminatePagesListLength = len(TERMINATEPAGELIST)
                URLlistLength = len(URLLIST)   
                print "Closing webpage: " + terminatePage
                webDriver.switch_to.window(webDriver.window_handles[i])
                webDriver.close()
                breakFlag = True
                break
            
            i += 1
        
        if breakFlag == True:
            continue
        
        print "NO MATCH FOUND"
        y += 1
          
    
##### end of task3() ######## 

def task2(webDriver):
    
    for URL in TERMINATEPAGELIST:
        print "Trying optimizing URL: " + URL
        
        if re.match("^file:", URL):
            print "It has been optimized before"  
        else:
            print "It has not been optimized before"
            print "Optimizing URL"
            htmlSource = codeOptimization(URL)
            regexMatched = re.search("^https?://.+?\.(.+?)\..+?/", URL)
            htmlFileName = regexMatched.group(1)
            print "Webpage name: " + htmlFileName
            launchWebpage(webDriver, htmlSource, htmlFileName)


##### end of task2() ########       

def task1(webDriver):
    
    print "Getting current URLs:"
    getCurrentURLs(webDriver)
    print 
    print "Getting bandwidth for each URL:"
    webPagesBandwidths = bandwidthAnalyzer(URLLIST)
    print
    
    print "Analizing URLs:"
    for i in range(len(webPagesBandwidths)):        
        URL = webPagesBandwidths[i][0]
        webPageBandwidth = webPagesBandwidths[i][1]
        
        # Skip the first blank tab
        if URL == "about:blank" or URL == "about:newtab":
            continue
        
        print "Analizing URL: " + URL + " Bandwidth: " + str(webPageBandwidth)
        
        if webPageBandwidth <= THRESHOLD:
            print "Below or equal to theshold: CONTINUE"
            continue
        
        # If website is above THRESHOLD, add it to list
        print "Adding to TERMINATEPAGELIST"
        TERMINATEPAGELIST.append(URL)    
            
    print "Analizis finished\n"    
        

##### end of task1() ########


def envSetup():
    
    
    #fp = webdriver.FirefoxProfile('C:\\Users\\skyin\\Google Drive\\USC workspace\\Network_Scanner\\vbifylkm.NetworkScannerProfile')
    #fp = webdriver.FirefoxProfile('C:\\Users\\skyin\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\lip2ulf1.default')
    #fp.set_preference("browser.sessionstore.enabled", "enable")
    #driver = webdriver.Firefox(fp)
    driver = webdriver.Firefox()
    driver.execute_script("window.open('','_blank');")
    
    return driver

##### end of envSetup() ########

def debug(webdriver):
    
    webdriver.switch_to.window(webdriver.window_handles[-1])
    webdriver.get("http://www.isi.edu/~pedro/")
    
    webdriver.execute_script("window.open('','_blank');")
    webdriver.switch_to.window(webdriver.window_handles[-1])
    webdriver.get("http://www-classes.usc.edu/engr/ee-s/477p/")
    
    webdriver.execute_script("window.open('','_blank');")
    webdriver.switch_to.window(webdriver.window_handles[-1])
    webdriver.get("https://www.google.com/")
    
    webdriver.execute_script("window.open('','_blank');")
    webdriver.switch_to.window(webdriver.window_handles[-1])
    webdriver.get("http://www.tv-porinternet.com/")


def main():
    
    firefoxDriver = envSetup()
    # DEBUGGING ONLY
    debug(firefoxDriver)
    
    while (True):
        periodStart = time.time()
        
        
        # Task 1: Determine what websites to close or optimize depending on bandwidth
        print "TASK 1:"
        taskStart = time.time()
        task1(firefoxDriver)
        taskPeriod = time.time() - taskStart
        print "Task 1 period: " + str(taskPeriod)
        print 
        
        # Task 2: Try to optimize websites
        print "TASK 2:"
        taskStart = time.time()
        task2(firefoxDriver)
        taskPeriod = time.time() - taskStart
        print "Task 2 period: " + str(taskPeriod)
        print  
        
        # Task 3: Close websites
        print "TASK 3:"
        taskStart = time.time()
        task3(firefoxDriver)
        taskPeriod = time.time() - taskStart
        print "Task 3 period: " + str(taskPeriod)
        print
        
        # Task 4: Cleanup in case of deadline misses
        print "TASK 4:"
        taskStart = time.time()
        task4(firefoxDriver)
        taskPeriod = time.time() - taskStart
        print "Task 4 period: " + str(taskPeriod)
        print

        
        periodEnd = time.time()
        
        actualPeriod = periodEnd - periodStart
        print "Actual Period: " + str(actualPeriod)
        print "\n"
        
#         numIn = raw_input("Command: ")
#         if int(numIn) == 0:
#             break
        time.sleep(3)        

##### LOOP AND NEVER RETURN ######    
    
def test4():
    print FILEHANDLE

@timeout(2)
def test():
    #print FILEHANDLE
    time.sleep(3)
    
@timeout(3)
def test2():
    time.sleep(8)
        

if __name__ == "__main__":
    main()
    
    
    # implementation to make a task timeout 
    while (1):
        timeStart = time.time()  
             
        try:
            taskStart = time.time() 
            test()
            taskTime = time.time()  - taskStart
            taskDifference = 5 - taskTime
            if (taskDifference > 0):
                time.sleep(taskDifference)
        except:
            pass
        
        
        try:
            taskStart = time.time()
            test2()
            taskTime = time.time() - taskStart
            taskDifference = 5 - taskTime
            if (taskDifference > 0):
                time.sleep(taskDifference)
        except:
            pass
        
        timeEnd = time.time()
        cycleTime = timeEnd - timeStart
        print "Cycle finished in: " + str(cycleTime)
    
    
    
