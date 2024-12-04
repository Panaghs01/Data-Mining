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
df.replace({'sewing':0},inplace = True)
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


fig, (ax_box, ax_hist) = plt.subplots(
    nrows=2, 
    sharex=True,  # Share the x-axis
    gridspec_kw={"height_ratios": [1, 3]}  # Boxplot smaller than histogram
)
ax_box.boxplot(df['over_time'], vert=False, patch_artist=True)
ax_box.spines['bottom'].set_visible(False)  # Remove bottom border
ax_box.spines['top'].set_visible(False)  # Optional: hide top border
ax_box.spines['right'].set_visible(False)  # Optional: hide right border
ax_box.spines['left'].set_visible(False)  # Optional: hide left border
ax_box.set_yticks([])  # Remove y-axis ticks for cleanliness

ax_hist.hist(df['over_time'], edgecolor='yellow', color='purple')
ax_hist.set_ylabel('Frequency')
ax_hist.set_xlabel('Values')
ax_hist.spines['top'].set_visible(False)  # Remove top border (next to boxplot)

plt.subplots_adjust(hspace=0)
plt.show()
# clean_df = pd.DataFrame(df['over_time'].where((df['over_time'] <= upper) & (
#                 df['over_time'] >= lower)))
# clean_df.dropna(inplace = True)


# plt.boxplot(clean_df)
# plt.show()
















