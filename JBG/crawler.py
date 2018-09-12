import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from requests import get
from bs4 import BeautifulSoup

from time import sleep
import random

from datetime import datetime, timedelta
import re

from pandas import *

platinum = '#ffaa2d'
diamond = '#66c1ff'

url = "https://www.jobs.bg/it"
response = get(url)
html_soup = BeautifulSoup(response.text, 'html.parser')

jobs, joblinks, companies, dates, ratings, timestamps, cities, internship,\
 salaries, currency, nb, explored, dets, kw = ([] for i in range(14))

data_main = pd.read_csv('jobs_bg.csv')

while True:
    next = html_soup.find_all('a', class_="pathlink")[-1]

    for job, date, company in zip(html_soup.find_all('a', class_='joblink'), html_soup.find_all('span', class_='explainGray'), html_soup.find_all('a', class_='company_link')):
        if job['href'] not in data_main['Link'].tolist():
            print("Added", len(jobs)+1)

            jobs.append(job.text)
            joblinks.append(job['href'])
            companies.append(company.text)

            date_text = date.text
            if date_text == "днес":
                date_text = datetime.now().strftime("%d.%m.%y")
            elif date_text == "вчера":
                date_text = (datetime.now() - timedelta(1)).strftime("%d.%m.%y")
            dates.append(date_text)

            dets.append("")
            explored.append(0)
            kw.append("")

            timestamps.append(datetime.now().strftime("%d.%m.%y"))  # TODO give it a normal date (and change clean.py as well)

            details = job.parent.parent.div.span.text.strip()
            cities.append(re.split('[,;-]', details)[0])
            internship.append(1 if 'Стаж' in details else 0)

            nums = re.findall('(\d+(?:[.]\d+)?)', details)
            curr_and_nb = details.split()
            if len(nums) is 0:
                salaries.append(0)
                currency.append(0)
                nb.append(0)
            elif len(nums) is 1:
                salaries.append(nums[0])
                currency.append(curr_and_nb[-2])
                nb.append(curr_and_nb[-1].strip('()'))
            else:
                salaries.append((nums[0], nums[1]))
                currency.append(curr_and_nb[-2])
                nb.append(curr_and_nb[-1].strip('()'))

            next_ = date.find_next()
            if next_.name == 'span':
                if len(next_.text) is 5:
                    ratings.append('diamond' if re.search('(#.{6})', next_['style']).group(1) == diamond else 'platinum')
                elif len(next_.text) is 3:
                    ratings.append('gold')
                elif next_.text == '\uf4b3':
                    ratings.append('silver')
                else:
                    ratings.append('half-silver')
            else:
                ratings.append(0)

    # sleep(random.randint(1, 3))

    if next.text != ">>":
        break
    else:
        url = "https://www.jobs.bg" + next['href']
        response = get(url)
        html_soup = BeautifulSoup(response.text, 'html.parser')

print("Jobs added: ", len(jobs))

data = pd.DataFrame({'Job': jobs, 'Link': joblinks, 'Company': companies, 'Date': dates,
    'Rating': ratings, 'Timestamp': timestamps, 'City': cities, 'Internship': internship,
    'Salary': salaries, 'Currency': currency, 'B/N': nb, 'Explored': explored, 'Details': dets, 'Keywords': kw})
data.to_csv('jobs_bg.csv', mode='a', header=None, index=False)
print(data.tail())
