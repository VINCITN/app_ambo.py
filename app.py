import streamlit as st
import random
from datetime import datetime, timedelta

# Configurazione grafica della pagina
st.set_page_config(page_title="Verifica Terno Ago-Set", page_icon="🎰", layout="centered")

st.title("🎰 Verifica Ambi e Terni (Agosto - Settembre 2026)")
st.write("Verifica le vincite sulle ruote di Venezia, Torino, Milano e Genova limitatamente ad Agosto e Settembre.")

# Mantiene i numeri stabili sullo schermo
if 'terno' not in st.session_state:
    st.session_state.terno = sorted(random.sample(range(1, 91), 3))

# Pulsante per rigenerare i numeri
if st.button("🔮 Genera Nuovo Terno", type="primary"):
    st.session_state.terno = sorted(random.sample(range(1, 91), 3))

# Visualizzazione dei numeri nelle colonne
st.subheader("I tuoi numeri fortunati:")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"<div style='text-align: center; border: 2px solid #FF4B4B; border-radius: 10px; padding: 20px;'><h1 style='color: #FF4B4B; margin: 0;'>{st.session_state.terno[0]}</h1></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div style='text-align: center; border: 2px solid #FF4B4B; border-radius: 10px; padding: 20px;'><h1 style='color: #FF4B4B; margin: 0;'>{st.session_state.terno[1]}</h1></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div style='text-align: center; border: 2px solid #FF4B4B; border-radius: 10px; padding: 20px;'><h1 style='color: #FF4B4B; margin: 0;'>{st.session_state.terno[2]}</h1></div>", unsafe_allow_html=True)

# --- SEZIONE VERIFICA FILTRATA (AGOSTO E SETTEMBRE) ---
st.write("---")
st.subheader("📊 Esiti Rilevati: Agosto e Settembre 2026")

@st.cache_data
def genera_archivio_filtrato_2026():
    archivio = []
    data_inizio = datetime(2026, 1, 2)
    data_corrente = datetime.now()
    
    # Giorni di estrazione standard: 1=Martedì, 3=Giovedì, 4=Venerdì, 5=Sabato
    giorni_estrazione = [1, 3, 4, 5]
    
    id_concorso = 1
    data_ciclo = data_inizio
    
    random.seed(2026) # Mantiene i dati coerenti a ogni avvio
    ruote = ["Venezia", "Torino", "Milano", "Genova"]
    
    while data_ciclo <= data_corrente:
        if data_ciclo.weekday() in giorni_estrazione:
            # Estrae i dati per tutte le ruote
            estrazione_concorso = {
                "Concorso": f"{id_concorso}/2026",
                "Data": data_ciclo.strftime("%d/%m/%Y"),
                "Mese": data_ciclo.month,
                "Ruote": {ruota: sorted(random.sample(range(1, 91), 5)) for ruota in ruote}
            }
            archivio.append(estrazione_concorso)
            id_concorso += 1
        data_ciclo += timedelta(days=1)
        
    random.seed(None)
    return archivio

# Analisi dei risultati
archivio_completo = genera_archivio_filtrato_2026()
giocata_set = set(st.session_state.terno)

risultati_tabella = []
conteggio_esiti = {"Terno": 0, "Ambo": 0}

for concorso in archivio_completo:
    # FILTRO: Considera solo Agosto (8) e Settembre (9)
    if concorso["Mese"] not in:
        continue
        
    for ruota, cinquina in concorso["Ruote"].items():
        cinquina_set = set(cinquina)
        indovinati = giocata_set.intersection(cinquina_set)
        punti = len(indovinati)
        
        # FILTRO: Solo Ambo (2) e Terno (3) - Esclude le Ambate (1)
        if punti >= 2:
            if punti == 3:
                esito_testo = "🎉 TERNO SECO!"
                conteggio_esiti["Terno"] += 1
            elif punti == 2:
                esito_testo = "🥈 Ambo"
                conteggio_esiti["Ambo"] += 1
                
            risultati_tabella.append({
                "Concorso": concorso["Concorso"],
                "Data": concorso["Data"],
                "Ruota": ruota,
                "Cinquina Estratta": ", ".join(map(str, cinquina)),
                "Numeri Presi": ", ".join(map(str, sorted(list(indovinati)))),
                "Esito": esito_testo
            })

# Visualizzazione metriche (senza la colonna Ambata)
col_t, col_am = st.columns(2)
col_t.metric("Terni Totali (Ago-Set)", conteggio_esiti["Terno"])
col_am.metric("Ambi Totali (Ago-Set)", conteggio_esiti["Ambo"])

# Mostra la tabella
if risultati_tabella:
    st.success(f"Trovati {len(risultati_tabella)} esiti utili tra Agosto e Settembre!")
    risultati_tabella.reverse() # Mostra i più recenti in alto
    st.dataframe(risultati_tabella, use_container_width=True, hide_index=True)
else:
    st.warning("Nessun ambo o terno registrato in questi due mesi su Venezia, Torino, Milano e Genova.")

st.info("💡 Ricorda: Il gioco del Lotto è basato interamente sulla casualità. Gioca sempre in modo responsabile.")
