import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from pandas import *
from ast import literal_eval

# sns.set(color_codes=True)

data = pd.read_csv('all_jobs_bg.csv')
raw_salary_data = data[data['Salary'] != "0"]
salary_data = list(map(literal_eval, raw_salary_data['Salary'].tolist()))
salary_data = [sum(map(int, a))/2 if type(a) is tuple else a for a in salary_data]
for i in range(raw_salary_data.shape[0]):
    if raw_salary_data.iloc[i]['Currency'] == 'EUR':
        salary_data[i] *= 2
    if raw_salary_data.iloc[i]['B/N'] == 'Нето':
        salary_data[i] *= 1.25

print(np.mean(salary_data))
sns.distplot(salary_data)
plt.show()
cities = data['City'].value_counts().to_dict()
plt.pie(cities.values(), labels=list(cities.keys())[:7]+[""]*(len(cities)-7), labeldistance=1.1)
plt.axis('equal')
plt.show()
