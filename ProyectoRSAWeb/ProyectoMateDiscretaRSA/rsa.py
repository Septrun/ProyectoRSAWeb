"""
Núcleo matemático RSA - Matemática Discreta
Catedrático: Mario Castillo
Integrantes: Diego Ayala, Juan José Mazariegos
"""

def _verificar_entero(nombre, valor):
    # Se verifica que el valor sea estrictamente un entero
    if isinstance(valor, bool) or not isinstance(valor, int):
        raise TypeError(f"'{nombre}' debe ser un número entero.")


def es_primo(n):
    _verificar_entero("n", n)
    
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    # Se comprueba la primalidad por división de impares hasta la raíz cuadrada
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def mcd(a, b):
    _verificar_entero("a", a)
    _verificar_entero("b", b)

    # Se normaliza a valores positivos para el algoritmo de Euclides
    a = abs(a)
    b = abs(b)

    # Algoritmo de Euclides para el cálculo del MCD
    while b != 0:
        a, b = b, a % b
    return a


def inverso_modular(e, phi):
    _verificar_entero("e", e)
    _verificar_entero("phi", phi)
    
    if phi <= 0:
        raise ValueError("phi debe ser un entero positivo.")
    
    # Algoritmo de Euclides extendido para encontrar el inverso multiplicativo    
    r0, r1 = e, phi
    x0, x1 = 1, 0
    
    while r1 != 0:
        cociente = r0 // r1
        r0, r1 = r1, r0 - cociente * r1
        x0, x1 = x1, x0 - cociente * x1
        
    if r0 != 1:
        raise ValueError("El inverso modular no existe (MCD(e, phi) debe ser 1).")
    
    d = x0 % phi
    if not (1 <= d < phi):
        raise ValueError("El exponente privado d está fuera del rango válido.")
        
    return d


def exponenciacion_modular(base, exponente, modulo):
    _verificar_entero("base", base)
    _verificar_entero("exponente", exponente)
    _verificar_entero("modulo", modulo)
    
    if modulo <= 0:
        raise ValueError("El módulo debe ser un entero positivo mayor que cero.")
    if exponente < 0:
        raise ValueError("El exponente debe ser mayor o igual a cero.")

    # Exponenciación binaria rápida   
    resultado = 1 % modulo
    base = base % modulo
    
    while exponente > 0:
        if exponente % 2 == 1:
            resultado = (resultado * base) % modulo
        base = (base * base) % modulo
        exponente //= 2
        
    return resultado


def validar_parametros(p, q, e):
    _verificar_entero("p", p)
    _verificar_entero("q", q)
    _verificar_entero("e", e)
    
    if not es_primo(p) or not es_primo(q):
        raise ValueError("p y q deben ser números primos.")
    
    if p == q:
        raise ValueError("p y q deben ser primos distintos.")
        
    n = p * q
    # Validación del rango de n
    if not (126126 < n < 1000000):
        raise ValueError("El producto n (p*q) está fuera del rango permitido (126126 < n < 1000000).")
        
    phi = (p - 1) * (q - 1)
    
    if e <= 1 or mcd(e, phi) != 1:
        raise ValueError("e debe ser mayor a 1 y coprimo con phi.")
        
    return n, phi


def generar_claves(p, q, e):
    n, phi = validar_parametros(p, q, e)
    d = inverso_modular(e, phi)
    
    clave_publica = (e, n)
    clave_privada = (d, n)
    
    return clave_publica, clave_privada


def cifrar_bloque(m, e, n):
    _verificar_entero("m", m)
    _verificar_entero("e", e)
    _verificar_entero("n", n)
    
    if n <= 0:
        raise ValueError("El módulo n debe ser positivo.")
    if e <= 0:
        raise ValueError("El exponente de cifrado e debe ser positivo.")
    if not (0 <= m < n):
        raise ValueError("El bloque m debe cumplir: 0 <= m < n.")
        
    return exponenciacion_modular(m, e, n)


def descifrar_bloque(c, d, n):
    _verificar_entero("c", c)
    _verificar_entero("d", d)
    _verificar_entero("n", n)
    
    if n <= 0:
        raise ValueError("El módulo n debe ser positivo.")
    if d <= 0:
        raise ValueError("El exponente privado d debe ser positivo.")
    if not (0 <= c < n):
        raise ValueError("El bloque cifrado c debe cumplir: 0 <= c < n.")
        
    return exponenciacion_modular(c, d, n)