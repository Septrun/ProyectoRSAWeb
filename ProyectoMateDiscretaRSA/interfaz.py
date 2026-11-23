import tkinter as tk
from tkinter import ttk, messagebox
from operaciones import cifrar_mensaje, descifrar_mensaje
from conversion import texto_a_ascii, texto_a_bloques
from rsa import generar_claves, validar_parametros, inverso_modular, descifrar_bloque


ventana = tk.Tk()
ventana.title("Sistema Criptográfico RSA - MM2015")
ventana.geometry("1120x760")
ventana.minsize(920, 620)
ventana.configure(bg="#EEF2F6")

header = tk.Frame(ventana, bg="#0F172A", pady=16, padx=28)
header.pack(fill="x")

header_izq = tk.Frame(header, bg="#0F172A")
header_izq.pack(side="left")

titulo = tk.Label(
    header_izq,
    text="SISTEMA CRIPTOGRÁFICO RSA",
    font=("Segoe UI", 17, "bold"),
    bg="#0F172A",
    fg="#FFFFFF"
)
titulo.pack(anchor="w")

subtitulo = tk.Label(
    header_izq,
    text="Cifrado y descifrado por bloques ASCII  |  Grupo 6",
    font=("Segoe UI", 9),
    bg="#0F172A",
    fg="#94A3B8"
)
subtitulo.pack(anchor="w", pady=(2, 0))

badge_curso = tk.Label(
    header,
    text="MM2015  |  Matemática Discreta 1",
    font=("Segoe UI", 9, "bold"),
    bg="#1E293B",
    fg="#93C5FD",
    padx=12,
    pady=6
)
badge_curso.pack(side="right", anchor="center")

canvas = tk.Canvas(ventana, bg="#EEF2F6", highlightthickness=0)
scrollbar = ttk.Scrollbar(ventana, orient="vertical", command=canvas.yview)
contenido = tk.Frame(canvas, bg="#EEF2F6")


def actualizar_scroll(event):
    canvas.configure(scrollregion=canvas.bbox("all"))


contenido.bind("<Configure>", actualizar_scroll)

ventana_contenido = canvas.create_window((0, 0), window=contenido, anchor="nw")


def ajustar_ancho(event):
    canvas.itemconfigure(ventana_contenido, width=event.width)


canvas.bind("<Configure>", ajustar_ancho)
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)


def desplazar_mouse(event):
    canvas.yview_scroll(int(-event.delta / 120), "units")


canvas.bind_all("<MouseWheel>", desplazar_mouse)

# Parámetros y generación de llaves

frame_parametros = tk.Frame(
    contenido,
    bg="#FFFFFF",
    highlightbackground="#CBD5E1",
    highlightthickness=1,
    padx=20,
    pady=16
)
frame_parametros.pack(fill="x", padx=28, pady=(16, 0))

encabezado_params = tk.Frame(frame_parametros, bg="#FFFFFF")
encabezado_params.pack(fill="x", pady=(0, 12))

tk.Frame(encabezado_params, bg="#2563EB", width=4, height=18).pack(side="left", padx=(0, 10))
tk.Label(
    encabezado_params,
    text="1. Parámetros y Generación de Llaves RSA",
    font=("Segoe UI", 11, "bold"),
    bg="#FFFFFF",
    fg="#0F172A"
).pack(side="left")

fila_superior = tk.Frame(frame_parametros, bg="#FFFFFF")
fila_superior.pack(fill="x")

for col in range(3):
    fila_superior.columnconfigure(col, weight=1)

tk.Label(
    fila_superior,
    text="Primo p",
    font=("Segoe UI", 9, "bold"),
    bg="#FFFFFF",
    fg="#475569"
).grid(row=0, column=0, sticky="w", padx=(0, 10), pady=(0, 4))

entrada_p = tk.Entry(
    fila_superior,
    font=("Consolas", 11),
    bg="#FFFFFF",
    fg="#0F172A",
    relief="solid",
    bd=1
)
entrada_p.grid(row=1, column=0, sticky="ew", padx=(0, 10), ipady=4)

tk.Label(
    fila_superior,
    text="Primo q",
    font=("Segoe UI", 9, "bold"),
    bg="#FFFFFF",
    fg="#475569"
).grid(row=0, column=1, sticky="w", padx=5, pady=(0, 4))

entrada_q = tk.Entry(
    fila_superior,
    font=("Consolas", 11),
    bg="#FFFFFF",
    fg="#0F172A",
    relief="solid",
    bd=1
)
entrada_q.grid(row=1, column=1, sticky="ew", padx=5, ipady=4)

tk.Label(
    fila_superior,
    text="Exponente público e",
    font=("Segoe UI", 9, "bold"),
    bg="#FFFFFF",
    fg="#475569"
).grid(row=0, column=2, sticky="w", padx=(10, 14), pady=(0, 4))

entrada_e = tk.Entry(
    fila_superior,
    font=("Consolas", 11),
    bg="#FFFFFF",
    fg="#0F172A",
    relief="solid",
    bd=1
)
entrada_e.grid(row=1, column=2, sticky="ew", padx=(10, 14), ipady=4)

entrada_p.insert(0, "367")
entrada_q.insert(0, "373")
entrada_e.insert(0, "17")

acciones_claves = tk.Frame(fila_superior, bg="#FFFFFF")
acciones_claves.grid(row=1, column=3, sticky="e")


def calcular_claves():
    try:
        texto_p = entrada_p.get().strip()
        texto_q = entrada_q.get().strip()
        texto_e = entrada_e.get().strip()

        if not texto_p or not texto_q or not texto_e:
            raise ValueError("Debe completar todos los parámetros RSA.")

        try:
            p = int(texto_p)
            q = int(texto_q)
            e = int(texto_e)
        except ValueError:
            raise ValueError("Los parámetros p, q y e deben ser números enteros.")

        n, phi = validar_parametros(p, q, e)
        clave_publica, clave_privada = generar_claves(p, q, e)
        d, _ = clave_privada

        resultado_n.config(text=str(n))
        resultado_phi.config(text=str(phi))
        resultado_publica.config(text=f"(e={e}, n={n})")
        resultado_privada.config(text=f"(d={d}, n={n})")

        messagebox.showinfo("Claves generadas", "Las claves RSA se generaron correctamente.")

    except (ValueError, TypeError) as error:
        resultado_n.config(text="---")
        resultado_phi.config(text="---")
        resultado_publica.config(text="---")
        resultado_privada.config(text="---")
        messagebox.showerror("Error en los parámetros", str(error))


def limpiar_todo():
    resultado_n.config(text="---")
    resultado_phi.config(text="---")
    resultado_publica.config(text="---")
    resultado_privada.config(text="---")

    entrada_mensaje.delete("1.0", tk.END)
    resultado_ascii.config(text="Códigos ASCII: ---\nBloques m:     ---")
    resultado_longitud.config(text="Longitud L: ---")
    resultado_relleno.config(text="Relleno: ---")

    salida_cifrado.config(state="normal")
    salida_cifrado.delete("1.0", tk.END)
    salida_cifrado.config(state="disabled")

    entrada_cifrado.delete("1.0", tk.END)
    entrada_longitud.delete(0, tk.END)
    resultado_detalle_dec.config(text="Exponente d: ---  |  Relleno: ---\nBloques m:   ---")

    salida_descifrado.config(state="normal")
    salida_descifrado.delete("1.0", tk.END)
    salida_descifrado.config(state="disabled")


boton_generar = tk.Button(
    acciones_claves,
    text="GENERAR CLAVES",
    font=("Segoe UI", 9, "bold"),
    bg="#2563EB",
    fg="white",
    activebackground="#1D4ED8",
    activeforeground="white",
    relief="flat",
    padx=16,
    pady=7,
    cursor="hand2",
    command=calcular_claves
)
boton_generar.pack(side="left", padx=(0, 8))

boton_limpiar = tk.Button(
    acciones_claves,
    text="LIMPIAR",
    font=("Segoe UI", 9, "bold"),
    bg="#E2E8F0",
    fg="#475569",
    activebackground="#CBD5E1",
    activeforeground="#0F172A",
    relief="flat",
    padx=12,
    pady=7,
    cursor="hand2",
    command=limpiar_todo
)
boton_limpiar.pack(side="left")

grid_metricas = tk.Frame(frame_parametros, bg="#FFFFFF")
grid_metricas.pack(fill="x", pady=(14, 0))

for col in range(4):
    grid_metricas.columnconfigure(col, weight=1)

caja_n = tk.Frame(grid_metricas, bg="#F8FAFC", highlightbackground="#E2E8F0", highlightthickness=1, padx=12, pady=8)
caja_n.grid(row=0, column=0, sticky="ew", padx=(0, 8))
tk.Label(caja_n, text="MÓDULO n = p · q", font=("Segoe UI", 8, "bold"), bg="#F8FAFC", fg="#64748B").pack(anchor="w")
resultado_n = tk.Label(caja_n, text="---", font=("Consolas", 10, "bold"), bg="#F8FAFC", fg="#0F172A")
resultado_n.pack(anchor="w", pady=(2, 0))

caja_phi = tk.Frame(grid_metricas, bg="#F8FAFC", highlightbackground="#E2E8F0", highlightthickness=1, padx=12, pady=8)
caja_phi.grid(row=0, column=1, sticky="ew", padx=4)
tk.Label(caja_phi, text="FUNCIÓN φ(n) = (p-1)(q-1)", font=("Segoe UI", 8, "bold"), bg="#F8FAFC", fg="#64748B").pack(anchor="w")
resultado_phi = tk.Label(caja_phi, text="---", font=("Consolas", 10, "bold"), bg="#F8FAFC", fg="#0F172A")
resultado_phi.pack(anchor="w", pady=(2, 0))

caja_pub = tk.Frame(grid_metricas, bg="#F8FAFC", highlightbackground="#E2E8F0", highlightthickness=1, padx=12, pady=8)
caja_pub.grid(row=0, column=2, sticky="ew", padx=4)
tk.Label(caja_pub, text="LLAVE PÚBLICA (e, n)", font=("Segoe UI", 8, "bold"), bg="#F8FAFC", fg="#64748B").pack(anchor="w")
resultado_publica = tk.Label(caja_pub, text="---", font=("Consolas", 10, "bold"), bg="#F8FAFC", fg="#15803D")
resultado_publica.pack(anchor="w", pady=(2, 0))

caja_priv = tk.Frame(grid_metricas, bg="#F8FAFC", highlightbackground="#E2E8F0", highlightthickness=1, padx=12, pady=8)
caja_priv.grid(row=0, column=3, sticky="ew", padx=(8, 0))
tk.Label(caja_priv, text="LLAVE PRIVADA (d, n)", font=("Segoe UI", 8, "bold"), bg="#F8FAFC", fg="#64748B").pack(anchor="w")
resultado_privada = tk.Label(caja_priv, text="---", font=("Consolas", 10, "bold"), bg="#F8FAFC", fg="#B45309")
resultado_privada.pack(anchor="w", pady=(2, 0))

# Operaciones de cifrado y descifrado

columnas_trabajo = tk.Frame(contenido, bg="#EEF2F6")
columnas_trabajo.pack(fill="both", expand=True, padx=28, pady=(16, 24))
columnas_trabajo.columnconfigure(0, weight=1, uniform="grupo")
columnas_trabajo.columnconfigure(1, weight=1, uniform="grupo")

# Cifrado

frame_encriptacion = tk.Frame(
    columnas_trabajo,
    bg="#FFFFFF",
    highlightbackground="#CBD5E1",
    highlightthickness=1,
    padx=20,
    pady=16
)
frame_encriptacion.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

encabezado_enc = tk.Frame(frame_encriptacion, bg="#FFFFFF")
encabezado_enc.pack(fill="x", pady=(0, 12))

tk.Frame(encabezado_enc, bg="#15803D", width=4, height=18).pack(side="left", padx=(0, 10))
tk.Label(
    encabezado_enc,
    text="2. Encriptación de Mensajes",
    font=("Segoe UI", 11, "bold"),
    bg="#FFFFFF",
    fg="#0F172A"
).pack(side="left")

tk.Label(
    frame_encriptacion,
    text="Mensaje original M (ASCII imprimible 32-126)",
    font=("Segoe UI", 9, "bold"),
    bg="#FFFFFF",
    fg="#475569"
).pack(anchor="w", pady=(0, 4))

entrada_mensaje = tk.Text(
    frame_encriptacion,
    height=3,
    font=("Consolas", 11),
    wrap="word",
    bg="#FFFFFF",
    fg="#0F172A",
    relief="solid",
    bd=1,
    padx=8,
    pady=6
)
entrada_mensaje.pack(fill="x")


def encriptar_desde_interfaz():
    try:
        texto_p = entrada_p.get().strip()
        texto_q = entrada_q.get().strip()
        texto_e = entrada_e.get().strip()

        if not texto_p or not texto_q or not texto_e:
            raise ValueError("Debe completar todos los parámetros RSA.")

        try:
            p = int(texto_p)
            q = int(texto_q)
            e = int(texto_e)
        except ValueError:
            raise ValueError("Los parámetros p, q y e deben ser números enteros.")

        n, phi = validar_parametros(p, q, e)

        mensaje = entrada_mensaje.get("1.0", "end-1c")
        if mensaje == "":
            raise ValueError("Debe ingresar un mensaje para encriptar.")

        bloques, L = texto_a_bloques(mensaje)
        cifrado, L = cifrar_mensaje(mensaje, p, q, e)

        resultado_n.config(text=str(n))
        resultado_phi.config(text=str(phi))
        resultado_publica.config(text=f"(e={e}, n={n})")

        codigos_formateados = " ".join(texto_a_ascii(mensaje))

        lista_bloques = []
        for bloque in bloques:
            lista_bloques.append(str(bloque).zfill(6))
        bloques_formateados = " ".join(lista_bloques)

        resultado_ascii.config(
            text=(
                f"Códigos ASCII: {codigos_formateados}\n"
                f"Bloques m:     {bloques_formateados}"
            )
        )
        resultado_longitud.config(text=f"Longitud L: {L}")

        if L % 2 != 0:
            resultado_relleno.config(text="Relleno: Sí (espacio 032)")
        else:
            resultado_relleno.config(text="Relleno: No requerido")

        salida_cifrado.config(state="normal")
        salida_cifrado.delete("1.0", tk.END)
        salida_cifrado.insert("1.0", cifrado)
        salida_cifrado.config(state="disabled")

        messagebox.showinfo("Encriptación exitosa", "El mensaje fue encriptado correctamente.")

    except (ValueError, TypeError) as error:
        resultado_ascii.config(text="Códigos ASCII: ---\nBloques m:     ---")
        resultado_longitud.config(text="Longitud L: ---")
        resultado_relleno.config(text="Relleno: ---")

        salida_cifrado.config(state="normal")
        salida_cifrado.delete("1.0", tk.END)
        salida_cifrado.config(state="disabled")

        messagebox.showerror("Error de encriptación", str(error))


def copiar_cifrado():
    texto_c = salida_cifrado.get("1.0", "end-1c").strip()
    if texto_c:
        ventana.clipboard_clear()
        ventana.clipboard_append(texto_c)
        messagebox.showinfo("Copiado", "Cifrado C copiado al portapapeles.")


def transferir_a_desencriptar():
    texto_c = salida_cifrado.get("1.0", "end-1c").strip()
    texto_l = resultado_longitud.cget("text").replace("Longitud L:", "").strip()
    if texto_c and texto_l != "---":
        entrada_cifrado.delete("1.0", tk.END)
        entrada_cifrado.insert("1.0", texto_c)
        entrada_longitud.delete(0, tk.END)
        entrada_longitud.insert(0, texto_l)


barra_btn_enc = tk.Frame(frame_encriptacion, bg="#FFFFFF")
barra_btn_enc.pack(fill="x", pady=12)

boton_encriptar = tk.Button(
    barra_btn_enc,
    text="ENCRIPTAR MENSAJE",
    font=("Segoe UI", 9, "bold"),
    bg="#15803D",
    fg="white",
    activebackground="#166534",
    activeforeground="white",
    relief="flat",
    padx=16,
    pady=7,
    cursor="hand2",
    command=encriptar_desde_interfaz
)
boton_encriptar.pack(side="left", padx=(0, 8))

boton_transferir = tk.Button(
    barra_btn_enc,
    text="Transferir C y L →",
    font=("Segoe UI", 9, "bold"),
    bg="#E2E8F0",
    fg="#0F172A",
    activebackground="#CBD5E1",
    activeforeground="#0F172A",
    relief="flat",
    padx=12,
    pady=7,
    cursor="hand2",
    command=transferir_a_desencriptar
)
boton_transferir.pack(side="left")

panel_detalles_enc = tk.Frame(
    frame_encriptacion,
    bg="#F8FAFC",
    highlightbackground="#E2E8F0",
    highlightthickness=1,
    padx=12,
    pady=10
)
panel_detalles_enc.pack(fill="x", pady=(0, 12))

fila_meta = tk.Frame(panel_detalles_enc, bg="#F8FAFC")
fila_meta.pack(fill="x", pady=(0, 6))

resultado_longitud = tk.Label(
    fila_meta,
    text="Longitud L: ---",
    font=("Segoe UI", 9, "bold"),
    bg="#F8FAFC",
    fg="#2563EB"
)
resultado_longitud.pack(side="left", padx=(0, 18))

resultado_relleno = tk.Label(
    fila_meta,
    text="Relleno: ---",
    font=("Segoe UI", 9, "bold"),
    bg="#F8FAFC",
    fg="#475569"
)
resultado_relleno.pack(side="left")

resultado_ascii = tk.Label(
    panel_detalles_enc,
    text="Códigos ASCII: ---\nBloques m:     ---",
    font=("Consolas", 9),
    bg="#F8FAFC",
    fg="#0F172A",
    wraplength=440,
    justify="left"
)
resultado_ascii.pack(anchor="w")

fila_titulo_c = tk.Frame(frame_encriptacion, bg="#FFFFFF")
fila_titulo_c.pack(fill="x", pady=(0, 4))

tk.Label(
    fila_titulo_c,
    text="Mensaje cifrado C",
    font=("Segoe UI", 9, "bold"),
    bg="#FFFFFF",
    fg="#0F172A"
).pack(side="left")

btn_copiar = tk.Button(
    fila_titulo_c,
    text="Copiar C",
    font=("Segoe UI", 8, "bold"),
    bg="#F8FAFC",
    fg="#2563EB",
    activebackground="#E2E8F0",
    relief="flat",
    padx=8,
    pady=2,
    cursor="hand2",
    command=copiar_cifrado
)
btn_copiar.pack(side="right")

salida_cifrado = tk.Text(
    frame_encriptacion,
    height=3,
    font=("Consolas", 11, "bold"),
    wrap="word",
    bg="#F8FAFC",
    fg="#15803D",
    relief="solid",
    bd=1,
    padx=8,
    pady=6,
    state="disabled"
)
salida_cifrado.pack(fill="x")

# Descifrado

frame_desencriptacion = tk.Frame(
    columnas_trabajo,
    bg="#FFFFFF",
    highlightbackground="#CBD5E1",
    highlightthickness=1,
    padx=20,
    pady=16
)
frame_desencriptacion.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

encabezado_dec = tk.Frame(frame_desencriptacion, bg="#FFFFFF")
encabezado_dec.pack(fill="x", pady=(0, 12))

tk.Frame(encabezado_dec, bg="#B45309", width=4, height=18).pack(side="left", padx=(0, 10))
tk.Label(
    encabezado_dec,
    text="3. Desencriptación de Mensajes",
    font=("Segoe UI", 11, "bold"),
    bg="#FFFFFF",
    fg="#0F172A"
).pack(side="left")

tk.Label(
    frame_desencriptacion,
    text="Mensaje cifrado C (bloques de 6 dígitos separados por espacio)",
    font=("Segoe UI", 9, "bold"),
    bg="#FFFFFF",
    fg="#475569"
).pack(anchor="w", pady=(0, 4))

entrada_cifrado = tk.Text(
    frame_desencriptacion,
    height=3,
    font=("Consolas", 11),
    wrap="word",
    bg="#FFFFFF",
    fg="#0F172A",
    relief="solid",
    bd=1,
    padx=8,
    pady=6
)
entrada_cifrado.pack(fill="x")

fila_l_btn = tk.Frame(frame_desencriptacion, bg="#FFFFFF")
fila_l_btn.pack(fill="x", pady=12)

tk.Label(
    fila_l_btn,
    text="Longitud L:",
    font=("Segoe UI", 9, "bold"),
    bg="#FFFFFF",
    fg="#475569"
).pack(side="left", padx=(0, 8))

entrada_longitud = tk.Entry(
    fila_l_btn,
    width=10,
    font=("Consolas", 11),
    bg="#FFFFFF",
    fg="#0F172A",
    relief="solid",
    bd=1
)
entrada_longitud.pack(side="left", padx=(0, 14), ipady=3)


def desencriptar_desde_interfaz():
    try:
        texto_p = entrada_p.get().strip()
        texto_q = entrada_q.get().strip()
        texto_e = entrada_e.get().strip()

        if not texto_p or not texto_q or not texto_e:
            raise ValueError("Debe completar todos los parámetros RSA.")

        try:
            p = int(texto_p)
            q = int(texto_q)
            e = int(texto_e)
        except ValueError:
            raise ValueError("Los parámetros p, q y e deben ser enteros.")

        n, phi = validar_parametros(p, q, e)

        cifrado = entrada_cifrado.get("1.0", "end-1c")
        if not cifrado.strip():
            raise ValueError("Debe ingresar un mensaje cifrado.")

        texto_L = entrada_longitud.get().strip()
        if not texto_L:
            raise ValueError("Debe ingresar la longitud original L.")

        try:
            L = int(texto_L)
        except ValueError:
            raise ValueError("La longitud L debe ser un número entero.")

        mensaje = descifrar_mensaje(cifrado, L, p, q, e)

        d = inverso_modular(e, phi)
        bloques_m = []
        for bloque in cifrado.split():
            valor_m = descifrar_bloque(int(bloque), d, n)
            bloques_m.append(str(valor_m).zfill(6))

        resultado_n.config(text=str(n))
        resultado_phi.config(text=str(phi))
        resultado_publica.config(text=f"(e={e}, n={n})")
        resultado_privada.config(text=f"(d={d}, n={n})")

        if L % 2 != 0:
            estado_relleno = "Retirado (032 final)"
        else:
            estado_relleno = "Sin relleno (L par)"

        resultado_detalle_dec.config(
            text=(
                f"Exponente d: {d}  |  Relleno: {estado_relleno}\n"
                f"Bloques m:   {' '.join(bloques_m)}"
            )
        )

        salida_descifrado.config(state="normal")
        salida_descifrado.delete("1.0", tk.END)
        salida_descifrado.insert("1.0", mensaje)
        salida_descifrado.config(state="disabled")

        messagebox.showinfo("Desencriptación exitosa", "El mensaje fue recuperado correctamente.")

    except (ValueError, TypeError) as error:
        resultado_detalle_dec.config(text="Exponente d: ---  |  Relleno: ---\nBloques m:   ---")
        salida_descifrado.config(state="normal")
        salida_descifrado.delete("1.0", tk.END)
        salida_descifrado.config(state="disabled")

        messagebox.showerror("Error de desencriptación", str(error))


boton_desencriptar = tk.Button(
    fila_l_btn,
    text="DESENCRIPTAR MENSAJE",
    font=("Segoe UI", 9, "bold"),
    bg="#B45309",
    fg="white",
    activebackground="#92400E",
    activeforeground="white",
    relief="flat",
    padx=16,
    pady=7,
    cursor="hand2",
    command=desencriptar_desde_interfaz
)
boton_desencriptar.pack(side="left")

panel_detalles_dec = tk.Frame(
    frame_desencriptacion,
    bg="#F8FAFC",
    highlightbackground="#E2E8F0",
    highlightthickness=1,
    padx=12,
    pady=10
)
panel_detalles_dec.pack(fill="x", pady=(0, 12))

resultado_detalle_dec = tk.Label(
    panel_detalles_dec,
    text="Exponente d: ---  |  Relleno: ---\nBloques m:   ---",
    font=("Consolas", 9),
    bg="#F8FAFC",
    fg="#0F172A",
    wraplength=440,
    justify="left"
)
resultado_detalle_dec.pack(anchor="w")

tk.Label(
    frame_desencriptacion,
    text="Mensaje recuperado M",
    font=("Segoe UI", 9, "bold"),
    bg="#FFFFFF",
    fg="#0F172A"
).pack(anchor="w", pady=(0, 4))

salida_descifrado = tk.Text(
    frame_desencriptacion,
    height=3,
    font=("Consolas", 11, "bold"),
    wrap="word",
    bg="#F8FAFC",
    fg="#0F172A",
    relief="solid",
    bd=1,
    padx=8,
    pady=6,
    state="disabled"
)
salida_descifrado.pack(fill="x")

ventana.mainloop()