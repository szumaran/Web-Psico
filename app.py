import streamlit as st
import time

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Sistema Psico-IA", page_icon="🧠", layout="wide")

# --- 2. FUNCIÓN DE CONTROL DE ACCESO (LOGIN) ---
def check_password():
    """Retorna True si el usuario ingresó las credenciales correctas."""
    
    def password_entered():
        # AQUÍ defines el usuario y la clave
        if st.session_state["username"] == "admin" and st.session_state["password"] == "centro2026":
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Seguridad: borrar clave de memoria
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # Pantalla inicial de Login
        st.title("🔐 Acceso al Sistema Psico-IA")
        st.subheader("Por favor, identifícate para continuar")
        st.text_input("Usuario", key="username")
        st.text_input("Contraseña", type="password", key="password")
        st.button("Entrar", on_click=password_entered)
        return False
    
    elif not st.session_state["password_correct"]:
        # Mensaje si fallan los datos
        st.title("🔐 Acceso al Sistema Psico-IA")
        st.text_input("Usuario", key="username")
        st.text_input("Contraseña", type="password", key="password")
        st.button("Entrar", on_click=password_entered)
        st.error("❌ Usuario o contraseña incorrectos")
        return False
    
    else:
        return True

# --- 3. CONTENIDO DE LA PÁGINA (Solo si el login es exitoso) ---
if check_password():
    # Barra lateral
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/1995/1995574.png", width=80)
    st.sidebar.title("Menú Principal")
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state["password_correct"] = False
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
        curso = st.selectbox("Curso", ["Kinder", "1° Básico", "2° Básico", "3° Básico", "4° Básico", "5° Básico", "6° Básico"])
        
        st.subheader("Observaciones")
        obs = st.text_area("Notas de la sesión", height=200, 
                          placeholder="Escribe aquí tus observaciones clínicas...")
        
        boton_generar = st.button("✨ Generar Informe Profesional")

    with col2:
        st.header("📄 Informe Sugerido")
        if boton_generar:
            if nombre and obs:
                with st.spinner("La IA está redactando el informe..."):
                    time.sleep(2)  # Simulación de proceso
                    st.success("¡Informe generado con éxito!")
                    
                    # Estructura del informe que verá tu hermano
                    informe_final = f"""
### INFORME PSICOPEDAGÓGICO
---
**DATOS DE IDENTIFICACIÓN**
* **Nombre:** {nombre}
* **Edad:** {edad} años
* **Curso:** {curso}

**OBSERVACIONES CLÍNICAS**
{obs}

**RECOMENDACIONES PRELIMINARES**
1. Realizar adecuaciones curriculares de acceso.
2. Reforzar el área socio-afectiva en el hogar.
3. Se sugiere nueva evaluación en 6 meses.
                    """
                    st.markdown(informe_final)
                    
                    # Botón para descargar el resultado
                    st.download_button(
                        label="📥 Descargar Informe (TXT)",
                        data=informe_final,
                        file_name=f"Informe_{nombre}.txt",
                        mime="text/plain"
                    )
            else:
                st.warning("⚠️ Por favor, ingresa el nombre y las observaciones.")
        else:
            st.info("Ingresa los datos a la izquierda y presiona el botón para ver el borrador aquí.")

    st.markdown("---")
    st.caption("© 2026 Centro Psicopedagógico - Sistema de Gestión de Informes")
