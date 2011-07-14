import sys
import re
import urllib.request, urllib.error, urllib.parse
import urllib.parse


class Node():
        def __init__(self,url):
                self.url = url
                self.visited = False
                self.edges = []
                self.previsit = 0
                self.postvisit = 0
                self.ccnum = 0

class Clock():
        def __init__(self):
                self.time = 1

clock = Clock()
ccclock = Clock()
ccclock.time = 0

def graphstats(scc_dict,comp_dict):
        numNodes = 0
        numEdges = 0
        numSCC = len(scc_dict)
        for entry in comp_dict:
                numNodes += len(comp_dict[entry])
                for n in comp_dict[entry]:
                        numEdges += len(comp_dict[entry][n])
        density = numEdges/float(numNodes)
        print ("NumNodes: \t", numNodes)
        print ("Density: \t", density)
        print ("NumSCC: \t", numSCC)
        maxSCC = 0

        for x in comp_dict:
                minSCC = len(comp_dict[x])
                for y in comp_dict[x]:
                        minOut = len(comp_dict[x][y])
                        break
                break
                
        totalSCC = 0
        sccLens = []
        maxOut = 0
        outLens = []
        totalOut = 0
        for entry in comp_dict:
                currNum = len(comp_dict[entry])
                sccLens.append(currNum)
                totalSCC +=currNum
                if currNum > maxSCC:
                        maxSCC = currNum
                if currNum < minSCC:
                        minSCC = currNum

                for n in comp_dict[entry]:
                        curr = len(comp_dict[entry][n])
                        outLens.append(curr)
                        totalOut += curr
                        if curr > maxOut:
                                maxOut = curr
                        if curr < minOut:
                                minOut = curr
                                
        medSCC = sccLens[len(sccLens)//2]
        meanSCC = (totalSCC/float(numSCC))
        print ("MinSCC: \t", minSCC)
        print ("MaxSCC: \t", maxSCC)
        print ("MedSCC: \t", medSCC)
        print ("MeanSCC: \t", meanSCC)

        medOut = outLens[len(outLens)//2]
        meanOut = (totalOut/float(numNodes))
        print ("MinOut/In: \t", minOut)
        print ("MaxOut/In: \t", maxOut)
        print ("MedOut/In: \t", medOut)
        print ("MeanOut/In: \t", meanOut)

        
                
      
        

def graphReverse(G):
        reverse = {}
        reverse["None"] = []
        for url in G:
                if G[url] == []:
                        reverse["None"] += [url]
                else:
                        for item in G[url]:
                                item = item[1]
                                if item in reverse:
                                        reverse[item] += [url]
                                else:
                                        reverse[item] = [url]
        return reverse

def stronglyConnectedComponents(G):
        reverseG = graphReverse(G)
        verteces = dfsReverse(reverseG)
        verteces = dfs(verteces)
        scc_dict = {}
        comp_dict = {}

        # again i know this is horribly inefficient, I just cannot find a better way with the structure i have
        for vertex in verteces:
                if vertex.ccnum not in scc_dict:
                        scc_dict[vertex.ccnum] = dict()
                if vertex.ccnum not in comp_dict:
                        comp_dict[vertex.ccnum] = dict()
                comp_dict[vertex.ccnum][vertex.url] = []
                for edge in G[vertex.url]:
                        if type(edge) == type(()):
                                edge = edge[1]
                        comp_dict[vertex.ccnum][vertex.url] += [edge]       
                        for i in range(len(verteces)):
                                v = verteces[i]
                                if edge == v.url:
                                        if v.ccnum !=  vertex.ccnum:
                                                if v.ccnum not in scc_dict[vertex.ccnum]:
                                                        scc_dict[vertex.ccnum][v.ccnum] = []
                                                scc_dict[vertex.ccnum][v.ccnum] += [(vertex.url, v.url)]
                                                
        return (scc_dict, comp_dict)
                       
        

def dfs(verteces):

        
        verteces.sort(key=lambda vertex: vertex.postvisit)
        for vertex in verteces:
                vertex.visited = False
        for i in range(len(verteces)):
                vertex = verteces[i]
                if vertex.url == 'None':
                       verteces.remove(vertex) 
                elif vertex.visited == False:
                        ccclock.time += 1
                        verteces = explore(verteces,vertex)

        return verteces

def dfsReverse(G):
        # only difference is that this doesn't update the ccclock time
        vertexUrls = G.keys()
        verteces  = []
        for url in vertexUrls:
                vertex = Node(url)
                vertex.edges += G[url]
                verteces.append(vertex)
        for i in range(len(verteces)):
                vertex = verteces[i]
                if vertex.visited == False:
                        verteces = explore(verteces,vertex)

        return verteces    

def explore(verteces,v):
        
        v.visited = True
        v.ccnum = ccclock.time
        v.previsit = clock.time
        clock.time += 1
        ## I know that this double loop is inefficient but I could not think of another way to work with the combinations of url strings and node information
        if len(v.edges) > 0:
                for edge in v.edges:
                        if type(edge) == type(()):
                                edge = edge[1]
                        for i in range(len(verteces)):
                                vertex = verteces[i]
                                if edge == vertex.url:
                                        if vertex.visited == False:
                                                verteces = explore(verteces,vertex)

        v.postvisit = clock.time
        clock.time += 1
        return verteces
        
def webcrawl(url, maxdepth=10, domain=True):
        crawled = {url:[]}
        graph = webcrawlhelper2(url,0,maxdepth,domain,crawled)
        return(stronglyConnectedComponents(graph))
        
def webcrawlhelper2(url, depth, maxdepth, domain,crawled):
        if url not in crawled:
                crawled[url] = []
        depth+=1
        nextlinks = webcrawlhelper(url, domain)
        while len(nextlinks) > 0 and depth <= maxdepth:
                url2 = nextlinks.pop()
                if (url,url2) not in crawled[url] and url2 != url:
                        crawled[url].append((url,url2))
                        webcrawlhelper2(url2,depth,maxdepth,domain,crawled)
        return crawled

def webcrawlhelper(urlBegin,domain=True):
        tocrawl = set([urlBegin])
        linkregex = re.compile('<a\s*href=[\'|"](.*?)[\'"].*?>')
        
        try:
                crawling = tocrawl.pop()
        except KeyError:
                return tocrawl
        url = urllib.parse.urlparse(crawling)
        root = urllib.parse.urlparse(urlBegin).netloc

        
        try:
                response = urllib.request.urlopen(crawling)
        except:
                return tocrawl
        msg = str(response.read(), "utf-8", errors = "replace")
        startPos = msg.find('<title>')
        if startPos != -1:
                endPos = msg.find('</title>', startPos+7)
                if endPos != -1:
                        title = msg[startPos+7:endPos]
        links = linkregex.findall(msg)
        
        for link in (links.pop(0) for _ in range(len(links))):
                if link.startswith('..'):
                        link = link[3:]
                if link.startswith('/'):
                        link = 'http://' + url[1] + link
                elif link.startswith('#'):
                        link = 'http://' + url[1] + url[2] + link
                elif not link.startswith('http'):
                        link = 'http://' + url[1] + '/' + link

                site = urllib.parse.urlparse(link).netloc
                if (domain == False or site == root):
                        tocrawl.add(link)
                print (link)
        return tocrawl

def main():
        url = input("Please enter a url: ")
        maxDepth = eval(input("Please enter max depth: "))
        domain = input("Stay within domain? (y/n) ").upper() == 'Y'
        
        f = open("output.txt", "w")
        originalOut = sys.stdout
        sys.stdout = f
        result  = webcrawl(url,maxDepth,domain)
        graphstats(result[0],result[1])
        print ("\nscc_dict: \n\n", result[0], "\n\ncomp_dict: \n\n", result[1])

        sys.stdout = originalOut
        f.close()

if __name__=='__main__':
    main()
