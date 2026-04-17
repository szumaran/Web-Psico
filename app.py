import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Sistema Psico-IA", page_icon="🧠", layout="wide")

# --- 2. CONFIGURACIÓN DE GEMINI ---
# Reemplaza 'TU_API_KEY_AQUI' con la clave de la imagen que me mostraste
genai.configure(api_key="TU_API_KEY_AQUI")
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 3. FUNCIÓN DE CONTROL DE ACCESO (LOGIN) ---
def check_password():
    """Retorna True si el usuario ingresó las credenciales correctas."""
    if "password_correct" not in st.session_state:
        st.title("🔐 Acceso al Sistema Psico-IA")
        st.subheader("Por favor, identifícate para continuar")
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        if st.button("Entrar"):
            if username == "admin" and password == "centro2026":
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("❌ Usuario o contraseña incorrectos")
        return False
    return True

# --- 4. CONTENIDO DE LA PÁGINA ---
if check_password():
    # Barra lateral
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/1995/1995574.png", width=80)
    st.sidebar.title("Menú Principal")
    if st.sidebar.button("Cerrar Sesión"):
        del st.session_state["password_correct"]
        st.rerun()

    st.title("🧠 Generador Inteligente de Informes")
    st.write("Bienvenido al portal de redacción automatizada para el centro.")
    st.markdown("---")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.header("📥 Datos del Alumno")
        nombre = st.text_input("Nombre completo del alumno", placeholder="Ej: Mateo Gómez")
        edad = st.number_input("Edad", min_value=0, max_value=18, value=8)
        curso = st.selectbox("Curso", ["Kinder", "1° Básico", "2° Básico", "3° Básico", "4° Básico", "5° Básico", "6° Básico", "7° Básico", "8° Básico", "I Medio"])
        
        st.subheader("Observaciones")
        obs = st.text_area("Notas de la sesión", height=250, 
                          placeholder="Ej: El alumno presenta dificultades en la lectura fluida, se distrae con facilidad pero responde bien al refuerzo positivo...")
        
        boton_generar = st.button("✨ Generar Informe con IA")

    with col2:
        st.header("📄 Informe Sugerido")
        if boton_generar:
            if nombre and obs:
                with st.spinner("Gemini está redactando el informe profesional..."):
                    try:
                        # PROMPT ESTRATÉGICO PARA EL CENTRO
                        prompt_sistema = f"""
                        Actúa como un Psicopedagogo experto con años de experiencia clínica.
                        Tu tarea es redactar un informe profesional para el alumno {nombre}, de {edad} años, que cursa {curso}.
                        
                        Basándote estrictamente en estas notas de observación: "{obs}", genera un informe con este formato:
                        
                        1. **IDENTIFICACIÓN**: Resumen de los datos del alumno.
                        2. **ANÁLISIS DE LA CONDUCTA**: Describe el comportamiento y desempeño según las notas.
                        3. **SÍNTESIS PSICOPEDAGÓGICA**: Interpretación técnica de las dificultades o fortalezas detectadas.
                        4. **SUGERENCIAS Y RECOMENDACIONES**: Entrega 3 a 5 recomendaciones concretas para el colegio y la familia.
                        
                        Usa un tono formal, técnico y empático.
                        """
                        
                        # Llamada real a la API de Gemini
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
                        st.error(f"Hubo un error con la IA: {e}")
            else:
                st.warning("⚠️ Por favor, ingresa el nombre y las observaciones para trabajar.")
        else:
            st.info("Ingresa los datos y presiona el botón. Gemini analizará tus notas y redactará el borrador.")

    st.markdown("---")
    st.caption("© 2026 Centro Psicopedagógico - Potenciado por Gemini 1.5 Flash")

    st.markdown("---")
    st.caption("© 2026 Centro Psicopedagógico - Sistema de Gestión de Informes")
