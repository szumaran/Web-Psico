import streamlit as st
import google.generativeai as genai

st.title("🔍 Detector de Modelos de tu cuenta")

if "GEMINI_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        
        # Esto le pregunta a Google: "¿Qué modelos me dejas usar con esta clave?"
        models = genai.list_models()
        
        st.write("### Copia el nombre exacto de esta lista:")
        
        for m in models:
            if 'generateContent' in m.supported_generation_methods:
                # Te mostrará una lista de nombres técnicos
                nombre_modelo = m.name.replace('models/', '')
                st.code(nombre_modelo)
                
    except Exception as e:
        st.error(f"Error al conectar con Google: {e}")
        st.info("Si sale error de autenticación, tu API Key está mala.")
else:
    st.error("No hay clave en Secrets. Ve a Settings > Secrets en Streamlit.")
