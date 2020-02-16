import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Los nuevos objetos antecedentes / consecuentes contienen variables del universo y pertenencia funciones
# edad = ctrl.Antecedent(np.arange(0, 3, 10, 18, 30, 60, 100), 'edad')
edad = ctrl.Antecedent(np.arange(0, 50, 1), 'edad')

# sexo = ctrl.Antecedent(np.arange(0, 1), 'sexo')
sexo = ctrl.Antecedent(np.arange(0, 50, 1), 'sexo')

# gerf = ctrl.Consequent(np.arange(10.5, 11.6, 12.2, 13.5, 14.7, 15.3, 17.5, 22.5, 22.7, 60, 61), 'gerf')
gerf = ctrl.Consequent(np.arange(0, 60, 1), 'gerf')

edad.automf(3)
sexo.automf(3)

gerf['bajo'] = fuzz.trimf(gerf.universe, [10.5, 11.6, 13.5])
gerf['medio'] = fuzz.trimf(gerf.universe, [14.7, 15.3, 17.5])
gerf['alto'] = fuzz.trimf(gerf.universe, [22.5, 60, 61])

edad['average'].view()

sexo.view()

gerf.view()

# Rules
rule1 = ctrl.Rule(edad['poor'] | sexo['poor'], gerf['bajo'])
rule2 = ctrl.Rule(sexo['average'], gerf['medio'])
rule3 = ctrl.Rule(sexo['good'] | edad['good'], gerf['alto'])
#
# rule1.view()

tipping_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
tipping = ctrl.ControlSystemSimulation(tipping_ctrl)

tipping.input['edad'] = 3
tipping.input['sexo'] = 1

# Crunch the numbers
tipping.compute()

print(tipping.output['gerf'])
gerf.view(sim=tipping)