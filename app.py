import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Sistema Psico-IA", page_icon="🧠", layout="wide")

# --- 2. CONFIGURACIÓN DE GEMINI (SEGURA) ---
# Se usa st.secrets para que GitHub no bloquee la clave
try:
    if "GEMINI_API_KEY" in st.secrets:
        api_key_gemini = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key_gemini)
        model = genai.GenerativeModel('gemini-1.5-flash')
    else:
        st.warning("⚠️ Configura GEMINI_API_KEY en los Secrets de Streamlit.")
except Exception as e:
    st.error(f"Error de configuración: {e}")

# --- 3. FUNCIÓN DE CONTROL DE ACCESO (LOGIN) ---
def check_password():
    """Retorna True si el usuario ingresó las credenciales correctas."""
    if "password_correct" not in st.session_state:
        st.title("🔐 Acceso al Sistema Psico-IA")
        st.subheader("Por favor, identifícate para continuar")
        
        # Formulario de login
        with st.form("login_form"):
            username = st.text_input("Usuario")
            password = st.text_input("Contraseña", type="password")
            submit_button = st.form_submit_button("Entrar")
            
            if submit_button:
                if username == "admin" and password == "centro2026":
                    st.session_state["password_correct"] = True
                    st.rerun()
                else:
                    st.error("❌ Usuario o contraseña incorrectos")
        return False
    return True

# --- 4. CONTENIDO DE LA PÁGINA (Solo si el login es exitoso) ---
if check_password():
    # Barra lateral
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/1995/1995574.png", width=80)
    st.sidebar.title("Menú Principal")
    
    if st.sidebar.button("Cerrar Sesión"):
        del st.session_state["password_correct"]
        st.rerun()

    # Título principal de la web
    st.title("🧠 Generador Inteligente de Informes")
    st.write("Bienvenido al portal de redacción automatizada para el centro.")
    st.markdown("---")

    # Columnas para organizar el diseño
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
        obs = st.text_area("Notas de la sesión", height=300, 
                          placeholder="Escribe aquí tus observaciones clínicas, resultados de tests o comportamiento...")
        
        boton_generar = st.button("✨ Generar Informe Profesional")

    with col2:
        st.header("📄 Informe Sugerido")
        if boton_generar:
            if nombre and obs:
                with st.spinner("La IA de Gemini está redactando el informe..."):
                    try:
                        # PROMPT TÉCNICO PARA EL PROFESIONAL
                        prompt_sistema = f"""
                        Actúa como un Psicopedagogo clínico experto. 
                        Tu tarea es redactar un informe profesional para el alumno {nombre}, de {edad} años, que cursa {curso}.
                        
                        Basándote en estas notas de observación: "{obs}", genera un informe con este formato:
                        
                        1. IDENTIFICACIÓN: Resumen de los datos.
                        2. ANÁLISIS DE LA CONDUCTA: Desempeño durante la evaluación.
                        3. SÍNTESIS PSICOPEDAGÓGICA: Interpretación técnica de los hallazgos.
                        4. RECOMENDACIONES: 3 sugerencias para el colegio y 2 para el hogar.
                        
                        Usa un tono formal, clínico y preciso.
                        """
                        
                        # Llamada a Gemini
                        response = model.generate_content(prompt_sistema)
                        informe_final = response.text
                        
                        st.success("¡Informe generado con éxito!")
                        st.markdown(informe_final)
                        
                        # Botón para descargar el resultado
                        st.download_button(
                            label="📥 Descargar Informe (TXT)",
                            data=informe_final,
                            file_name=f"Informe_{nombre}.txt",
                            mime="text/plain"
                        )
                    except Exception as e:
                        st.error(f"Ocurrió un error al conectar con la IA: {e}")
            else:
                st.warning("⚠️ Por favor, ingresa el nombre y las observaciones para poder trabajar.")
        else:
            st.info("Ingresa los datos a la izquierda y presiona el botón para ver el borrador generado por IA.")

    st.markdown("---")
    st.caption("© 2026 Centro Psicopedagógico - Sistema de Gestión de Informes con IA")
