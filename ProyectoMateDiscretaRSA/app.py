import streamlit as st

from conversion import texto_a_ascii, texto_a_bloques
from operaciones import cifrar_mensaje, descifrar_mensaje
from rsa import (
    validar_parametros,
    generar_claves,
    inverso_modular,
    descifrar_bloque,
)

st.set_page_config(
    page_title="Sistema Criptográfico RSA | MM2015",
    layout="wide",
)

st.markdown(
    """
    <style>
    .stApp { background: #f1f5f9; color: #1e293b; }
    [data-testid="stHeader"] { background: rgba(241,245,249,0.9); }
    .main .block-container { max-width: 1120px; padding-top: 2rem; }
    [data-testid="stAppViewContainer"] *,
    [data-testid="stSidebar"] * { color: #1e293b; }
    .hero { background: #0f172a; color: white; padding: 1.5rem 1.8rem;
            border-radius: 14px; margin-bottom: 1.2rem; }
    .hero h1 { color: white !important; margin: 0; font-size: 1.7rem; }
    .hero p { color: #cbd5e1 !important; margin: .35rem 0 0 0; }
    [data-testid="stTextInput"] input,
    [data-testid="stTextArea"] textarea,
    [data-testid="stNumberInput"] input {
        background: white !important;
        color: #111827 !important;
        -webkit-text-fill-color: #111827 !important;
    }
    [data-testid="stTextInput"] label,
    [data-testid="stTextArea"] label,
    [data-testid="stNumberInput"] label,
    [data-testid="stWidgetLabel"] {
        color: #1e293b !important;
    }
    [data-testid="stMetricValue"],
    [data-testid="stMetricLabel"] { color: #1e293b !important; }
    [data-testid="stTab"] { color: #1e293b !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="hero"><h1>SISTEMA CRIPTOGRÁFICO RSA</h1>'
    '<p>Cifrado y descifrado por bloques ASCII &nbsp; | &nbsp; Grupo 6 · MM2015 Matemática Discreta 1</p></div>',
    unsafe_allow_html=True,
)

if "cifrado" not in st.session_state:
    st.session_state.cifrado = ""
if "longitud" not in st.session_state:
    st.session_state.longitud = 0
if "mensaje_original" not in st.session_state:
    st.session_state.mensaje_original = ""
if "entrada_cifrado_web" not in st.session_state:
    st.session_state.entrada_cifrado_web = st.session_state.cifrado
if "entrada_longitud_web" not in st.session_state:
    st.session_state.entrada_longitud_web = int(st.session_state.longitud)

st.subheader("1. Parámetros y generación de llaves RSA")
col_p, col_q, col_e = st.columns(3)
with col_p:
    p = st.number_input("Primo p", min_value=2, value=367, step=1)
with col_q:
    q = st.number_input("Primo q", min_value=2, value=373, step=1)
with col_e:
    e = st.number_input("Exponente público e", min_value=2, value=17, step=1)

try:
    n, phi = validar_parametros(int(p), int(q), int(e))
    clave_publica, clave_privada = generar_claves(int(p), int(q), int(e))
    d, _ = clave_privada
    st.success("Los parámetros son válidos y las llaves se generaron correctamente.")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Módulo n", f"{n:,}")
    k2.metric("φ(n)", f"{phi:,}")
    k3.metric("Llave pública (e, n)", f"({int(e)}, {n})")
    k4.metric("Llave privada (d, n)", f"({d}, {n})")
    parametros_validos = True
except (ValueError, TypeError) as error:
    st.error(str(error))
    parametros_validos = False
    d = None
    n = None
    phi = None

st.divider()
tab_cifrar, tab_descifrar = st.tabs(["2. Encriptar mensaje", "3. Desencriptar mensaje"])

with tab_cifrar:
    st.write("Escribe un mensaje utilizando caracteres ASCII imprimibles (códigos 032 a 126).")
    mensaje = st.text_area("Mensaje M", height=110, placeholder="Escribe aquí el mensaje que deseas encriptar...")
    if st.button("ENCRIPTAR MENSAJE", type="primary", use_container_width=True, disabled=not parametros_validos):
        try:
            if mensaje == "":
                raise ValueError("Debe ingresar un mensaje para encriptar.")
            bloques, L = texto_a_bloques(mensaje)
            cifrado, L = cifrar_mensaje(mensaje, int(p), int(q), int(e))
            st.session_state.cifrado = cifrado
            st.session_state.longitud = L
            st.session_state.mensaje_original = mensaje
            st.session_state.bloques_originales = bloques
            st.session_state.codigos_ascii = texto_a_ascii(mensaje)
            st.success("El mensaje fue encriptado correctamente.")
        except (ValueError, TypeError) as error:
            st.error(str(error))

    if st.session_state.cifrado:
        st.markdown("**Resultado del proceso**")
        st.text_input("Códigos ASCII", value=" ".join(st.session_state.codigos_ascii), disabled=True)
        st.text_input("Bloques numéricos m", value=" ".join(str(x).zfill(6) for x in st.session_state.bloques_originales), disabled=True)
        r1, r2 = st.columns(2)
        r1.metric("Longitud original L", st.session_state.longitud)
        r2.metric("Relleno", "Sí · espacio 032" if st.session_state.longitud % 2 else "No requerido")
        st.text_area("Mensaje cifrado C", value=st.session_state.cifrado, height=100)
        if st.button("Transferir C y L al descifrado"):
            st.session_state.entrada_cifrado_web = st.session_state.cifrado
            st.session_state.entrada_longitud_web = int(st.session_state.longitud)
            st.info("Se transfirieron el mensaje cifrado y su longitud. Abre la pestaña de desencriptación.")

with tab_descifrar:
    st.write("Ingresa el texto cifrado y la longitud L del mensaje original.")
    cifrado = st.text_area("Mensaje cifrado C", height=100, key="entrada_cifrado_web")
    L = st.number_input("Longitud original L", min_value=0, step=1, key="entrada_longitud_web")
    if st.button("DESENCRIPTAR MENSAJE", type="primary", use_container_width=True, disabled=not parametros_validos):
        try:
            if not cifrado.strip():
                raise ValueError("Debe ingresar un mensaje cifrado.")
            mensaje_recuperado = descifrar_mensaje(cifrado, int(L), int(p), int(q), int(e))
            d_local = inverso_modular(int(e), int(phi))
            bloques_m = [
                str(descifrar_bloque(int(bloque), d_local, int(n))).zfill(6)
                for bloque in cifrado.split()
            ]
            st.success("El mensaje fue recuperado correctamente.")
            st.text_area("Mensaje recuperado M", value=mensaje_recuperado, height=100)
            det1, det2 = st.columns(2)
            det1.metric("Exponente privado d", d_local)
            det2.metric("Relleno", "Retirado · 032 final" if int(L) % 2 else "No utilizado")
            st.text_input("Bloques m recuperados", value=" ".join(bloques_m), disabled=True)
        except (ValueError, TypeError) as error:
            st.error(str(error))

st.divider()
with st.expander("Información del proyecto"):
    st.write(
        "Esta aplicación implementa RSA mediante aritmética modular y codificación por bloques ASCII. "
        "Cada carácter permitido se representa con tres dígitos y se agrupa en bloques de seis dígitos. "
        "Cuando la longitud del mensaje es impar, se agrega un espacio ASCII 032 como relleno y se retira al descifrar."
    )
    st.caption("Proyecto académico de Matemática Discreta 1 (MM2015) · Grupo 6")
