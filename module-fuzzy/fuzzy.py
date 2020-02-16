import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Los nuevos objetos antecedentes / consecuentes contienen variables del universo y pertenencia
# funciones
quality = ctrl.Antecedent(np.arange(0, 11, 1), 'calidad')
service = ctrl.Antecedent(np.arange(0, 11, 1), 'servicio')
tip = ctrl.Consequent(np.arange(0, 26, 1), 'propina')

# La función de membresía automática es posible con .automf (3, 5 o 7)
quality.automf(3)
service.automf(3)

# Las funciones de membresía personalizadas se pueden construir interactivamente con un familiar,
# API Pythonic
tip['bajo'] = fuzz.trimf(tip.universe, [0, 0, 13])
tip['medio'] = fuzz.trimf(tip.universe, [0, 13, 25])
tip['alto'] = fuzz.trimf(tip.universe, [13, 25, 25])

# Puedes ver cómo se ven con .view ()
# quality['average'].view()

# service.view()
#
# tip.view()

# Rules
rule1 = ctrl.Rule(quality['poor'] | service['poor'], tip['bajo'])
rule2 = ctrl.Rule(service['average'], tip['medio'])
rule3 = ctrl.Rule(service['good'] | quality['good'], tip['alto'])
#
# rule1.view()

tipping_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
tipping = ctrl.ControlSystemSimulation(tipping_ctrl)

# Pass inputs to the ControlSystem using Antecedent labels with Pythonic API
# Note: if you like passing many inputs all at once, use .inputs(dict_of_data)
tipping.input['calidad'] = 6.5
tipping.input['servicio'] = 9.8

# Crunch the numbers
tipping.compute()

print(tipping.output['propina'])
tip.view(sim=tipping)
