import streamlit as st
import time

# Configuración de la pestaña
st.set_page_config(page_title="Copiloto Psicopedagógico IA", page_icon="🧠", layout="wide")

# Estilo personalizado con CSS simple
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; background-color: #4CAF50; color: white; }
    </style>
    """, unsafe_allow_html=True)

# Encabezado
st.title("🧠 Asistente de Informes Inteligente")
st.subheader("Centro Psicopedagógico")
st.markdown("---")

# Layout de dos columnas
col_input, col_output = st.columns([1, 1])

with col_input:
    st.header("📥 Entrada de Datos")
    
    with st.expander("1. Identificación del Niño", expanded=True):
        nombre = st.text_input("Nombre Completo")
        edad = st.number_input("Edad", min_value=0, max_value=18, value=8)
        escolaridad = st.selectbox("Curso", ["Pre-Kinder", "Kinder", "1° Básico", "2° Básico", "3° Básico", "4° Básico"])

    with st.expander("2. Observaciones de la Sesión", expanded=True):
        obs = st.text_area("Notas rápidas (Ej: se distrae fácil, buena memoria visual...)", height=150)

    with st.expander("3. Resultados de Tests"):
        c1, c2 = st.columns(2)
        wisc = c1.number_input("WISC-V (Puntaje Total)", 0, 160, 90)
        lectura = c2.selectbox("Nivel Lectura", ["Bajo", "Medio-Bajo", "Adecuado", "Superior"])

    # Botón de acción
    boton_ia = st.button("✨ GENERAR INFORME PROFESIONAL")

with col_output:
    st.header("📄 Borrador del Informe")
    
    if boton_ia:
        if not nombre or not obs:
            st.warning("Por favor, ingresa el nombre y las observaciones primero.")
        else:
            with st.spinner('La IA está redactando el informe siguiendo el formato del centro...'):
                time.sleep(3) # Simulamos el tiempo de procesamiento de la IA
                
                # Esto es lo que vería el profesional (Simulado por ahora)
                st.success("¡Informe generado!")
                informe_final = f"""
                **INFORME PSICOPEDAGÓGICO**
                
                **I. IDENTIFICACIÓN**
                - **Nombre:** {nombre}
                - **Edad:** {edad} años
                - **Curso:** {escolaridad}
                
                **II. CONDUCTA OBSERVADA**
                Durante la sesión, el evaluado presentó el siguiente perfil: {obs}.
                
                **III. ANÁLISIS DE RESULTADOS**
                En la evaluación psicométrica, se obtuvo un puntaje de {wisc} en el test WISC-V. 
                En cuanto a la lectoescritura, se sitúa en un nivel {lectura}.
                
                **IV. SUGERENCIAS**
                - Reforzar autonomía en tareas escolares.
                - Adecuaciones curriculares en el área de lenguaje.
                """
                st.markdown(informe_final)
                
                # Opciones de exportación
                st.download_button("📥 Descargar como PDF (Simulado)", "Contenido del informe", file_name=f"Informe_{nombre}.pdf")
    else:
        st.info("Ingresa los datos a la izquierda y presiona el botón para ver la magia.")

# Pie de página
st.markdown("---")
st.caption("Desarrollado para la optimización de procesos clínicos - 2026")