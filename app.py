import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURACIÓN DE LA PÁGINA (Debe ser lo primero) ---
st.set_page_config(
    page_title="Sistema Psico-IA",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CONFIGURACIÓN DE SEGURIDAD (SECRETS) ---
def configurar_ia():
    try:
        if "GEMINI_API_KEY" in st.secrets:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            # Usamos gemini-1.5-flash que es el más moderno y rápido
            return genai.GenerativeModel('gemini-1.5-flash')
        else:
            st.error("❌ Error: No se encontró la clave 'GEMINI_API_KEY' en los Secrets de Streamlit.")
            return None
    except Exception as e:
        st.error(f"❌ Error al configurar Google AI: {e}")
        return None

model = configurar_ia()

# --- 3. SISTEMA DE LOGIN ---
def check_password():
    if "password_correct" not in st.session_state:
        st.title("🔐 Acceso al Sistema Psico-IA")
        st.subheader("Centro Psicopedagógico")
        
        with st.form("login_form"):
            user = st.text_input("Usuario")
            pw = st.text_input("Contraseña", type="password")
            submit = st.form_submit_button("Entrar")
            
            if submit:
                if user == "admin" and pw == "centro2026":
                    st.session_state["password_correct"] = True
                    st.rerun()
                else:
                    st.error("❌ Usuario o contraseña incorrectos")
        return False
    return True

# --- 4. APLICACIÓN PRINCIPAL ---
if check_password():
    # Barra lateral
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/1995/1995574.png", width=80)
    st.sidebar.title("Menú Principal")
    if st.sidebar.button("Cerrar Sesión"):
        del st.session_state["password_correct"]
        st.rerun()

    st.title("🧠 Generador Inteligente de Informes")
    st.write("Bienvenido al portal de redacción automatizada.")
    st.markdown("---")

    # Layout de dos columnas
    col1, col2 = st.columns([1, 1])

    with col1:
        st.header("📥 Datos del Alumno")
        nombre = st.text_input("Nombre completo del alumno", placeholder="Ej: Mateo Gómez")
        edad = st.number_input("Edad", min_value=0, max_value=18, value=8)
        curso = st.selectbox("Curso", [
            "Kinder", "1° Básico", "2° Básico", "3° Básico", 
            "4° Básico", "5° Básico", "6° Básico", "7° Básico", 
            "8° Básico", "I Medio", "II Medio", "III Medio", "IV Medio"
        ])
        
        st.subheader("Observaciones")
        obs = st.text_area("Notas de la sesión", height=250, 
                          placeholder="Escriba aquí sus notas, resultados de tests o conducta observada...")
        
        boton_generar = st.button("✨ Generar Informe Profesional")

    with col2:
        st.header("📄 Informe Sugerido")
        if boton_generar:
            if not nombre or not obs:
                st.warning("⚠️ Por favor, completa el nombre y las observaciones.")
            elif model is None:
                st.error("⚠️ El motor de IA no está configurado.")
            else:
                with st.spinner("La IA está analizando y redactando..."):
                    try:
                        # Prompt clínico mejorado
                        prompt = f"""
                        Eres un Psicopedagogo experto. 
                        Redacta un informe profesional para el alumno {nombre}, de {edad} años, del curso {curso}.
                        Notas de evaluación: {obs}
                        
                        Estructura el informe de forma profesional:
                        1. IDENTIFICACIÓN
                        2. ANÁLISIS DE LA EVALUACIÓN
                        3. SÍNTESIS TÉCNICA
                        4. RECOMENDACIONES PEDAGÓGICAS
                        
                        Usa un tono formal y preciso.
                        """
                        
                        response = model.generate_content(prompt)
                        
                        if response:
                            st.success("¡Informe generado con éxito!")
                            informe_texto = response.text
                            st.markdown(informe_texto)
                            
                            st.download_button(
                                label="📥 Descargar Informe (TXT)",
                                data=informe_texto,
                                file_name=f"Informe_{nombre}.txt",
                                mime="text/plain"
                            )
                    except Exception as e:
                        st.error(f"Ocurrió un error al generar el contenido: {e}")
                        st.info("Nota: Si el error persiste, revisa que tu API Key sea válida y tenga cuota disponible.")
        else:
            st.info("Ingresa los datos a la izquierda y presiona el botón para generar el borrador.")

    st.markdown("---")
    st.caption("© 2026 Centro Psicopedagógico - Sistema Pro v1.0")
st.caption("© 2026 Sistema de Apoyo Psicopedagógico")
