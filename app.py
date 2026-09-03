import streamlit as st
import random

# Configurazione grafica della pagina
st.set_page_config(page_title="Generatore Ambo Venezia", page_icon="🎰", layout="centered")

st.title("🎰 Generatore di Ambi - Ruota di Venezia")
st.write("Clicca sul pulsante per generare una combinazione di 2 numeri fortunati da giocare sulla ruota di Venezia.")

# Mantiene i numeri stabili sullo schermo finché non si clicca il pulsante
if 'ambo' not in st.session_state:
    st.session_state.ambo = sorted(random.sample(range(1, 91), 2))

# Pulsante interattivo per rigenerare i numeri
if st.button("🔮 Genera Nuovo Ambo", type="primary"):
    # Estrae 2 numeri casuali unici tra 1 e 90 e li ordina
    st.session_state.ambo = sorted(random.sample(range(1, 91), 2))

# Visualizzazione dei numeri allineati in due colonne distinte
st.subheader("I tuoi numeri per la ruota di Venezia:")

col1, col2 = st.columns(2)
with col1:
    st.markdown(f"<div style='text-align: center; border: 2px solid #FF4B4B; border-radius: 10px; padding: 20px;'><h1 style='color: #FF4B4B; margin: 0;'>{st.session_state.ambo[0]}</h1></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div style='text-align: center; border: 2px solid #FF4B4B; border-radius: 10px; padding: 20px;'><h1 style='color: #FF4B4B; margin: 0;'>{st.session_state.ambo[1]}</h1></div>", unsafe_allow_html=True)

st.info("💡 Ricorda: Il gioco del Lotto è basato interamente sulla casualità. Gioca sempre in modo responsabile e con modificazione.")

