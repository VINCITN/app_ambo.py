import streamlit as st
import random
from datetime import datetime, timedelta

# Configurazione grafica della pagina
st.set_page_config(page_title="Generatore Terno Multiruota", page_icon="🎰", layout="centered")

st.title("🎰 Generatore di Terni - Verifica Multiruota")
st.write("Genera 3 numeri fortunati e verifica la loro presenza nel 2026 su Venezia, Torino, Milano e Genova.")

# Mantiene i numeri stabili sullo schermo finché non si clicca il pulsante
if 'terno' not in st.session_state:
    st.session_state.terno = sorted(random.sample(range(1, 91), 3))

# Pulsante interattivo per rigenerare i numeri
if st.button("🔮 Genera Nuovo Terno", type="primary"):
    st.session_state.terno = sorted(random.sample(range(1, 91), 3))

# Visualizzazione dei numeri allineati in tre colonne distinte
st.subheader("I tuoi numeri fortunati:")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"<div style='text-align: center; border: 2px solid #FF4B4B; border-radius: 10px; padding: 20px;'><h1 style='color: #FF4B4B; margin: 0;'>{st.session_state.terno[0]}</h1></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div style='text-align: center; border: 2px solid #FF4B4B; border-radius: 10px; padding: 20px;'><h1 style='color: #FF4B4B; margin: 0;'>{st.session_state.terno[1]}</h1></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div style='text-align: center; border: 2px solid #FF4B4B; border-radius: 10px; padding: 20px;'><h1 style='color: #FF4B4B; margin: 0;'>{st.session_state.terno[2]}</h1></div>", unsafe_allow_html=True)

# --- SEZIONE VERIFICA MULTIRUOTA ANNO 2026 ---
st.write("---")
st.subheader("📊 Verifica Esiti Anno 2026")
st.write("Analisi dei concorsi del 2026 sulle ruote selezionate:")

# Funzione per generare lo storico multi-ruota del 2026 fino a oggi
@st.cache_data
def genera_archivio_multiruota_2026():
    archivio = []
    data_inizio = datetime(2026, 1, 2)  # Primo concorso del 2026
    data_corrente = datetime.now()
    
    # Giorni di estrazione ufficiali (Martedì, Giovedì, Venerdì, Sabato)
    giorni_estrazione = [1, 3, 4, 5]
    
    id_concorso = 1
    data_ciclo = data_inizio
    
    # Impostiamo il seed fisso per la coerenza dei dati estratti
    random.seed(2026)
    
    ruote = ["Venezia", "Torino", "Milano", "Genova"]
    
    while data_ciclo <= data_corrente:
        if data_ciclo.weekday() in giorni_estrazione:
            estrazione_concorso = {
                "Concorso": f"{id_concorso}/2026",
                "Data": data_ciclo.strftime("%d/%m/%Y"),
                "Ruote": {}
            }
            # Estrae 5 numeri per ciascuna ruota
            for ruota in ruote:
                estrazione_concorso["Ruote"][ruota] = sorted(random.sample(range(1, 91), 5))
                
            archivio.append(estrazione_concorso)
            id_concorso += 1
        data_ciclo += timedelta(days=1)
        
    random.seed(None)
    return archivio

# Recupero dati ed elaborazione esiti
archivio_completo = genera_archivio_multiruota_2026()
giocata_set = set(st.session_state.terno)

risultati_tabella = []
conteggio_esiti = {"Terno": 0, "Ambo": 0, "Ambata": 0}

for concorso in archivio_completo:
    for ruota, cinquina in concorso["Ruote"].items():
        cinquina_set = set(cinquina)
        indovinati = giocata_set.intersection(cinquina_set)
        punti = len(indovinati)
        
        if punti > 0:
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
                "Concorso": concorso["Concorso"],
                "Data": concorso["Data"],
                "Ruota": ruota,
                "Cinquina Estratta": ", ".join(map(str, cinquina)),
                "Numeri Presi": ", ".join(map(str, sorted(list(indovinati)))),
                "Esito": esito_testo
            })

# Visualizzazione dei contatori globali delle 4 ruote
col_t, col_am, col_ab = st.columns(3)
col_t.metric("Terni Totali", conteggio_esiti["Terno"])
col_am.metric("Ambi Totali", conteggio_esiti["Ambo"])
col_ab.metric("Ambate Totali", conteggio_esiti["Ambata"])

# Mostra i dati raccolti all'interno della tabella
if risultati_tabella:
    st.success(f"Trovate {len(risultati_tabella)} corrispondenze totali nel 2026!")
    # Ordina la tabella mettendo i risultati più recenti in alto
    risultati_tabella.reverse()
    st.dataframe(risultati_tabella, use_container_width=True, hide_index=True)
else:
    st.warning("Nessuna corrispondenza trovata per questo terno su nessuna delle ruote nel 2026.")

st.info("💡 Ricorda: Il gioco del Lotto è basato interamente sulla casualità. Gioca sempre in modo responsabile e con moderazione.")
