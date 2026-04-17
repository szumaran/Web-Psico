import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
# Debe ser SIEMPRE la primera instrucción de Streamlit
st.set_page_config(page_title="Sistema Psico-IA", page_icon="🧠", layout="wide")

# --- 2. CONFIGURACIÓN DE LA IA ---
def inicializar_ia():
    if "GEMINI_API_KEY" in st.secrets:
        try:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            # Usamos gemini-pro para evitar el error 404 del modelo flash
            return genai.GenerativeModel('gemini-3-flash')
        except Exception as e:
            st.error(f"Error al configurar la IA: {e}")
            return None
    else:
        st.error("❌ No se encontró GEMINI_API_KEY en los Secrets de Streamlit.")
        return None

model = inicializar_ia()

# --- 3. CONTROL DE ACCESO (LOGIN) ---
if "autenticado" not in st.session_state:
    st.title("🔐 Acceso al Sistema")
    st.subheader("Centro Psicopedagógico")
    
    with st.form("login_form"):
        usuario = st.text_input("Usuario")
        clave = st.text_input("Contraseña", type="password")
        submit = st.form_submit_button("Entrar")
        
        if submit:
            if usuario == "admin" and clave == "centro2026":
                st.session_state["autenticado"] = True
                st.rerun()
            else:
                st.error("❌ Usuario o contraseña incorrectos")
    st.stop()

# --- 4. INTERFAZ DE USUARIO (SOLO SI ESTÁ AUTENTICADO) ---
# Botón para cerrar sesión en la barra lateral
if st.sidebar.button("Cerrar Sesión"):
    del st.session_state["autenticado"]
    st.rerun()

st.title("🧠 Generador Inteligente de Informes")
st.write("Herramienta de redacción asistida por Inteligencia Artificial.")
st.markdown("---")

# Creación de dos columnas para el diseño
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📥 Entrada de Datos")
    nombre_alumno = st.text_input("Nombre completo del alumno")
    edad_alumno = st.number_input("Edad", min_value=0, max_value=18, value=8)
    curso_alumno = st.selectbox("Curso", [
        "Kinder", "1° Básico", "2° Básico", "3° Básico", 
        "4° Básico", "5° Básico", "6° Básico", "7° Básico", 
        "8° Básico", "I Medio", "II Medio", "III Medio", "IV Medio"
    ])
    
    st.subheader("Observaciones")
    notas_clinicas = st.text_area("Notas de la sesión", height=250, 
                                 placeholder="Escriba aquí sus observaciones...")
    
    boton_generar = st.button("✨ Generar Informe")

with col2:
    st.header("📄 Informe Sugerido")
    if boton_generar:
        if nombre_alumno and notas_clinicas:
            if model:
                with st.spinner("La IA está trabajando en el informe..."):
                    try:
                        # Prompt estructurado para calidad profesional
                        prompt_instruccion = f"""
                        Actúa como un Psicopedagogo experto. 
                        Redacta un informe para el alumno {nombre_alumno}, de {edad_alumno} años, curso {curso_alumno}.
                        Basado en estas observaciones: {notas_clinicas}
                        
                        Formato requerido:
                        1. IDENTIFICACIÓN
                        2. ANÁLISIS CONDUCTUAL
                        3. SÍNTESIS TÉCNICA
                        4. RECOMENDACIONES
                        """
                        
                        resultado = model.generate_content(prompt_instruccion)
                        
                        if resultado.text:
                            st.success("¡Informe generado!")
                            st.markdown(resultado.text)
                            
                            # Opción de descarga
                            st.download_button(
                                label="📥 Descargar TXT",
                                data=resultado.text,
                                file_name=f"Informe_{nombre_alumno}.txt",
                                mime="text/plain"
                            )
                    except Exception as e:
                        st.error(f"Error de la IA: {e}")
            else:
                st.error("El modelo no pudo iniciarse. Revisa tu API Key.")
        else:
            st.warning("⚠️ Por favor, ingresa el nombre y las notas.")
    else:
        st.info("Ingresa los datos a la izquierda para ver la propuesta de informe.")

st.markdown("---")
st.caption("© 2026 Centro Psicopedagógico")
