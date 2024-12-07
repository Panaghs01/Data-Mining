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
    r"""C:/Users/Admin/Desktop/Data-Mining/garments_worker_productivity.csv""")

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

# for i in corr_df.columns:
#     print()
#     correlation_actual = df[['actual_productivity',i]].corr(
#         method='pearson')
#     correlation_ratio = df[['productivity_ratio',i]].corr(
#         method='pearson')
#     plt.plot(correlation_actual)
#     plt.show()
#     print(correlation_actual)
#     print(correlation_ratio)
#     print()

# Bloxplots!
def bloxplot(attribute):
    #Give attribute as an array made from the df column
    #Calculate the boxplot
    median = np.median(attribute)
    q1 = np.quantile(attribute, 0.25)
    q3 = np.quantile(attribute, 0.75)
    iqr = q3-q1
    lower_inner_fence = q1 - 1.5*iqr
    upper_inner_fence = q3 + 1.5*iqr
    
    return (median, iqr, lower_inner_fence, upper_inner_fence)

def pretty_graphs(attribute):
    #This makes the histogram/boxplot graph look good
    fig, (ax_box, ax_hist) = plt.subplots(
        nrows=2, 
        sharex=True,  # Share the x-axis
        gridspec_kw={"height_ratios": [1, 3]}  # Boxplot smaller than histogram
    )
    ax_box.boxplot(df[attribute], vert=False, patch_artist=True)
    ax_box.spines['bottom'].set_visible(False)  
    ax_box.spines['top'].set_visible(False)  
    ax_box.spines['right'].set_visible(False)  
    ax_box.spines['left'].set_visible(False)  
    ax_box.set_yticks([])  
    
    ax_hist.hist(df[attribute], edgecolor='yellow', color='purple')
    ax_hist.set_ylabel('Frequency')
    ax_hist.set_xlabel('Values')
    ax_hist.set_title(f'{attribute}')
    ax_hist.spines['top'].set_visible(False)  

    plt.subplots_adjust(hspace=0)
    plt.show()
    

for attr in df:
    if(attr != 'date' and attr != 'quarter' and attr != 'department' and attr != 'day' and attr != 'team'):
        #Boxplot outlier detection
        attrlist = [x for x in df[attr]]
        attrlist = sorted(attrlist)
        attr_array = np.array(attrlist)
        # pretty_graphs(attr)

# overtime_box = bloxplot(overtime_array)
# idle_time_box = bloxplot()
# idle_men_box = bloxplot()

#df with all the outliers!!!!!
surprise_tool_that_will_help_us_later = pd.DataFrame()



mean = np.mean(df['actual_productivity'])
std = np.std(df['actual_productivity'])
normal_range=(mean-3*std,mean+3*std)
print(normal_range)

minprod = min(df['actual_productivity'])
maxprod = max(df['actual_productivity'])
print(minprod,maxprod)
outliers = []
for row in df['actual_productivity']:
    z = abs(row-mean)/std
    if (z > 3):
        outliers.append(row)
        
print(outliers)




# clean_df = pd.DataFrame(df['over_time'].where((df['over_time'] <= upper) & (
#                 df['over_time'] >= lower)))
# clean_df.dropna(inplace = True)


# plt.boxplot(clean_df)
# plt.show()
















