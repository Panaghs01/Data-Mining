import matplotlib.pyplot as plt
import pandas as pd
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np
import preprocessing as pp


outliers,clean = pp.run()

#Antecedent/Consequent 
#Generate array from 0 to a little above productivity ratio max value
ratio_prod = ctrl.Antecedent(np.arange(0, 1.7, 0.1), 'ratio_prod') 
#Generate array from 0 to a little above actual productivity max value
act_prod = ctrl.Antecedent(np.arange(0, 1.2, 0.08), 'act_prod')

expectation_concern = ctrl.Consequent(np.arange(0, 11, 1), 'expectation_concern')
production_concern = ctrl.Consequent(np.arange(0, 11, 1), 'production_concern')

act_prod.automf(3)
ratio_prod.automf(3)

# Consequent membership function is formed!
expectation_concern['low'] = fuzz.trapmf(expectation_concern.universe, [0, 0, 2, 4]) 
expectation_concern['medium'] = fuzz.trapmf(expectation_concern.universe, [2, 4, 6, 8])
expectation_concern['high'] = fuzz.trapmf(expectation_concern.universe, [6, 8, 10, 10])

# Consequent membership function is formed!
production_concern['low'] = fuzz.trapmf(production_concern.universe, [0, 0, 2, 4]) 
production_concern['medium'] = fuzz.trapmf(production_concern.universe, [2, 4, 6, 8])
production_concern['high'] = fuzz.trapmf(production_concern.universe, [6, 8, 10, 10])

# ratio_prod.view()
# act_prod.view()
# concern.view()

# Rules
rule1 = ctrl.Rule(act_prod['poor'] & ratio_prod['poor'], production_concern['high'])
rule2a = ctrl.Rule(act_prod['poor'] & ratio_prod['average'], production_concern['low'])
rule2b = ctrl.Rule(act_prod['poor'] & ratio_prod['average'],expectation_concern['low'])
rule3 = ctrl.Rule(act_prod['average'] & ratio_prod['average'], production_concern['medium'])
rule4 = ctrl.Rule(act_prod['average'] & ratio_prod['good'], expectation_concern['medium'])
rule5 = ctrl.Rule(act_prod['good'] & ratio_prod['poor'], expectation_concern['high'])
rule6 = ctrl.Rule(act_prod['good'] & (ratio_prod['average'] | ratio_prod['good']), production_concern['low'])


#Control System Creation and Simulation
concern_ctrl = ctrl.ControlSystem([rule1, rule2a, rule2b, rule3, rule4, rule5, rule6])#Create Control System using "ControlSystem" class from the skfuzzy.control module

concern_sim = ctrl.ControlSystemSimulation(concern_ctrl)

concern_sim.input['act_prod'] = 1
concern_sim.input['ratio_prod'] = 0.8

# Crunch the numbers
concern_sim.compute()

print( concern_sim.output['expectation_concern']) 
production_concern.view(sim=concern_sim)
expectation_concern.view(sim=concern_sim)