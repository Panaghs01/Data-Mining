# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 13:12:48 2024

@author: panos
"""


import matplotlib.pyplot as plt
import pandas as pd


pd.set_option('display.max_rows',10)
pd.set_option('display.max_columns',None)

data = pd.read_csv("""C:/Users/panos/Desktop/Code/Data_mining/productivity+prediction+of+garment+employees/garments_worker_productivity.csv""")
df = pd.DataFrame(data)


df['wip'].fillna(0,inplace = True)
#a.append(df['actual_productivity']/df['targeted_productivity'])
df['productivity_ratio'] = df['actual_productivity']/df['targeted_productivity']

df = df.round({'actual_productivity': 4, 'productivity_ratio': 4, 'no_of_workers': 0})

df['department'].replace(to_replace = 'sweing',value = 'sewing',inplace = True)

print(df.where(df['wip'] != 0).dropna())

actual_prod_mean = df['actual_productivity'].mean()
targeted_prod_mean = df['targeted_productivity'].mean()
ratio_prod_mean = df['productivity_ratio'].mean()
print("Actual prod mean:",actual_prod_mean)
print("Targeted prod mean:",targeted_prod_mean)
print("Ratio prod mean:",ratio_prod_mean)


correlation_actual_overtime = df[['actual_productivity','over_time']].corr(method='pearson')
correlation_ratio_overtime = df[['productivity_ratio','over_time']].corr(method='pearson')

df1 = df.where(df['team'] == 1)
df1.dropna(inplace = True)

plt.plot(df1['productivity_ratio'])
plt.show()

print(df1['productivity_ratio'].mean())