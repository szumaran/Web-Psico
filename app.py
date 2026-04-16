import streamlit as st
import time

# --- 1. CONFIGURACIÓ DE LA PÀGINA ---
st.set_page_config(page_title="Sistema Psico-IA", page_icon="🧠", layout="wide")

# --- 2. FUNCIÓ DE CONTROL D'ACCÉS (LOGIN) ---
def check_password():
    """Retorna True si l'usuari ha introduït les credencials correctes."""
    
    def password_entered():
        # AQUÍ dónes l'usuari i la clau que vulguis (pots canviar-les)
        if st.session_state["username"] == "admin" and st.session_state["password"] == "centro2026":
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Esborra la contrasenya de la memòria per seguretat
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # Pantalla inicial de Login
        st.title("🔐 Accés al Sistema Psico-IA")
        st.subheader("Si us plau, identifica't per continuar")
        st.text_input("Usuari", key="username")
        st.text_input("Contrasenya", type="password", key="password")
        st.button("Entrar", on_click=password_entered)
        return False
    
    elif not st.session_state["password_correct"]:
        # Si s'equivoca de contrasenya
        st.title("🔐 Accés al Sistema Psico-IA")
        st.text_input("Usuari", key="username")
        st.text_input("Contrasenya", type="password", key="password")
        st.button("Entrar", on_click=password_entered)
        st.error("❌ Usuari o contrasenya incorrectes")
        return False
    
    else:
        return True

# --- 3. CONTINGUT DE LA PÀGINA WEB (Només es veu si el login és correcte) ---
if check_password():
    # Barra lateral
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/1995/1995574.png", width=80)
    st.sidebar.title("Menú Principal")
    if st.sidebar.button("Tancar Sessió"):
        st.session_state["password_correct"] = False
        st.rerun()

    # Títol de la web
    st.title("🧠 Generador Intel·ligent d'Informes Psicopedagògics")
    st.write("Benvingut al portal de redacció automatitzada.")
    st.markdown("---")

    # Columnes per al formulari
    col1, col2 = st.columns([1, 1])

    with col1:
        st.header("📥 Dades de l'alumne")
        nom = st.text_input("Nom complet de l'alumne")
        edat = st.number_input("Edat", min_value=0, max_value=18, value=8)
        observacions = st.text_area("Observacions i notes de l'avaluació", height=200, 
                                   placeholder="Escriu aquí el que has observat durant la sessió...")
        
        boto_generar = st.button("✨ Generar Informe")

    with col2:
        st.header("📄 Informe Resultant")
        if boto_generar:
            if nom and observacions:
                with st.spinner('L'IA està redactant l'informe...'):
                    time.sleep(2) # Simulació de processament
                    st.success("Informe generat amb èxit!")
                    
                    text_final = f"""
                    ### INFORME PSICOPEDAGÒGIC
                    **Nom:** {nom}
                    **Edat:** {edat} anys
                    
                    **ANÀLISI:**
                    {observacions}
                    
                    **RECOMANACIONS:**
                    1. Seguiment a l'escola.
                    2. Reforç en les àrees identificades.
                    """
                    st.markdown(text_final)
                    
                    st.download_button(label="📥 Descarregar Informe", 
                                       data=text_final, 
                                       file_name=f"Informe_{nom}.txt")
            else:
                st.warning("Si us plau, omple el nom i les observacions.")
        else:
            st.info("Omple les dades de l'esquerra per veure l'esborrany de l'informe aquí.")

    st.markdown("---")
    st.caption("© 2026 Centro Psicopedagógico - Prototip de Prova")
