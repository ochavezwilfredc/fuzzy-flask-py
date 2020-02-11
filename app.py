from flask import Flask, request, abort, jsonify
import numpy as np
import skfuzzy as fuzz
from flask_cors import CORS
from skfuzzy import control as ctrl

app = Flask(__name__)
# definición de constantes
PORT = 5000
DEBUG = True

CORS(app, resources={r"/api/*": {"origins": "*"}})


def get_fuzzy(edad_, sexo_):
    print("edad: {} - sexo: {}".format(type(edad_), type(sexo_)))

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

    # edad['average'].view()

    # sexo.view()

    # gerf.view()

    # Rules
    rule1 = ctrl.Rule(edad['poor'] | sexo['poor'], gerf['bajo'])
    rule2 = ctrl.Rule(sexo['average'], gerf['medio'])
    rule3 = ctrl.Rule(sexo['good'] | edad['good'], gerf['alto'])
    #
    # rule1.view()

    tipping_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
    tipping = ctrl.ControlSystemSimulation(tipping_ctrl)

    tipping.input['edad'] = edad_
    tipping.input['sexo'] = sexo_

    # Crunch the numbers
    tipping.compute()
    ger = tipping.output['gerf']
    print("El GER para la edad: {} sexo: {} es: {}".format(edad, sexo, ger))
    # gerf.view(sim=tipping)
    return ger


@app.route('/nutricion/api/v1/ger', methods=['POST'])
def get_fuzzy_ger():
    if not request.json or not ('edad' in request.json and 'sexo' in request.json and 'peso' in request.json):
        abort(400)
    edad = request.json.get('edad')
    sexo = request.json.get('sexo')
    peso = request.json.get('peso')

    gerf = get_fuzzy(int(edad), int(sexo))

    get_total = get_ger_total(int(gerf), int(edad), int(sexo), float(peso))

    return jsonify({'ger': get_total}), 201


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
    app.run(port=PORT, debug=DEBUG)
