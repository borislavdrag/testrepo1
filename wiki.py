from bs4 import BeautifulSoup
from requests import get

url = 'https://en.wikipedia.org/wiki/Cat'
response = get(url)
soup = BeautifulSoup(response.text, 'lxml')

tags = soup.body.find('table', class_='infobox biota').find_next_sibling('p').find_all('a')
new_wikis = [tag['href'] for tag in tags if tag.parent.name != 'sup']
words = [tag.text for tag in tags if tag.parent.name != 'sup']
print(words, new_wikis)
