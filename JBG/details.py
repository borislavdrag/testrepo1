import pandas as pd

from requests import get
from bs4 import BeautifulSoup

from time import sleep
import random

start = 'Проблем с обявата'
end = 'Кандидатствай по тази обява'

keywords = ['Java', 'SAP', 'Python', 'ERP', 'C++', 'Javascript', 'CRM']

data_main = pd.read_csv('jobs_bg.csv')
data_all = pd.read_csv('all_jobs_bg.csv')

for idx, job in data_main.iterrows():

    if not job['Explored']:

        url = "https://www.jobs.bg/" + job['Link']
        response = get(url)
        html_soup = BeautifulSoup(response.text, 'lxml')
        # sleep(random.randint(4, 15))

        [script.extract() for script in html_soup('script')]
        [style.extract() for style in html_soup('style')]

        s = html_soup.get_text()

        if start in s and end in s:
            job['Details'] = (s.split(start))[1].split(end)[0].strip()
            job['Keywords'] = [0]*len(keywords)
            for i in range(len(keywords)):
                if keywords[i] in job['Details']:
                    job['Keywords'][i] = 1
            print('Processing job', idx)
            data_all.loc[-1] = job
            data_all.index += 1
            data_main.at[idx, 'Explored'] = 1
        else:
            print(f"Job {idx} not available {job['Link']}")
            data_main = data_main.drop(idx)

data_all.to_csv('all_jobs_bg.csv', index=False)
data_main.to_csv('jobs_bg.csv', index=False)
