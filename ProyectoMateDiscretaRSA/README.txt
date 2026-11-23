# Sistema Criptográfico RSA - Matemática Discreta 1 (MM2015)
Grupo 6

El proyecto consiste en la implementación modular en Python del algoritmo de cifrado y descifrado RSA mediante aritmética modular y codificación por bloques ASCII.

## Estructura del proyecto
- interfaz.py: interfaz gráfica desarrollada con tkinter para la generación de llaves, cifrado y descifrado de mensajes.
- operaciones.py: funciones de alto nivel (cifrar_mensaje y descifrar_mensaje) para el procesamiento de bloques cifrados de 6 dígitos.
- conversion.py: conversión entre texto ASCII (3 dígitos por carácter) y bloques numéricos de 6 dígitos, incluyendo el manejo de relleno para longitudes impares.
- rsa.py: núcleo matemático con validación de parámetros, algoritmo de Euclides, inverso modular y exponenciación modular.

## Características principales
1. Validación de parámetros RSA: Verifica que "p" y "q" sean primos distintos, que el módulo "n = p \cdot q" sea mayor a "999999" para representar bloques de 6 dígitos y que "\gcd(e, \varphi(n)) = 1".

2. Codificación por bloques: Cada carácter del rango ASCII se representa con 3 dígitos y se agrupa en pares para formar bloques enteros "m" de 6 dígitos.

3. Manejo de longitud impar: Si la longitud "L" del mensaje original es impar, se añade un espacio ASCII ("032") como relleno al final. Durante el descifrado se valida la presencia de dicho relleno y se elimina únicamente ese carácter adicional.

4. Trazabilidad en interfaz: Muestra paso a paso los valores de "n", "\varphi(n)", llave pública "(e, n)", llave privada "(d, n)", códigos ASCII, bloques numéricos "m", longitud "L" y el estado del relleno tanto al encriptar como al desencriptar.

## Ejecución
No requiere librerías externas (utiliza únicamente la biblioteca estándar de Python 3):

- En la carpeta del proyecto (Si te tiene un editor de código) únicamente se ejecuta el archivo "interfaz.py".

- En bash se coloca el siguiente comando:
python interfaz.py