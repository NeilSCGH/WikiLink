from lib.utils import *
import requests
from bs4 import BeautifulSoup

class wiki():
    def __init__(self,args):
        self.utils = utils(args)
        self.setup(args)#process the arguments

    def setup(self,args):
        if self.utils.argExist("-h") or self.utils.argExist("-help") or self.utils.argExist("-?"):
            self.help()
            exit(0)

        if self.utils.argHasValue("-start"):
            self.startName = self.utils.argValue("-start")
        else:
            print("-start is missing")
            self.help()
            exit(0)

        if self.utils.argHasValue("-d"):
            self.depth = int(self.utils.argValue("-d"))
            if self.depth < 1:
                print("-d is invalid")
                self.help()
                exit(0)
        else:
            print("-d is missing")
            self.help()
            exit(0)

        self.endName=""
        if self.utils.argHasValue("-end"):
            self.endName = (self.utils.argValue("-end")).lower()

        self.max=0
        if self.utils.argHasValue("-max"):
            self.max = int(self.utils.argValue("-max"))
            if self.max < 1:
                print("-max is invalid")                
                self.help()
                exit(0)

        self.noTech = self.utils.argExist("-noTech")



        self.relations=[[self.startName, []]]

        self.toScan = [[self.startName, []]] #elements : [names, path] with path = [name1, name2, ...]
        self.relations = [] #elements : [names, path]
        self.foundNames = [] #elements : names

    def help(self):
        print()
        print("Usage: python wikilink.py -start start_name -end end_name")
        print("                          -d depth [-max count] [-noTech]")
        print("                          [[-h] | [-help] | [-?]]")
        print()
        print("Options:")
        print("   -start start_name  The starting name page.")
        print("   -end end_name      The target name page.")
        print("                      If not set, will reach the depth provided using -d, then stop.")
        print("   -d depth           The maximum allowed depth to scan.")
        print("   -max count         (Optional) The maximum number of links to extract from each page.")
        print("   -noTech            (Optional) Exclude technical pages (containing \":\" in the name).")
        print("   -h|help|?          (Optional) Print this help.")

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

        if self.noTech: #remove names containing ":"
            links4=[]
            for l in links3:
                if ":" not in l:
                    links4.append(l)
            links3 = links4[:]

        if self.max>0:
            links3=links3[:self.max]

        return links3

    def makeUrl(self, name):
        return "https://fr.wikipedia.org/wiki/{}".format(name)

    def run(self):
        print("Hey")
        print("The starting url is {}".format(self.makeUrl(self.startName)))
        print("The target name is {}".format(self.endName))

        for d in range(self.depth):

            print()
            print("#"*101)
            print("{0} Depth {1:>2}/{2:<2} {0}".format("#"*44, d+1, self.depth))
            print("#"*101)

            #Finding new links on ToScan links
            newLinksFound=[] #elements : [names, path] 
            n=len(self.toScan)
            for index, (name, currentPath) in enumerate(self.toScan):
                if currentPath==[]:
                    print("Scanning {:>50.50} -> {:<50.50} ".format(".", name),end="")
                else:
                    currentName = "{} ({:}/{})".format(currentPath[-1],index+1, n)
                    print("Scanning {:>50.50} -> {:<50.50} ".format(currentName, name),end="")
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
                if name.lower()==self.endName:
                    print("\nFOUND !!!")
                    for p in path:
                        print("{} -> ".format(p), end="")
                    print(self.endName)

                    exit(0)

                self.toScan.append([name, path])

            self.foundNames += [elem[0] for elem in self.toScan]#extract the names

        for a,b in self.relations: print(b,a)


    def stop(self, msg = ""):
        if msg != "": print(msg)
        exit(0)#stop the program