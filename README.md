## Sistema de control difuso para el cálculo del GER
### Antecednets (entradas)
- **Edad**
    - Universo (es decir, rango de valores nítidos): ¿Que edad se especifica para el cáculo, en una escala del 1 al 100?
    - Conjunto difuso (es decir, rango de valores difusos): niño, joven, adulto
    
- **Sexo**
    - Universo: ¿Cual es tu sexo!, en una escala del 1 al 100?
    - Conjunto difuso: hombre, mujer, na

### Consecuencias (Salidas)
- **Ger**
    - Universo: ¿Valor que debería ser, en una escala de 10 al 61
    - Conjunto difuso: bajo, medio, alto

### Reglas
* SI la edad corresponde a un niño **o** el sexo de la persona es hombre, ENTONCES el cálculo del ger será alto.
* SI el edad corresponde a un joven, ENTONCES el cálculo del ger será media.
* SI el edad corresponde a un adulto y el sexo de la persona es mujer, ENTONCES el cálculo del ger será baja.

### Uso
- **Si le digo a este controlador que cálcule :**
    - La edad = 25, y el sexo = Mujer
- **Genera un valor:**
    - **GER:** 2359
