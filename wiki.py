import sys
from time import sleep
from random import randint

from requests import get
from bs4 import BeautifulSoup

import pydot

class Node:
    def __init__(self, link, d, parent):
        self.name = link.split('/')[-1].replace("_", " ")
        self.depth = d  # shows on which level of the tree is the node
        self.link = link  # stores Wikipedia link
        self.words = []  # stores the words that are going to be displayed in the graph
        self.subnodes = []  # stores all subnodes
        self.parent = parent

        if d <= 3:  # explores only until level 2 (so we technically have 3 levels)
            self.explore()

    def explore(self):
        sleep(randint(3, 7))  # prevents overloading the server
        try:
            url = 'https://en.wikipedia.org'
            response = get(url + self.link)
            soup = BeautifulSoup(response.text, 'html.parser')

            tags = soup.body.find('div', class_='mw-parser-output').find('p', class_=None, recursive=False).find_all('a')
            self.subnodes = [Node(tag['href'], self.depth + 1, self) for tag in tags if tag.parent.name == 'p']
            self.words = [tag.text.lower() for tag in tags if tag.parent.name == 'p']
            print(self.words)

            if self.depth is not 1:
                draw(self.parent.name, self.name)
        except Exception:
            print("Error4e", self.name)


def draw(parent, me):
    edge = pydot.Edge(parent, me)
    graph.add_edge(edge)

if __name__ == '__main__':
    graph = pydot.Dot(graph_type='graph')
    n = Node('/wiki/' + sys.argv[1], 1, None)
    graph.write_png('example1_graph.png')
