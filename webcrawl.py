#!/usr/local/bin/python

'''
    DESCRIPTION: This program crawl and save web links into a database for further analysis
    
    Created:    Jul 17, 2015
    Modified:   Aug 21, 2015

    authors:    Nguyen Ngoc Lan
                Tran Thanh Liem
'''

import requests
from requests import ConnectionError
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import MySQLdb
import sys


#===========================================================================================
# DESCRIPTION: Suppress empty spaces from strings.
#===========================================================================================
def TrimString(s): return " ".join(s.split())
    

#===========================================================================================
# DESCRIPTION: Insert elements of the list 'recordList' into the 'webs1' DB.
#===========================================================================================
def Insert2DB(recordList):
    # Open DB connection to insert the list of records
    db = MySQLdb.connect("localhost", "testuser", "test123", "weblinks")
    if db is not None:
        with db:    # the 'with' keyword provides error handling and permits
                    # the python interpreter to release automatically resources
            
            # Prepare a cursor object using cursor() method
            cursor = db.cursor();
        
            # determine the maximum buffer size (in byte) for bulk insert 
            sqlCmd = "SELECT @@bulk_insert_buffer_size;"
            cursor.execute(sqlCmd)
            bufferSize = cursor.fetchone()
            bufferSize = int(bufferSize[0])

            # determine each tuple size (in byte)
            tupleSize = sys.getsizeof(recordList[0])
            
            # determine the maximum number of tuples per batch
            nbTuplePerBatch = bufferSize / tupleSize
        
            # bulk insertion of tuples (per batch)
            sqlCmd = "INSERT INTO webs1 (title, url, meta, description) VALUES(%s, %s, %s, %s)"
            for i in range(0, len(recordList), nbTuplePerBatch):
                batchList = recordList[i:i+nbTuplePerBatch]
                cursor.executemany(sqlCmd, batchList)
                db.commit() # commit the changes in the DB
        
        # Disconnect from Server
        db.close();
    else:
        print "Unable to log into Database\n";


#===========================================================================================
# DESCRIPTION: Extract the title, metadata and link addresses from the specified link 'url'.
#              This function processes recursively the same operation for each child links
#              until the 'maxLevels' is reached.
# INPUTS:    - url : starting url
#            - maxLevels : number of levels to go down
# OUTPUT:    - linksList : list of urls found from the crawl
#===========================================================================================
def crawlAll(url, maxLevels, linksList):
    
    global fail, success, recnum

    if (maxLevels == 0):
        return fail
    
    # Defer downloading the response's body until response.content is accessed
    try:
        response = requests.get(url, stream=True)
    except ConnectionError:
        print ("ConnectionError for url: %s" %url)
        return fail
        
    if (response.status_code != requests.codes.ok):
        return fail
    
    # Scrape the website
    only_head_tag = SoupStrainer('head')
    soup = BeautifulSoup(response.text, "html.parser", parse_only=only_head_tag)
    if soup.title is not None:
        pageTitle = unicode(soup.title.string)
    else:
        # TODO: INSERT CASE TO EXTRACT THE TITLE FROM PDF LINKS!!!
        pageTitle = 'emptyTitle!'

    # Record this link
    url_utf8 = url.encode('utf-8')
    title_utf8 = TrimString(pageTitle).encode('utf-8')
    meta_utf8 = 'metadata_go_here'
    desc_utf8 = 'description_go_here'
    currentPage = (title_utf8, url_utf8, meta_utf8, desc_utf8)
    
    # Test for empty list and existing links and eventually save the extracted infos to the list
    if not linksList or not any(url_utf8 in d for d in linksList):
        recnum += 1
        print "saving record_%d: %s..." % (recnum, url)
        linksList.append(currentPage)
    else:
        print "the url %s exist!" % url
        return fail # no need to go further since this url is has already been crawled
    
     
    # Create a SoupStrainer for parsing only <a> tags with an href attribute
    # and pass it to BeautifulSoup
    only_a_tag_with_href = SoupStrainer('a', href=True)
    soup = BeautifulSoup(response.text, "html.parser", parse_only=only_a_tag_with_href)
    
    
    # Repeat recursively the process for all valid urls from this page
    for link in soup:
        if link['href']=='' or link['href'].startswith('#'): continue;
        if 'http' in link['href']: # eliminate internal links. Only absolute links are considered
            crawlAll(link['href'], maxLevels-1, linksList)
    return success

#
# MAIN PROGRAM
#        

fail, success, recnum = False, True, 0
linksList = []
testURL = 'http://www.lapresse.ca/'
# apdfURL = 'http://www.emis.de/journals/IJOPCM/files/IJOPCM(vol.1.2.3.S.8).pdf'

# Crawl the initial url and save all the links found to a list
crawlres = crawlAll(testURL, 2, linksList)


# Save the list found into DB
if crawlres==success:
    Insert2DB(linksList)
    print "%d records have been inserted into %s table." % (len(linksList), 'webs1')
else:
    print "unable to scrape the specified initial link: %d" % testURL
