from lib.utils import *
import requests
from bs4 import BeautifulSoup

class wiki():
    def __init__(self,args):
        self.tool = utils(args)
        self.setup(args)#process the arguments

    def getLinks(self,url):
        req = requests.get(url)
        soup = BeautifulSoup(req.text, "html.parser")

        #Extracting links
        list=[]
        for link in soup.find_all('a', href=True):
            href=link["href"]
            if href.startswith("/wiki/"):
                href=href.split(":")[0]
                list.append(href)

        #Cleaning duplicates
        list2=[]
        for l in list:
            if l not in list2:
                list2.append(l)
                print(l)

        return list2

    def makeUrl(self, name):
        return "https://fr.wikipedia.org/{}".format(name)

    def setup(self,args):
        if self.tool.argHasValue("-url"):
          self.url = self.tool.argValue("-url")
        else:
            print("-url is missing")
            exit(0)

    def run(self):
        print("Hey")
        print("The url is {}".format(self.url))
        self.getLinks(self.url)

    def stop(self, msg = ""):
        if msg != "": print(msg)
        exit(0)#stop the program