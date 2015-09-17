import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

def processBibFile(filename):

    authorsGroup = []
    yearDict = {}
    journalsDict = {}
    
    fd = open(filename)

    for line in fd:

        # Getting authors:
        if line.find('author') >= 0:
            value = line.split('=')[1].strip()
            value = value.strip('{},')

            authors = value.split(' and ')
            for i, a in enumerate(authors):
                authors[i] = a.strip()

            authorsGroup.append(authors)

        # Getting year of publication:
        elif line.find('year') >= 0:
            value = line.split('=')[1].strip()
            value = value.strip('{},')

            if not value in yearDict:
                yearDict[value] = 1
            else:
                yearDict[value] += 1

        # Getting journal of publication:
        elif line.find('journal') >= 0:
            value = line.split('=')[1].strip()
            value = value.strip('{},')

            if not value in journalsDict:
                journalsDict[value] = 1
            else:
                journalsDict[value] += 1
        
    fd.close()
    return authorsGroup, yearDict, journalsDict

    
filename = 'test.bib'

authorsGroups, yearDict, journalsDict = processBibFile(filename)

for i in sorted(authorsGroups):
    print i

for i, j in journalsDict.iteritems():
    print i, j

x = []
y = []
for year, count in yearDict.iteritems():
    x.append(int(year))
    y.append(int(count))
    print year, count

#fig, ax = plt.subplots()
#rects1 = plt.bar(x, y)
#plt.show()

labels = {}
collaborators = nx.Graph()
for group in authorsGroups:
    print len(group)
    if len(group) == 1:
        collaborators.add_node(group[0])
        labels[group[0]] = unicode(group[0][:2])
    else:
        for i, a1 in enumerate(group):
            if i + 1 < len(group):
                for a2 in group[i+1:]:
                    collaborators.add_edge(a1, a2)
                    labels[a1] = unicode(a1[:2])
                    labels[a2] = unicode(a2[:2])

pos = nx.spring_layout(collaborators, k=0.4, scale=10)
nx.draw_networkx_nodes(collaborators, pos, node_size=300)
nx.draw_networkx_edges(collaborators, pos)
nx.draw_networkx_labels(collaborators, pos, labels=labels)

#nx.draw(collaborators, pos)
plt.show()


