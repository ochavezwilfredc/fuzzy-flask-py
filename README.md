## Sistema de control difuso para el cálculo del GER
### Antecednets (entradas)
- **Edad**
    - Universo (es decir, rango de valores nítidos): ¿Que edad se especifica para el cáculo, en una escala del 1 al 100?
    - Conjunto difuso (es decir, rango de valores difusos): niño, adolecente, joven, adulto, adulto mayor
    
- **Sexo**
    - Universo: ¿Cual es tu sexo!, en una escala del 0 al 25?
    - Conjunto difuso: hombre, mujer, na

### Consecuencias (Salidas)
- **Ger**
    - Universo: ¿Valor que debería ser, en una escala de 0 al 61
    - Conjunto difuso: bajo, medio bajo, medio, medio alto, alto

### Reglas
* SI la edad corresponde a un adulto **o** el sexo de la persona es hombre, ENTONCES el cálculo del ger será bajo.
* SI la edad corresponde a un adulto **o** el sexo de la persona es mujer, ENTONCES el cálculo del ger será medio bajo.

* SI el sexo corresponde a una mujer, ENTONCES el cálculo del ger será medio.

* SI el edad corresponde a un adulto mayor y el sexo de la persona es hombre, ENTONCES el cálculo del ger será medio alto.
* SI el edad corresponde a un adulto mayor y el sexo de la persona es mujer, ENTONCES el cálculo del ger será alto.

* SI el edad corresponde a un adolecente y el sexo de la persona es hombre, ENTONCES el cálculo del ger será bajo.
* SI el edad corresponde a un adolecente y el sexo de la persona es mujer, ENTONCES el cálculo del ger será medio bajo.

* SI el edad corresponde a un joven y el sexo de la persona es hombre, ENTONCES el cálculo del ger será bajo.
* SI el edad corresponde a un joven y el sexo de la persona es mujer, ENTONCES el cálculo del ger será medio bajo.

* SI el edad corresponde a un niño y el sexo de la persona es hombre, ENTONCES el cálculo del ger será bajo.
* SI el edad corresponde a un niño y el sexo de la persona es mujer, ENTONCES el cálculo del ger será medio bajo.


### Uso
#### POSTMAN
* Usando el verbo **POST** 
* ENDPONIT http://13.58.250.57:5000/api/nutrition/ger
* BODY
```JSON
{
	"edad": "25",
	"sexo": "5",
	"peso": "80"
}
```
#### POSTMAN
- **Si le digo a este controlador que cálcule :**
    - La edad = 25, y el sexo = Mujer
- **Genera un valor:**
    - **GER:** 2016
