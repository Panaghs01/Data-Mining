# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 13:12:48 2024

@author: panos
"""

import pandas as pd
import numpy as np

pd.set_option('display.max_rows',10)
pd.set_option('display.max_columns',None)

data = pd.read_csv("""C:/Users/panos/Desktop/Code/Data_mining/productivity+prediction+of+garment+employees/garments_worker_productivity.csv""")
df = pd.DataFrame(data)


df['wip'].fillna(0,inplace = True)
#a.append(df['actual_productivity']/df['targeted_productivity'])
df['productivity_ratio'] = df['actual_productivity']/df['targeted_productivity']

df = df.round({'actual_productivity': 4, 'productivity_ratio': 4})
df['department'].replace(to_replace = 'sweing',value = 'sewing',inplace = True)

print(df)

actual_prod_mean = df['actual_productivity'].mean()
targeted_prod_mean = df['targeted_productivity'].mean()
print(df[['actual_productivity','over_time']].corr(method='pearson'))