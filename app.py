import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Sistema Psico-IA", page_icon="🧠", layout="wide")

# --- 2. CONFIGURACIÓN DE LA IA ---
# Usamos el nombre exacto que apareció en tu lista
if "GEMINI_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # Aquí pusimos el nombre exacto de tu lista de 2026
        model = genai.GenerativeModel('gemini-3-flash-preview')
    except Exception as e:
        st.error(f"Error al configurar la IA: {e}")
else:
    st.error("❌ Falta GEMINI_API_KEY en los Secrets.")

# --- 3. LOGIN ---
if "autenticado" not in st.session_state:
    st.title("🔐 Acceso al Sistema")
    with st.form("login"):
        u = st.text_input("Usuario")
        p = st.text_input("Contraseña", type="password")
        if st.form_submit_button("Entrar"):
            if u == "admin" and p == "centro2026":
                st.session_state["autenticado"] = True
                st.rerun()
            else:
                st.error("❌ Credenciales incorrectas")
    st.stop()

# --- 4. INTERFAZ ---
st.sidebar.title("Menú")
if st.sidebar.button("Cerrar Sesión"):
    del st.session_state["autenticado"]
    st.rerun()

st.title("🧠 Generador Inteligente de Informes")
st.write("Potenciado por Gemini 3 Flash Preview")
st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.header("📥 Datos del Alumno")
    nombre = st.text_input("Nombre completo")
    curso = st.text_input("Curso")
    obs = st.text_area("Notas de la sesión", height=300, placeholder="Escribe tus notas aquí...")
    
    boton_generar = st.button("✨ Generar Informe")

with col2:
    st.header("📄 Informe Sugerido")
    if boton_generar:
        if nombre and obs:
            with st.spinner("Redactando informe..."):
                try:
                    # Prompt optimizado
                    prompt = f"Actúa como psicopedagogo clínico. Redacta un informe para {nombre} del curso {curso}. Notas: {obs}. Estructura con Identificación, Análisis y Recomendaciones."
                    
                    response = model.generate_content(prompt)
                    
                    if response.text:
                        st.success("¡Informe generado con éxito!")
                        st.markdown(response.text)
                        
                        st.download_button(
                            label="📥 Descargar TXT",
                            data=response.text,
                            file_name=f"Informe_{nombre}.txt",
                            mime="text/plain"
                        )
                except Exception as e:
                    st.error(f"Error técnico: {e}")
        else:
            st.warning("⚠️ Rellena el nombre y las notas.")

st.markdown("---")
st.caption("© 2026 Centro Psicopedagógico")
