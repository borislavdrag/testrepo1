from bs4 import BeautifulSoup
from requests import get
import sys

url = 'https://en.wikipedia.org/wiki/'
response = get(url + sys.argv[1])
soup = BeautifulSoup(response.text, 'html.parser')


tags = soup.body.find('div', class_='mw-parser-output').find('p', class_=None, recursive=False).find_all('a')
new_wikis = [tag['href'] for tag in tags if tag.parent.name != 'sup']
words = [tag.text for tag in tags if tag.parent.name != 'sup']
print(words)

# def explore_wiki(wiki):
#     url = 'https://en.wikipedia.org'
#     response = get(url + wiki)
#     soup = BeautifulSoup(response.text, 'lxml')
#
#     tags = soup.body.find('table', class_='infobox biota').find_next_sibling('p').find_all('a')
#     new_wikis = [tag['href'] for tag in tags if tag.parent.name != 'sup']
#     words = [tag.text for tag in tags if tag.parent.name != 'sup']
#     print(words)
#
# for wiki in new_wikis:
#     print(wiki)
#     explore_wiki(wiki)
