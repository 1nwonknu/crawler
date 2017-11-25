#!/usr/bin/env python

import urllib.request
import queue
from bs4 import BeautifulSoup
import re
import multiprocessing

import db
import preProp
import argparse


class Crawler(db.DB, preProp.PreProcessor):

    def __init__(self, startURL, dbName = 'crawler.db'):

        db.DB.__init__(self, dbName, ())

        preProp.PreProcessor.__init__(self, '')

        self.startURL=startURL
        self.currentURL=startURL
        self.queueURL=queue.Queue()
        self.enqueueURL(self.currentURL)
        self.soup=''
        self.writeTriple=('', '', '')


    def readUrl(self):

        try:
            url = urllib.request.urlopen(self.currentURL)

            contentURL = url.read()
            self.soup = BeautifulSoup(contentURL, 'html.parser')
            return ""
        except urllib.error.HTTPError:
            print("Access denied to webpage %s. continuing with next in queue." % self.currentURL)
        except urllib.error.URLError:
            print("Not a URL: %s" %self.currentURL)
        except ValueError:
            print("Unknown URL type %s" %self.currentURL)
        finally:
            print("Unknown error %s" %self.currentURL)
        return "error"


    def setDate(self):

        date = re.search(r'\d\d[-](0[1-9]|1[012])[-](0[1-9]|[12][0-9]|3[01])', str(self.soup))
        if date != None:
            self.date = (date.group(0))
        else:
            date = re.search(r'\d\d[-](0[1-9]|1[012])[-](0[1-9]|[12][0-9]|3[01])', str(self.currentURL))
            if date != None:
                self.date = (date.group(0))


    def getUrl(self):

        for link in self.soup.find_all('a'):
            link_html = link.get('href')

            re_check = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                                  str(link_html))
            if len(re_check) > 0:
                self.enqueueURL(link_html)


    def enqueueURL(self, newURL):
        self.queueURL.put(newURL)


    def dequeueURL(self):

        if not (self.queueURL.empty()):
            self.currentURL=self.queueURL.get(0)


    def getTextURL(self):

        # kill all script and style elements
        for script in self.soup(["script", "style"]):
            script.extract()  # rip it out

        # get text
        text_total = self.soup.get_text()

        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text_total.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text


    def preProcessText(self, textURL):

        listTextURL = textURL.splitlines()
        cleanedListTextURL = []
        for text in listTextURL:
            self.setText(text)
            self.applyFilters()
            cleanedListTextURL.append(self.textURL)

        joinedText = ' '.join(cleanedListTextURL)
        return joinedText


    def crawl(self):

        while not self.queueURL.empty():
            self.date=""
            self.dequeueURL()
            if self.record_exists(): continue

            print("scrapping webpage %s" %self.currentURL)

            error = self.readUrl()
            if len(error) > 0: continue

            ## enqueue all links found on the webpage
            self.getUrl()
            self.setDate()
            textURL = self.getTextURL()

            joinedText = self.preProcessText(textURL)

            self.writeTriple=(self.currentURL, self.date, joinedText)

            ## inherited from DB supper class: write2db
            self.insert()
        print("Queue is empty.")

if __name__ == '__main__':
   

   parser = argparse.ArgumentParser()
   parser.add_argument('startURL', type=str)

   args = parser.parse_args()

   
   c = Crawler(args.startURL)

   c.crawl()





