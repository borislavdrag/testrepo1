from bs4 import BeautifulSoup
from requests import get

import sys
from time import sleep
from random import randint


class Node:
    def __init__(self, link, d):
        self.link = link
        self.subnodes = []
        self.words = []
        self.depth = d

        if d <= 2:
            self.explore()
    def explore(self):
        sleep(randint(1, 5))
        url = 'https://en.wikipedia.org'
        response = get(url + self.link)
        soup = BeautifulSoup(response.text, 'lxml')

        tags = soup.body.find('div', class_='mw-parser-output').find('p', class_=None, recursive=False).find_all('a')
        self.subnodes = [Node(tag['href'], self.depth + 1) for tag in tags if tag.parent.name == 'p']
        self.words = [tag.text for tag in tags if tag.parent.name == 'p']
        print(self.words)

n = Node('/wiki/' + sys.argv[1], 1)
