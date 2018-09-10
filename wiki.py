import sys
from time import sleep
from random import randint

from requests import get
from bs4 import BeautifulSoup


class Node:
    def __init__(self, link, d):
        self.depth = d  # shows on which level of the tree is the node
        self.link = link  # stores Wikipedia link
        self.words = []  # stores the words that are going to be displayed in the graph
        self.subnodes = []  # stores all subnodes

        if d <= 2:  # explores only until level 2 (so we technically have 3 levels)
            self.explore()

    def explore(self):
        sleep(randint(1, 5))  # prevents overloading the server
        url = 'https://en.wikipedia.org'
        response = get(url + self.link)
        soup = BeautifulSoup(response.text, 'lxml')

        tags = soup.body.find('div', class_='mw-parser-output').find('p', class_=None, recursive=False).find_all('a')
        self.subnodes = [Node(tag['href'], self.depth + 1) for tag in tags if tag.parent.name == 'p']
        self.words = [tag.text.lower() for tag in tags if tag.parent.name == 'p']
        print(self.words)


if __name__ == '__main__':
    n = Node('/wiki/' + sys.argv[1], 1)
