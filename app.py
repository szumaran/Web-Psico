import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURACIÓN INICIAL ---
st.set_page_config(page_title="Sistema Psico-IA", page_icon="🧠", layout="wide")

# --- 2. CONFIGURACIÓN DE IA (ESTABLE) ---
# Usamos st.secrets para la clave y configuramos el modelo Pro que es el más estable
if "GEMINI_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # Usamos gemini-pro que tiene 99% de compatibilidad
        model = genai.GenerativeModel('gemini-pro')
    except Exception as e:
        st.error(f"Error al configurar la IA: {e}")
else:
    st.error("⚠️ Falta la clave GEMINI_API_KEY en los Secrets de Streamlit.")

# --- 3. SISTEMA DE LOGIN ---
if "autenticado" not in st.session_state:
    st.title("🔐 Acceso al Sistema")
    st.subheader("Centro Psicopedagógico")
    
    with st.form("login"):
        user = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        if st.form_submit_button("Entrar"):
            if user == "admin" and password == "centro2026":
                st.session_state["autenticado"] = True
                st.rerun()
            else:
                st.error("❌ Credenciales incorrectas")
    st.stop()

# --- 4. INTERFAZ DE GENERACIÓN (Si está logueado) ---
st.title("🧠 Generador de Informes Inteligente")
st.write("Complete los datos para que la IA redacte el borrador del informe.")

if st.sidebar.button("Cerrar Sesión"):
    del st.session_state["autenticado"]
    st.rerun()

st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.header("📥 Entrada de Datos")
    nombre_alumno = st.text_input("Nombre completo del alumno")
    edad_alumno = st.number_input("Edad", min_value=0, max_value=18, value=8)
    curso_alumno = st.text_input("Curso")
    
    st.subheader("Observaciones Clínicas")
    notas = st.text_area("Escriba aquí sus notas desordenadas o resultados de tests", height=300,
                         placeholder="Ej: El alumno presenta dificultades en lectoescritura, se distrae fácil...")

    boton = st.button("✨ Generar Informe Profesional")

with col2:
    st.header("📄 Informe Sugerido")
    if boton:
        if nombre_alumno and notas:
            with st.spinner("La IA está redactando..."):
                try:
                    # Instrucción clara para evitar errores de contenido
                    prompt = f"""
                    Eres un experto psicopedagogo. 
                    Redacta un informe formal para el alumno {nombre_alumno}, de {edad_alumno} años, curso {curso_alumno}.
                    Usa estas notas: {notas}.
                    Estructura: 1. Identificación, 2. Análisis, 3. Recomendaciones.
                    """
                    
                    response = model.generate_content(prompt)
                    
                    if response.text:
                        st.success("¡Informe listo!")
                        st.markdown(response.text)
                        
                        # Botón de descarga
                        st.download_button(
                            label="📥 Descargar Informe (.txt)",
                            data=response.text,
                            file_name=f"Informe_{nombre_alumno}.txt",
                            mime="text/plain"
                        )
                except Exception as e:
                    st.error(f"Error de la IA: {e}")
                    st.info("Si el error es 404, prueba creando una NUEVA API Key en un proyecto nuevo en Google AI Studio.")
        else:
            st.warning("⚠️ Ingresa el nombre y las notas para continuar.")
    else:
        st.info("Complete los datos de la izquierda y presione 'Generar'.")

st.markdown("---")
st.caption("© 2026 Sistema de Apoyo Psicopedagógico")
