import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Los nuevos objetos antecedentes / consecuentes contienen variables del universo y pertenencia funciones
edad = ctrl.Antecedent(np.arange(0, 110, 1), 'edad')
sexo = ctrl.Antecedent(np.arange(0, 25, 1), 'sexo')
factor_ger_f = ctrl.Consequent(np.arange(0, 70, 1), 'factor_ger_f')

# edad.automf(3)
edad['INFANTE'] = fuzz.trimf(edad.universe, [0, 2, 3])
edad['NIÑO'] = fuzz.trimf(edad.universe, [3, 9, 10])
edad['ADOLECENTE'] = fuzz.trimf(edad.universe, [10, 17, 18])
edad['JOVEN'] = fuzz.trimf(edad.universe, [18, 30, 30])
edad['ADULTO'] = fuzz.trimf(edad.universe, [30, 60, 60])
edad['ADULTO_MAYOR'] = fuzz.trimf(edad.universe, [60, 80, 100])

# sexo.automf(3)
sexo['HOMBRE'] = fuzz.trimf(sexo.universe, [0, 5, 5])
sexo['MUJER'] = fuzz.trimf(sexo.universe, [5, 10, 10])
sexo['NA'] = fuzz.trimf(sexo.universe, [10, 13, 15])

factor_ger_f['BAJO'] = fuzz.trimf(factor_ger_f.universe, [0, 12, 12.2])
factor_ger_f['MEDIO_BAJO'] = fuzz.trimf(factor_ger_f.universe, [12.2, 23.4, 24.4])
factor_ger_f['MEDIO'] = fuzz.trimf(factor_ger_f.universe, [24.4, 35.6, 36.6])
factor_ger_f['MEDIO_ALTO'] = fuzz.trimf(factor_ger_f.universe, [36.6, 47.8, 48.8])
factor_ger_f['ALTO'] = fuzz.trimf(factor_ger_f.universe, [48.8, 55, 61])

edad.view()
sexo.view()
factor_ger_f.view()

# # Rules
rule1a = ctrl.Rule(edad['INFANTE'] & sexo['HOMBRE'], factor_ger_f['ALTO'])
rule1b = ctrl.Rule(edad['INFANTE'] & sexo['MUJER'], factor_ger_f['ALTO'])

rule2a = ctrl.Rule(edad['NIÑO'] & sexo['HOMBRE'], factor_ger_f['MEDIO_BAJO'])
rule2b = ctrl.Rule(edad['NIÑO'] & sexo['MUJER'], factor_ger_f['MEDIO_BAJO'])

rule3a = ctrl.Rule(edad['ADOLECENTE'] & sexo['HOMBRE'], factor_ger_f['MEDIO_BAJO'])
rule3b = ctrl.Rule(edad['ADOLECENTE'] & sexo['MUJER'], factor_ger_f['BAJO'])

rule4a = ctrl.Rule(edad['JOVEN'] & sexo['HOMBRE'], factor_ger_f['MEDIO_BAJO'])
rule4b = ctrl.Rule(edad['JOVEN'] & sexo['MUJER'], factor_ger_f['MEDIO_BAJO'])

rule5a = ctrl.Rule(edad['ADULTO'] & sexo['HOMBRE'], factor_ger_f['BAJO'])
rule5b = ctrl.Rule(edad['ADULTO'] & sexo['MUJER'], factor_ger_f['MEDIO_BAJO'])

rule6a = ctrl.Rule(edad['ADULTO_MAYOR'] & sexo['HOMBRE'], factor_ger_f['MEDIO_BAJO'])
rule6b = ctrl.Rule(edad['ADULTO_MAYOR'] & sexo['MUJER'], factor_ger_f['BAJO'])

# #
rule1a.view()
#
factor_ger_f_ctrl = ctrl.ControlSystem(
    [rule1a, rule1b, rule2a, rule2b, rule3a, rule3b, rule4a, rule4b, rule5a, rule5b, rule6a, rule6b])
factor_ger = ctrl.ControlSystemSimulation(factor_ger_f_ctrl)


factor_ger.input['edad'] = int(80)
factor_ger.input['sexo'] = int(5)
#
# # Crunch the numbers
factor_ger.compute()
#
print(factor_ger.output['factor_ger_f'])
factor_ger_f.view(sim=factor_ger)
