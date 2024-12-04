# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 13:12:48 2024

@author: panos
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#Preprocessing

pd.set_option('display.max_rows',10)
pd.set_option('display.max_columns',None)


df = pd.read_csv(
    r"""C:\Users\user\Desktop\code\Data_mining\garments_worker_productivity.csv""")

#replacing NaN values with 0
df.fillna({'wip':0},inplace = True)

df['productivity_ratio'] = df['actual_productivity']/df['targeted_productivity']
#Cleaning up attributes
df = df.round(
    {'actual_productivity': 4, 'productivity_ratio': 4, 'no_of_workers': 0})

df.replace({"finishing ":"finishing"},inplace = True)
df.replace({'sweing':'sewing'},inplace = True) #this is needless
df.replace({'sewing':-1},inplace = True)
df.replace({'finishing':1},inplace = True)

print(df)

actual_prod_mean = df['actual_productivity'].mean()
targeted_prod_mean = df['targeted_productivity'].mean()
ratio_prod_mean = df['productivity_ratio'].mean()

# print("Actual prod mean:",actual_prod_mean)
# print("Targeted prod mean:",targeted_prod_mean)
# print("Ratio prod mean:",ratio_prod_mean)

correlation_matrix = []
corr_df = df[['department','team','no_of_workers','no_of_style_change','targeted_productivity',
              'actual_productivity','smv','wip','over_time','incentive','idle_time','idle_men']]

for i in corr_df.columns:
    print()
    correlation_actual = df[['actual_productivity',i]].corr(
        method='pearson')
    correlation_ratio = df[['productivity_ratio',i]].corr(
        method='pearson')
    print(correlation_actual)
    print(correlation_ratio)
    print()
    
    
    
#Boxplot outlier detection
over_time_list = [x for x in df['over_time']]
over_time_list = sorted(over_time_list)
over = np.array(over_time_list)

median = np.median(over)
q1 = np.quantile(over, 0.25)
q3 = np.quantile(over, 0.75)
iqr = q3-q1
lower = q1 - 1.5*iqr
upper = q3 + 1.5*iqr

# print(q1,q3,median,iqr,upper,lower)

plt.figure(figsize=(15, 6), dpi=80)
plt.boxplot(over_time_list)
plt.show()

clean_df = pd.DataFrame(df['over_time'].where((df['over_time'] <= upper) & (
                df['over_time'] >= lower)))
clean_df.dropna(inplace = True)


plt.boxplot(clean_df)
plt.show()
















