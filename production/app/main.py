from flask import Flask, request, abort, jsonify
import numpy as np
import skfuzzy as fuzz
from flask_cors import CORS
from skfuzzy import control as ctrl

app = Flask(__name__)

# definición de constantes
HOST = '0.0.0.0'
PORT = 80
DEBUG = True

CORS(app, resources={r"/api/*": {"origins": "*"}})


def get_fuzzy(edad_, sexo_):
    # print("edad: {} - sexo: {}".format(type(edad_), type(sexo_)))
    edad = ctrl.Antecedent(np.arange(0, 100, 1), 'edad')
    sexo = ctrl.Antecedent(np.arange(0, 25, 1), 'sexo')
    gerf = ctrl.Consequent(np.arange(0, 61, 1), 'gerf')

    edad['niño'] = fuzz.trimf(edad.universe, [0, 5, 11])
    edad['adolecente'] = fuzz.trimf(edad.universe, [10, 15, 17])
    edad['joven'] = fuzz.trimf(edad.universe, [15, 24, 29])
    edad['adulto'] = fuzz.trimf(edad.universe, [29, 40, 59])
    edad['adulto_mayor'] = fuzz.trimf(edad.universe, [55, 80, 99])

    sexo['hombre'] = fuzz.trimf(sexo.universe, [0, 0, 10])
    sexo['mujer'] = fuzz.trimf(sexo.universe, [5, 10, 15])
    sexo['na'] = fuzz.trimf(sexo.universe, [10, 15, 20])

    gerf['bajo'] = fuzz.trimf(gerf.universe, [0, 5, 10.5])
    gerf['medio_bajo'] = fuzz.trimf(gerf.universe, [5.5, 10.5, 15.5])
    gerf['medio'] = fuzz.trimf(gerf.universe, [15.5, 20, 25.5])
    gerf['medio_alto'] = fuzz.trimf(gerf.universe, [25.5, 35, 40])
    gerf['alto'] = fuzz.trimf(gerf.universe, [40, 50, 61])

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

    gerf_ctrl = ctrl.ControlSystem(
        [rule1a, rule1b, rule2, rule3a, rule3b, rule4a, rule4b, rule5a, rule5b, rule6a, rule6b])
    ger = ctrl.ControlSystemSimulation(gerf_ctrl)

    ger.input['edad'] = edad_
    ger.input['sexo'] = sexo_

    ger.compute()

    ger_f = ger.output['gerf']
    # print("El GER para la edad: {} sexo: {} es: {}".format(edad_, sexo_, ger_f))
    return ger_f


@app.route('/api/nutrition/ger', methods=['POST'])
def get_fuzzy_ger():
    if not request.json or not ('edad' and 'sexo' and 'peso' in request.json):
        abort(400)
    edad = request.json.get('edad')
    sexo = request.json.get('sexo')
    peso = request.json.get('peso')

    gerf = get_fuzzy(int(edad), int(sexo))

    get_total = get_ger_total(int(gerf), int(edad), int(sexo), float(peso))

    return jsonify({'ger': int(get_total)}), 201


def get_ger_total(getf, edad, sexo, peso):
    if 0 < edad <= 3:
        if sexo == 1:
            ger = getf * peso - 54
        else:
            ger = getf * peso - 51
    else:
        if 3 < edad <= 10:
            if sexo == 1:
                ger = getf * peso + 495
            else:
                ger = getf * peso + 499
        else:
            if 10 < edad <= 18:
                if sexo == 1:
                    ger = getf * peso + 651
                else:
                    ger = getf * peso + 746
            else:
                if 18 < edad <= 30:
                    if sexo == 1:
                        ger = getf * peso + 679
                    else:
                        ger = getf * peso + 496
                else:
                    if 30 < edad <= 60:
                        if sexo == 1:
                            ger = getf * peso + 879
                        else:
                            ger = getf * peso + 746
                    else:
                        if edad > 60 and sexo == 1:
                            ger = getf * peso + 487
                        else:
                            ger = getf * peso + 596
    return ger


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)
