import pandas as pd
from datetime import datetime

data = pd.read_csv('jobs_bg.csv')

for idx, job in data.iterrows():
    if (datetime.now() - datetime.strptime(job['Timestamp'], '%d.%m.%y')).days >= 31:
        data = data.drop(idx)
        print(f"Job {idx} cleaned")

data.to_csv('jobs_bg.csv', index=False)
