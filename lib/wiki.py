from lib.utils import *
import requests
from bs4 import BeautifulSoup

class wiki():
    def __init__(self,args):
        self.tool = utils(args)
        self.setup(args)#process the arguments

    def getLinks(self,name):
        url = self.makeUrl(name)
        req = requests.get(url)
        soup = BeautifulSoup(req.text, "html.parser")

        #Extracting links
        list=[]
        for a in soup.find_all('a', href=True):
            href=a["href"]
            if href.startswith("/wiki/") and len(href)>6:
                href=href[6:]#remove the "/wiki/" part
                list.append(href)

        #Cleaning duplicates
        links=[]
        for l in list:
            if l not in links:
                links.append(l)
                print(l)

        return links

    def makeUrl(self, name):
        return "https://fr.wikipedia.org/wiki/{}".format(name)

    def setup(self,args):
        if self.tool.argHasValue("-name"):
          self.name = self.tool.argValue("-name")
        else:
            print("-name is missing")
            exit(0)

    def run(self):
        print("Hey")
        print("The starting url is {}".format(self.makeUrl(self.name)))
        self.getLinks(self.name)

    def stop(self, msg = ""):
        if msg != "": print(msg)
        exit(0)#stop the program