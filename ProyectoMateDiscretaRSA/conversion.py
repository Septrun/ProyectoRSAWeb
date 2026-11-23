def texto_a_ascii(mensaje):
    # Lista donde se guardan los códigos ASCII
    codigos = []

    for caracter in mensaje:
        # Conversión a ASCII
        valor = ord(caracter)

        if valor < 32 or valor > 126:
            raise ValueError(
                "El mensaje contiene caracteres no permitidos."
            )

        codigo = str(valor).zfill(3)

        codigos.append(codigo)

    return codigos

def texto_a_bloques(mensaje):
    # Conversión del mensaje a ASCII
    codigos = texto_a_ascii(mensaje)

    L = len(mensaje)

    if L % 2 != 0:
        codigos.append("032")

    # Lista para guardar los bloques numéricos
    bloques = []

    # Se recorren los códigos
    for i in range(0, len(codigos), 2):

        bloque = codigos[i] + codigos[i + 1]

        bloques.append(int(bloque))

    return bloques, L


def bloques_a_texto(bloques, L):
    # Se verifica que la longitud sea válida
    if not isinstance(L, int) or isinstance(L, bool) or L < 0:
        raise ValueError("La longitud L debe ser un entero no negativo.")

    # Se verifica la cantidad esperada de bloques
    cantidad_esperada = (L + 1) // 2

    if len(bloques) != cantidad_esperada:
        raise ValueError(
            "La cantidad de bloques no coincide con la longitud L."
        )

    # Se guardan los códigos ASCII recuperados
    caracteres = []

    for bloque in bloques:
        if isinstance(bloque, bool) or not isinstance(bloque, int):
            raise ValueError("Los bloques deben ser números enteros.")

        if bloque < 0 or bloque > 999999:
            raise ValueError("El bloque está fuera del rango permitido.")

        bloque_texto = str(bloque).zfill(6)

        codigo1 = int(bloque_texto[:3])
        codigo2 = int(bloque_texto[3:])

        caracteres.extend((codigo1, codigo2))

    # Si L es impar, se comprueba el espacio agregado como relleno
    if L % 2 != 0:
        if not caracteres or caracteres[-1] != 32:
            raise ValueError("El relleno del último bloque debe ser un espacio ASCII 032.")
        caracteres.pop()

    # Se validan los caracteres recuperados
    for codigo in caracteres:
        if codigo < 32 or codigo > 126:
            raise ValueError(
                "El bloque contiene un código ASCII no permitido."
            )

    # Se reconstruye el mensaje
    mensaje = ""

    for codigo in caracteres:
        mensaje += chr(codigo)

    return mensaje