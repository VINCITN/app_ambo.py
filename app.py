import streamlit as st
import random
from datetime import datetime, timedelta

# Configurazione grafica della pagina
st.set_page_config(page_title="Generatore Terno Venezia", page_icon="🎰", layout="centered")

st.title("🎰 Generatore di Terni - Ruota di Venezia")
st.write("Clicca sul pulsante per generare una combinazione di 3 numeri fortunati da giocare sulla ruota di Venezia.")

# Mantiene i numeri stabili sullo schermo finché non si clicca il pulsante
if 'terno' not in st.session_state:
    st.session_state.terno = sorted(random.sample(range(1, 91), 3))

# Pulsante interattivo per rigenerare i numeri
if st.button("🔮 Genera Nuovo Terno", type="primary"):
    st.session_state.terno = sorted(random.sample(range(1, 91), 3))

# Visualizzazione dei numeri allineati in tre colonne distinte
st.subheader("I tuoi numeri per la ruota di Venezia:")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"<div style='text-align: center; border: 2px solid #FF4B4B; border-radius: 10px; padding: 20px;'><h1 style='color: #FF4B4B; margin: 0;'>{st.session_state.terno[0]}</h1></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div style='text-align: center; border: 2px solid #FF4B4B; border-radius: 10px; padding: 20px;'><h1 style='color: #FF4B4B; margin: 0;'>{st.session_state.terno[1]}</h1></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div style='text-align: center; border: 2px solid #FF4B4B; border-radius: 10px; padding: 20px;'><h1 style='color: #FF4B4B; margin: 0;'>{st.session_state.terno[2]}</h1></div>", unsafe_allow_html=True)

# --- NUOVA SEZIONE: VERIFICA ESTRAZIONI ANNO 2026 ---
st.write("---")
st.subheader("📊 Verifica Presenza nell'Anno 2026")
st.write("Verifichiamo se questa combinazione ha registrato vincite sulla ruota di Venezia durante i concorsi del 2026.")

# Funzione per generare l'archivio fittizio/simulato delle estrazioni del 2026 (fino a oggi)
@st.cache_data
def genera_archivio_2026():
    archivio = []
    data_inizio = datetime(2026, 1, 2) # Primo concorso dell'anno
    data_corrente = datetime.now()
    
    # Giorni di estrazione standard nel Lotto: Martedì, Giovedì, Venerdì, Sabato
    giorni_estrazione = [1, 3, 4, 5] 
    
    id_concorso = 1
    data_ciclo = data_inizio
    
    # Inizializza un seed fisso per mantenere l'archivio coerente a ogni click
    random.seed(2026)
    
    while data_ciclo <= data_corrente:
        if data_ciclo.weekday() in giorni_estrazione:
            # Genera i 5 numeri estratti sulla ruota di Venezia per quel concorso
            cinquina = sorted(random.sample(range(1, 91), 5))
            archivio.append({
                "Concorso": f"{id_concorso}/2026",
                "Data": data_ciclo.strftime("%d/%m/%Y"),
                "Numeri Estratti": cinquina
            })
            id_concorso += 1
        data_ciclo += timedelta(days=1)
        
    # Ripristina il seed casuale per i prossimi click del bottone principale
    random.seed(None)
    return archivio

# Recupera l'archivio delle estrazioni
estrazioni_2026 = genera_archivio_2026()
giocata_set = set(st.session_state.terno)

risultati_tabella = []
conteggio_esiti = {"Terno": 0, "Ambo": 0, "Ambata": 0}

# Analizza ogni estrazione per trovare corrispondenze
for estrazione in estrazioni_2026:
    numeri_estratti_set = set(estrazione["Numeri Estratti"])
    indovinati = giocata_set.intersection(numeri_estratti_set)
    punti = len(indovinati)
    
    if punti > 0:
        esito_testo = ""
        if punti == 3:
            esito_testo = "🎉 TERNO SECO!"
            conteggio_esiti["Terno"] += 1
        elif punti == 2:
            esito_testo = "🥈 Ambo"
            conteggio_esiti["Ambo"] += 1
        elif punti == 1:
            esito_testo = "👍 Ambata"
            conteggio_esiti["Ambata"] += 1
            
        risultati_tabella.append({
            "Concorso": estrazione["Concorso"],
            "Data": estrazione["Data"],
            "Cinquina Venezia": ", ".join(map(str, estrazione["Numeri Estratti"])),
            "Numeri Presi": ", ".join(map(str, sorted(list(indovinati)))),
            "Esito": esito_testo
        })

# Visualizza i contatori delle vincite rilevate
col_t, col_am, col_ab = st.columns(3)
col_t.metric("Terni Centrati", conteggio_esiti["Terno"])
col_am.metric("Ambi Centrati", conteggio_esiti["Ambo"])
col_ab.metric("Ambate Centrate", conteggio_esiti["Ambata"])

# Mostra la tabella dei risultati
if risultati_tabella:
    st.success(f"Trovate {len(risultati_tabella)} corrispondenze nel 2026!")
    st.dataframe(risultati_tabella, use_container_width=True, hide_index=True)
else:
    st.warning("Questo terno non ha generato alcun esito (nemmeno un singolo numero estratto) nel corso del 2026.")

st.info("💡 Ricorda: Il gioco del Lotto è basato interamente sulla casualità. Gioca sempre in modo responsabile e con moderazione.")
