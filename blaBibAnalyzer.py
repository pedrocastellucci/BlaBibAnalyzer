
''' 
    Copyright (c) 2015 Pedro Belin Castellucci

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License version 3 as
    published by the Free Software Foundation.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

''' 
    If you use this in a publication please cite:
    Castellucci, P. B.; BlaBibAnalyzer A tool for extracting bibliographic information. (2016). 
    https://www.researchgate.net/publication/306223436_BlaBibAnalyzer_A_tool_for_extracting_bibliographic_information
 
'''

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import sys


def printSplash():
    print ('=============== BlaBibAnalyzer ===============')
    print ('= Copyright (c) 2015 Pedro Belin Castellucci =')
    print ('==============================================')


def printUsage():
    print('Correct usage is:')
    print('python blaBibAnalyzer filename.bib')


def printSeparation():
    print ('\n==================')


def pubsPerAuthor(authorsGroups):

    authorsDict = {}
    for group in authorsGroups:
        for a in group:
            if a not in authorsDict:
                authorsDict[a] = 1
            else:
                authorsDict[a] += 1

    return authorsDict


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

            if value not in yearDict:
                yearDict[value] = 1
            else:
                yearDict[value] += 1

        # Getting journal of publication:
        elif line.find('journal') >= 0:
            value = line.split('=')[1].strip()
            value = value.strip('{},')

            if value not in journalsDict:
                journalsDict[value] = 1
            else:
                journalsDict[value] += 1

    fd.close()
    return authorsGroup, yearDict, journalsDict


def plotBarPerYear(yearDict):
    x = []
    y = []
    print ('Year\tPublications')
    for year, count in yearDict.items():
        x.append(int(year))
        y.append(int(count))
        print ('%d\t%d' % (int(year), int(count)))

    x = np.array(x)
    y = np.array(y)

    barWidth = 0.75
    plt.xticks(range(min(x), max(x)+1), rotation='vertical', fontsize=20)
    plt.yticks(range(min(y) - 1, max(y)+2), fontsize=30)

    plt.xlim(min(x) - 0.5, max(x) + 0.5)
    plt.ylim(0, max(y) + 0.5)

    plt.ylabel('Number of publications', fontsize=30)
    plt.gca().yaxis.grid(True)
    plt.bar(x - barWidth/2.0, y, barWidth, color='black')  # Black bars
    plt.show()


def printAuthorsCounts(authorsDict):

    print ('Last name, First name \t Publications')

    sortedAuthorsCount = authorsDict.items()
    sortedAuthorsCount = sorted(
        sortedAuthorsCount, key=lambda x: x[1], reverse=True)

    for i, j in sortedAuthorsCount:
        names = i.split(',')
        print ('%s, %s\t%d' % (names[0].strip(), names[1].strip()[0], j))


def printJournalsCount(journalsDict):

    print ('Journal \t Publications')

    sortedList = journalsDict.items()
    sortedList = sorted(sortedList, key=lambda x: int(x[1]), reverse=True)

    for i, j in sortedList:
        print ('%s\t%d' % (i, int(j)))


def plotCollaborationGraph(authorsGroups):

    authors = []
    for group in authorsGroups:
        for a in group:
            authors.append(a)

    authors = list(set(authors))
    authors = sorted(authors, key=str.upper)

    count = 1
    labels = {}

    for a in authors:
        labels[a] = count
        count += 1

    collaborators = nx.Graph()
    for group in authorsGroups:
        if len(group) == 1:
            collaborators.add_node(labels[group[0]])
        else:
            for i, a1 in enumerate(group):
                if i + 1 < len(group):
                    for a2 in group[i+1:]:
                        collaborators.add_edge(labels[a1], labels[a2])

    try:
        pos = nx.pygraphviz_layout(collaborators)
    except AttributeError:
        print ('You may have a problem with graphviz.'
               'Using random layout for the graph -- '
               'which will probably be bad.')

        pos = nx.random_layout(collaborators)

    minPublications = min(authorsDict.values())
    maxPublications = max(authorsDict.values())
    pubsAmplitude = maxPublications - minPublications
    minNodeSize = 250
    maxNodeSize = 800
    sizeAmplitude = (maxNodeSize - minNodeSize)

    nodeSizes = [0]*len(collaborators.nodes())
    for a in authors:
        nodeSizes[labels[a]-1] = sizeAmplitude*(
            authorsDict[a] - minPublications)/(pubsAmplitude) + minNodeSize

    nx.draw_networkx_nodes(
        collaborators, pos, node_size=nodeSizes, node_color='w')

    nx.draw_networkx_edges(collaborators, pos)
    nx.draw_networkx_labels(collaborators, pos, fontsize=30)

    print('Last name, First name \t Number in graph')
    for x in authors:
        names = x.split(',')
        print ('%s, %s \t %d' % (
            names[0].strip(), names[1].strip()[0], labels[x]))

    plt.axis('off')
    plt.show()


if __name__ == '__main__':

    printSplash()
    if len(sys.argv) != 2:
        printUsage()
        exit(0)
    else:
        filename = sys.argv[1]

    authorsGroups, yearDict, journalsDict = processBibFile(filename)
    authorsDict = pubsPerAuthor(authorsGroups)

    printAuthorsCounts(authorsDict)
    printSeparation()
    printJournalsCount(journalsDict)
    printSeparation()

    plotBarPerYear(yearDict)
    printSeparation()
    plotCollaborationGraph(authorsGroups)
