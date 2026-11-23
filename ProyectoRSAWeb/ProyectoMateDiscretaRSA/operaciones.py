from rsa import generar_claves, cifrar_bloque, descifrar_bloque
from conversion import texto_a_bloques, bloques_a_texto


def cifrar_mensaje(mensaje, p, q, e):
    # Generación de las claves RSA
    clave_publica, clave_privada = generar_claves(p, q, e)

    e_publico, n = clave_publica

    bloques, L = texto_a_bloques(mensaje)

    bloques_cifrados = []

    # Se cifra cada bloque usando RSA
    for bloque in bloques:
        cifrado = cifrar_bloque(bloque, e_publico, n)
        bloques_cifrados.append(cifrado)

    # Cada bloque cifrado debe ocupar 6 dígitos
    resultado = " ".join(
        str(bloque).zfill(6)
        for bloque in bloques_cifrados
    )

    return resultado, L


def descifrar_mensaje(cifrado, L, p, q, e):
    # Generación de las claves RSA
    clave_publica, clave_privada = generar_claves(p, q, e)
    
    d, n = clave_privada

    if isinstance(L, bool) or not isinstance(L, int) or L < 0:
        raise ValueError("L debe ser un entero no negativo.")

    bloques_texto = cifrado.split()

    # Se comprueba la cantidad de bloques
    cantidad_esperada = (L + 1) // 2

    if len(bloques_texto) != cantidad_esperada:
        raise ValueError(
            "La cantidad de bloques no coincide con L."
        )

    bloques_descifrados = []

    for bloque in bloques_texto:
        # Cada bloque cifrado debe tener 6 dígitos
        if len(bloque) != 6 or not all(
            "0" <= caracter <= "9" for caracter in bloque
        ):
            raise ValueError(
                "Cada bloque cifrado debe tener exactamente 6 dígitos."
            )

        numero = int(bloque)

        # El bloque cifrado debe ser menor que n
        if numero >= n:
            raise ValueError(
                "Un bloque cifrado es mayor o igual que n."
            )

        # Se descifra el bloque
        original = descifrar_bloque(numero, d, n)

        bloques_descifrados.append(original)

    # Se reconstruye el mensaje original
    mensaje = bloques_a_texto(bloques_descifrados, L)

    return mensaje