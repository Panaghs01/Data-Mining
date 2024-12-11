import matplotlib.pyplot as plt
import pandas as pd
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np
import preprocessing as pp


outliers,clean = pp.run()

# Antecedent/Consequent
# Generate array from 0 to a little above productivity ratio max value
productivity_ratio_fuzzy = ctrl.Antecedent(np.arange(0, 2.1, 0.1), 'productivity_ratio_fuzzy') 
#Generate array from 0 to a little above actual productivity max value
actual_productivity_fuzzy = ctrl.Antecedent(np.arange(0, 1.3, 0.1), 'actual_productivity_fuzzy')

expectation_concern = ctrl.Consequent(np.arange(0, 11, 1), 'expectation_concern')
production_concern = ctrl.Consequent(np.arange(0, 11, 1), 'production_concern')

act_mean = np.mean(clean['actual_productivity'])
act_std = np.std(clean['actual_productivity'])

actual_productivity_fuzzy['poor'] = fuzz.trapmf(actual_productivity_fuzzy.universe,[0,0,act_mean-1.5*act_std,act_mean-act_std])
actual_productivity_fuzzy['average'] = fuzz.trapmf(actual_productivity_fuzzy.universe, [act_mean-1.5*act_std, act_mean-act_std, act_mean+act_std, act_mean+1.5*act_std])
actual_productivity_fuzzy['good'] = fuzz.trapmf(actual_productivity_fuzzy.universe,[act_mean+act_std,act_mean+1.5*act_std,1.3,1.3])

productivity_ratio_fuzzy['poor'] = fuzz.trapmf(productivity_ratio_fuzzy.universe, [0,0,0.9,1])
productivity_ratio_fuzzy['average'] = fuzz.trimf(productivity_ratio_fuzzy.universe, [0.9,1,1.1])
productivity_ratio_fuzzy['good'] = fuzz.trapmf(productivity_ratio_fuzzy.universe, [1,1.1,2,2])

# Consequent membership function is formed!
expectation_concern['low'] = fuzz.trapmf(expectation_concern.universe, [0, 0, 2, 4]) 
expectation_concern['medium'] = fuzz.trapmf(expectation_concern.universe, [2, 4, 6, 8])
expectation_concern['high'] = fuzz.trapmf(expectation_concern.universe, [6, 8, 10, 10])

# Consequent membership function is formed!
production_concern['low'] = fuzz.trapmf(production_concern.universe, [0, 0, 2, 4]) 
production_concern['medium'] = fuzz.trapmf(production_concern.universe, [2, 4, 6, 8])
production_concern['high'] = fuzz.trapmf(production_concern.universe, [6, 8, 10, 10])

actual_productivity_fuzzy.view()
productivity_ratio_fuzzy.view()

# Rules
rule1a = ctrl.Rule(actual_productivity_fuzzy['poor'] & productivity_ratio_fuzzy['poor'], production_concern['high'])
rule1b = ctrl.Rule(actual_productivity_fuzzy['poor'] & productivity_ratio_fuzzy['poor'], expectation_concern['low'])
rule2a = ctrl.Rule(actual_productivity_fuzzy['poor'] & (productivity_ratio_fuzzy['average'] | productivity_ratio_fuzzy['good']), production_concern['high'])
rule2b = ctrl.Rule(actual_productivity_fuzzy['poor'] & (productivity_ratio_fuzzy['average'] | productivity_ratio_fuzzy['good']), expectation_concern['high'])

rule3a = ctrl.Rule(actual_productivity_fuzzy['average'] & productivity_ratio_fuzzy['average'], production_concern['low'])
rule3b = ctrl.Rule(actual_productivity_fuzzy['average'] & productivity_ratio_fuzzy['average'], expectation_concern['low'])
rule4a = ctrl.Rule(actual_productivity_fuzzy['average'] & productivity_ratio_fuzzy['good'], expectation_concern['medium'])
rule4b = ctrl.Rule(actual_productivity_fuzzy['average'] & productivity_ratio_fuzzy['good'], production_concern['low'])
rule5a = ctrl.Rule(actual_productivity_fuzzy['average'] & productivity_ratio_fuzzy['poor'], production_concern['medium'])
rule5b = ctrl.Rule(actual_productivity_fuzzy['average'] & productivity_ratio_fuzzy['poor'], expectation_concern['high'])

rule6a = ctrl.Rule(actual_productivity_fuzzy['good'] & productivity_ratio_fuzzy['poor'], expectation_concern['high'])
rule6b = ctrl.Rule(actual_productivity_fuzzy['good'] & productivity_ratio_fuzzy['poor'], production_concern['medium'])
rule7a = ctrl.Rule(actual_productivity_fuzzy['good'] & (productivity_ratio_fuzzy['average'] | productivity_ratio_fuzzy['good']) , expectation_concern['medium'])
rule7b = ctrl.Rule(actual_productivity_fuzzy['good'] & (productivity_ratio_fuzzy['average'] | productivity_ratio_fuzzy['good']), production_concern['low'])

# Control System Creation and Simulation
concern_ctrl = ctrl.ControlSystem([rule1a, rule1b, rule2a, rule2b, rule3a, rule3b,
                                   rule4a, rule4b, rule5a, rule5b, rule6a, rule6b,
                                   rule7a, rule7b])
 
simulation = ctrl.ControlSystemSimulation(concern_ctrl)

expectation_concern_list = []
production_concern_list = []

#simulation.input['actual_productivity_fuzzy'] = 0.5
#simulation.input['productivity_ratio_fuzzy'] = 0.8

#simulation.compute()

#production_concern.view(sim=simulation)
#expectation_concern.view(sim=simulation)
#print(simulation.output)

for index,item in clean[['actual_productivity','productivity_ratio']].iterrows():
    simulation.input['actual_productivity_fuzzy'] = item['actual_productivity']
    simulation.input['productivity_ratio_fuzzy'] = item['productivity_ratio']
    # Crunch the numbers
    simulation.compute()

    #production_concern.view(sim=simulation)
    #expectation_concern.view(sim=simulation)

    #print(simulation.output)

    expectation_concern_list.append(simulation.output['expectation_concern'])
    production_concern_list.append(simulation.output['production_concern'])


#print(concern_sim.output)
clean['expectation_concern'] = expectation_concern_list
clean['production_concern'] = production_concern_list
    
# Generating a grouped dataframe for each team.
a = clean.groupby('team')
kati = pd.DataFrame()
# Creating an average production concern for every team based
# on a weighted average formula.
avg_dict = {}
for i in a:
    numerator=0
    denominator=0
    for value in i[1]['production_concern']:
        numerator += value * (value/10)
        denominator += value/10

        avg_dict[i[0]] = round((numerator/denominator), 3)

    plt.scatter(np.arange(0, i[1]['production_concern'].size),i[1]['production_concern'])
    plt.title(f'Team:{i[0]}')
    plt.show()

# Sorting the average production concern dictionary.
sorted_avg_dict = sorted(avg_dict.items(), key=lambda kv: kv[1])
print(sorted_avg_dict)


kati = clean.where(clean['production_concern'] >= 5)
kati.dropna(inplace = True)
print(kati)


    
corr_df = kati[['department','team','no_of_workers','no_of_style_change','targeted_productivity',
                'actual_productivity','smv','wip','over_time','incentive','expectation_concern','production_concern']]

# Correlation plots

    
for i in corr_df.columns:
    # correlation_actual = corr_df[['expectation_concern',i]].corr(
    #     method='pearson')
    x = corr_df['production_concern']
    y = corr_df[i]
    plt.title(i)
    plt.scatter(x, y)
    plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))
         (np.unique(x)), color='red')
    plt.show()
    correlation = corr_df[['production_concern',i]].corr(
        method='pearson')
    # print(correlation_actual)
    print(correlation['production_concern'])
    print()
    # print(correlation['production_concern'].loc[i])

b = kati.groupby('team')

for i in b:
    print(i[0],len(i[1]))






    