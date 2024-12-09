import matplotlib.pyplot as plt
import pandas as pd
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np
import preprocessing as pp


outliers,clean = pp.run()

#Antecedent/Consequent 
#Generate array from 0 to a little above productivity ratio max value
productivity_ratio_fuzzy = ctrl.Antecedent(np.arange(0, 2.1, 0.1), 'productivity_ratio_fuzzy') 
#Generate array from 0 to a little above actual productivity max value
actual_productivity_fuzzy = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'actual_productivity_fuzzy')

expectation_concern = ctrl.Consequent(np.arange(0, 11, 1), 'expectation_concern')
production_concern = ctrl.Consequent(np.arange(0, 11, 1), 'production_concern')

actual_productivity_fuzzy['good'] = fuzz.trapmf(actual_productivity_fuzzy.universe,[0.6,0.7,1,1])
actual_productivity_fuzzy['average'] = fuzz.trapmf(actual_productivity_fuzzy.universe, [0.3,0.4,0.6,0.7])
actual_productivity_fuzzy['poor'] = fuzz.trapmf(actual_productivity_fuzzy.universe,[0,0,0.3,0.4])

productivity_ratio_fuzzy['good'] = fuzz.trapmf(productivity_ratio_fuzzy.universe, [1.1,1.5,2,2])
productivity_ratio_fuzzy['average'] = fuzz.trapmf(productivity_ratio_fuzzy.universe, [0.8,0.9,1.1,1.2])
productivity_ratio_fuzzy['poor'] = fuzz.trapmf(productivity_ratio_fuzzy.universe, [0,0,0.6,0.9])

# Consequent membership function is formed!
expectation_concern['low'] = fuzz.trapmf(expectation_concern.universe, [0, 0, 2, 4]) 
expectation_concern['medium'] = fuzz.trapmf(expectation_concern.universe, [2, 4, 6, 8])
expectation_concern['high'] = fuzz.trapmf(expectation_concern.universe, [6, 8, 10, 10])

# Consequent membership function is formed!
production_concern['low'] = fuzz.trapmf(production_concern.universe, [0, 0, 2, 4]) 
production_concern['medium'] = fuzz.trapmf(production_concern.universe, [2, 4, 6, 8])
production_concern['high'] = fuzz.trapmf(production_concern.universe, [6, 8, 10, 10])

productivity_ratio_fuzzy.view()
actual_productivity_fuzzy.view()

# Rules
rule1 = ctrl.Rule(actual_productivity_fuzzy['poor'] & productivity_ratio_fuzzy['poor'], production_concern['high'])
rule2a = ctrl.Rule(actual_productivity_fuzzy['poor'] & (productivity_ratio_fuzzy['average'] | productivity_ratio_fuzzy['good']), production_concern['medium'])
rule2b = ctrl.Rule(actual_productivity_fuzzy['poor'] & (productivity_ratio_fuzzy['average'] | productivity_ratio_fuzzy['good']), expectation_concern['low'])

rule3 = ctrl.Rule(actual_productivity_fuzzy['average'] & productivity_ratio_fuzzy['average'], production_concern['low'])
rule4 = ctrl.Rule(actual_productivity_fuzzy['average'] & productivity_ratio_fuzzy['good'], expectation_concern['medium'])


rule5 = ctrl.Rule(actual_productivity_fuzzy['good'] & productivity_ratio_fuzzy['poor'], expectation_concern['high'])
rule6 = ctrl.Rule(actual_productivity_fuzzy['good'] & productivity_ratio_fuzzy['average'], expectation_concern['medium'])
rule7 = ctrl.Rule(actual_productivity_fuzzy['good'], production_concern['low'])


# Control System Creation and Simulation
concern_ctrl = ctrl.ControlSystem([rule1, rule2a, rule2b, rule3, rule4, rule5, rule6]) # Create Control System using "ControlSystem" class from the skfuzzy.control module
 
simulation = ctrl.ControlSystemSimulation(concern_ctrl)

expectation_concer_list = []
production_concer_list = []

simulation.input['actual_productivity_fuzzy'] = 0.5
simulation.input['productivity_ratio_fuzzy'] = 0.9

simulation.compute()

print(simulation.output)
production_concern.view(sim=simulation)
expectation_concern.view(sim=simulation)

# for index,item in clean[['actual_productivity','productivity_ratio']].iterrows():
#     print(item['actual_productivity'],item['productivity_ratio'] )
#     simulation.input['actual_productivity_fuzzy'] = item['actual_productivity']
#     simulation.input['productivity_ratio_fuzzy'] = item['productivity_ratio']    
#     # Crunch the numbers
#     simulation.compute()

#     production_concern.view(sim=simulation)
#     expectation_concern.view(sim=simulation)
    
#     print(simulation.output)
    
#     # expectation_concer_list.append(simulation.output['expectation_concern'])
#     production_concer_list.append(simulation.output['production_concern'])
    
#     #!! Remove when you are absolutely certain this wont explode !!
#     break


#print(concern_sim.output)