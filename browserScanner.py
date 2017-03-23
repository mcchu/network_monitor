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
task2Period = 1
task3Period = 1
task4Period = 1

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

@timeout(task4Period)
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

@timeout(task3Period)    
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

@timeout(task2Period)
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


@timeout(task1Period)
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
    
    
##### end of debug() ########
    
    
def adjustTaskTime(taskperiod, taskStartTime):
    
    actualTaskTime = time.time()  - taskStartTime
    print "Actual period: " + str(actualTaskTime)
    taskTimeRemaining = taskperiod - actualTaskTime
    if (taskTimeRemaining > 0):
        time.sleep(taskTimeRemaining)
        
##### end of adjustTaskTime() ########


def main():
    
    firefoxDriver = envSetup()
    # DEBUGGING ONLY
    debug(firefoxDriver)
    
    while (True):
        periodStart = time.time()
        
        
        # Task 1: Determine what websites to close or optimize depending on bandwidth
        print "TASK 1:"
        taskStart = time.time()
        missedDeadline = False
        try:
            task1(firefoxDriver)
        except:
            missedDeadline = True
            print "SOFTMISSED: missed deadline"
            
        adjustTaskTime(task1Period, taskStart)
        taskPeriod = time.time() - taskStart
        print "Task 1 period: " + str(taskPeriod)
        print 
        
        # Task 2: Try to optimize websites
        print "TASK 2:"
        taskStart = time.time()
        missedDeadline = False
        try:
            task2(firefoxDriver)
        except:
            missedDeadline = True
            print "SOFTMISSED: missed deadline"
            
        adjustTaskTime(task2Period, taskStart) 
        taskPeriod = time.time() - taskStart
        print "Task 2 period: " + str(taskPeriod)
        print  
        
        # Task 3: Close websites
        print "TASK 3:"
        taskStart = time.time()
        missedDeadline = False
        try:
            task3(firefoxDriver)
        except:
            missedDeadline = True
            print "SOFTMISSED: missed deadline"
            
        adjustTaskTime(task3Period, taskStart)
        taskPeriod = time.time() - taskStart
        print "Task 3 period: " + str(taskPeriod)
        print
        
        # Task 4: Cleanup in case of deadline misses
        print "TASK 4:"
        taskStart = time.time()
        missedDeadline = False
        try:
            task4(firefoxDriver)
        except:
            missedDeadline = True
            print "SOFTMISSED: missed deadline"
            
        adjustTaskTime(task4Period, taskStart)
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

##### LOOP AND NEVER RETURN ######    
        

if __name__ == "__main__":
    main()
    
    
    
