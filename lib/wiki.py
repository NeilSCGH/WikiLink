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

        return links

    def makeUrl(self, name):
        return "https://fr.wikipedia.org/wiki/{}".format(name)

    def setup(self,args):
        if self.tool.argHasValue("-name"):
            self.startName = self.tool.argValue("-name")
        else:
            print("-name is missing")
            exit(0)

        if self.tool.argHasValue("-d"):
            self.depth = int(self.tool.argValue("-d"))
            if self.depth < 1:
                print("-d is invalid")
                exit(0)
        else:
            print("-d is missing")
            exit(0)

        self.relations=[]

    def getPathFromName(self, name):
        for n, p in self.relations:
            if n==name:
                return p
        return ["ERROR"] #not found

    def findNameInRelations(self, name):
        for index, (n, p) in enumerate(self.relations):
            if n==name:
                return index
        return -1 #not found

    def addToRelations(self, newNames, path):
        for name in newNames:
            if name not in self.alreadyScanned:
                self.relations.append([name, path])
        #remove duplicate, simplify paths

    def run(self):
        print("Hey")
        print("The starting url is {}".format(self.makeUrl(self.startName)))

        self.relations.append([self.startName, [self.startName]])

        self.toScan = [self.startName]
        self.alreadyScanned = []

        for d in range(self.depth):
            self.alreadyScanned += self.toScan
            for name in self.toScan:
                currentPath = self.getPathFromName(name)
                newNames = self.getLinks(name)
                path = currentPath + [name]

                self.addToRelations(newNames, path)

        for a,b in self.relations: print(a,b)


    def stop(self, msg = ""):
        if msg != "": print(msg)
        exit(0)#stop the program