import sys
from time import sleep
from random import randint
import re

from requests import get
from bs4 import BeautifulSoup

link = "/wiki/" + sys.argv[1]

while True:
    url = 'https://en.wikipedia.org'
    response = get(url + link)
    soup = BeautifulSoup(response.text, 'html.parser')

    p = soup.body.find('div', class_='mw-parser-output').find('p', class_=None, recursive=False)
    p.string = re.sub(r'\([^)]*\)', '', p.text)
    tags = p.find_all('a')
    print(tags)
    print(soup.body.find('div', class_='mw-parser-output').find('p', class_=None, recursive=False))
    links = [tag['href'] for tag in tags if tag.parent.name == 'p']
    words = [tag.text.lower() for tag in tags if tag.parent.name == 'p']
    print(words[0])
    link = links[0]
