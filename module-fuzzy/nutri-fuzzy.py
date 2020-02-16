import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Los nuevos objetos antecedentes / consecuentes contienen variables del universo y pertenencia funciones
edad = ctrl.Antecedent(np.arange(0, 100, 1), 'edad')
sexo = ctrl.Antecedent(np.arange(0, 25, 1), 'sexo')
gerf = ctrl.Consequent(np.arange(0, 61, 1), 'gerf')

# edad.automf(3)
edad['niño'] = fuzz.trimf(edad.universe, [0, 5, 11])
edad['adolecente'] = fuzz.trimf(edad.universe, [10, 15, 17])
edad['joven'] = fuzz.trimf(edad.universe, [15, 24, 29])
edad['adulto'] = fuzz.trimf(edad.universe, [29, 40, 59])
edad['adulto_mayor'] = fuzz.trimf(edad.universe, [55, 80, 99])

# sexo.automf(3)
sexo['hombre'] = fuzz.trimf(sexo.universe, [0, 0, 10])
sexo['mujer'] = fuzz.trimf(sexo.universe, [5, 10, 15])
sexo['na'] = fuzz.trimf(sexo.universe, [10, 15, 20])

# gerf = ctrl.Consequent(np.arange(10.5, 11.6, 12.2, 13.5, 14.7, 15.3, 17.5, 22.5, 22.7, 60, 61), 'gerf')
gerf['bajo'] = fuzz.trimf(gerf.universe, [0, 5, 10.5])
gerf['medio_bajo'] = fuzz.trimf(gerf.universe, [5.5, 10.5, 15.5])
gerf['medio'] = fuzz.trimf(gerf.universe, [15.5, 20, 25.5])
gerf['medio_alto'] = fuzz.trimf(gerf.universe, [25.5, 35, 40])
gerf['alto'] = fuzz.trimf(gerf.universe, [40, 50, 61])

edad.view()
sexo.view()
gerf.view()

# # Rules
rule1a = ctrl.Rule(edad['adulto'] | sexo['hombre'], gerf['bajo'])
rule1b = ctrl.Rule(edad['adulto'] | sexo['mujer'], gerf['medio_bajo'])

rule2 = ctrl.Rule(sexo['mujer'], gerf['medio'])

rule3a = ctrl.Rule(edad['adulto_mayor'] | sexo['hombre'], gerf['medio_alto'])
rule3b = ctrl.Rule(edad['adulto_mayor'] | sexo['mujer'], gerf['alto'])

rule4a = ctrl.Rule(edad['adolecente'] | sexo['hombre'], gerf['bajo'])
rule4b = ctrl.Rule(edad['adolecente'] | sexo['mujer'], gerf['medio_bajo'])

rule5a = ctrl.Rule(edad['joven'] | sexo['hombre'], gerf['medio'])
rule5b = ctrl.Rule(edad['joven'] | sexo['mujer'], gerf['medio_bajo'])

rule6a = ctrl.Rule(edad['niño'] | sexo['hombre'], gerf['bajo'])
rule6b = ctrl.Rule(edad['niño'] | sexo['mujer'], gerf['medio_bajo'])

# #
# # rule1.view()
#
gerf_ctrl = ctrl.ControlSystem(
    [rule1a, rule1b, rule2, rule3a, rule3b, rule4a, rule4b, rule5a, rule5b, rule6a, rule6b])
ger = ctrl.ControlSystemSimulation(gerf_ctrl)


ger.input['edad'] = int(25)
ger.input['sexo'] = int(10)
#
# # Crunch the numbers
ger.compute()
#
print(ger.output['gerf'])
gerf.view(sim=ger)
