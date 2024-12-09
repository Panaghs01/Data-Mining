# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 13:12:48 2024

@author: panos
"""

import matplotlib.pyplot as plt
import pandas as pd
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np
import preprocessing as pp


outliers,clean = pp.run()

# New Antecedent/Consequent objects hold universe variables and membership functions
ratio_prod = ctrl.Antecedent(clean['productivity_ratio'], 'ratio_prod')#Generate the array [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
act_prod = ctrl.Antecedent(clean['actual_productivity'], 'act_prod')
concern = ctrl.Consequent(np.arange(0, 11, 1), 'concern')

concern['low'] = fuzz.trapmf(concern.universe, [0, 0, 2, 4]) #edo kathorizo ta akra kai to meso ton trigonon
concern['medium'] = fuzz.trapmf(concern.universe, [2, 4, 5,7])
concern['high'] = fuzz.trapmf(concern.universe, [7, 7,10, 10])

act_prod.automf(3)
ratio_prod.automf(3)
ratio_prod.view()
act_prod.view()
concern.view()