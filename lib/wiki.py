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
        links=[]
        for a in soup.find_all('a', href=True):
            href=a["href"]
            if href.startswith("/wiki/") and len(href)>6:
                href=href[6:]#remove the "/wiki/" part
                links.append(href)

        #Cleaning duplicates 
        links2=[]
        for l in links:
            if l not in links2:
                links2.append(l)

        #Cleaning already found links
        links3=[]
        for l in links2:
            if l not in self.foundNames:
                links3.append(l)

        return links3

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

    def run(self):
        print("Hey")
        print("The starting url is {}".format(self.makeUrl(self.startName)))

        self.relations.append([self.startName, []])

        self.toScan = [[self.startName, []]] #elements : [names, path] with path = [name1, name2, ...]
        self.relations = [] #elements : [names, path]
        self.foundNames = [] #elements : names

        for d in range(self.depth):

            #Finding new links on ToScan links
            newLinksFound=[] #elements : [names, path] 
            for name, currentPath in self.toScan:
                if currentPath==[]:
                    print("Scanning {:>50.50} -> {:<50.50} ".format(".", name),end="")
                else:
                    print("Scanning {:>50.50} -> {:<50.50} ".format(currentPath[-1], name),end="")
                newNames = self.getLinks(name)
                path = currentPath + [name]

                print("{} links found".format(len(newNames)))

                for nn in newNames:
                    newLinksFound.append([nn, path])

            #ToScan links are now "used"
            self.relations += self.toScan

            #Filtering new found links, adding them to ToScan list
            self.toScan=[]
            for name, path in newLinksFound:
                self.toScan.append([name, path])

            self.foundNames += [elem[0] for elem in self.toScan]#extract the names

        for a,b in self.relations: print(a,b)


    def stop(self, msg = ""):
        if msg != "": print(msg)
        exit(0)#stop the program