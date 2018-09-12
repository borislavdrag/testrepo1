import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import sys

data = pd.read_csv('all_jobs_bg.csv')

def new_kw(kws):
    keywords = kws

    for idx, job in data.iterrows():
        job['Keywords'] = [0]*len(keywords)
        for i in range(len(keywords)):
            job['Keywords'][i] = 1 if keywords[i] in job['Details'] else 0
    data.to_csv('all_jobs_bg', index=False)


def analyse_kw():
    kwl = list(map(sum, zip(*list(map(eval, data['Keywords'])))))
    print(kwl)

if __name__ == '__main__':
    if len(sys.argv) is 1:
        analyse_kw()
    elif len(sys.argv) is 2 and argv[1] in list(data):
        pass
    else:
        new_kw(sys.argv[1:])
