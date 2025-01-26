import streamlit as st
from stats_functions import *
from mplbasketball import Court
from stats_partita import display_stats_partita
from stats_giocatori import display_stats_giocatori
import random
import time
st.set_page_config(layout= "wide")

st.sidebar.image('zanica-badgers Logo.webp', use_column_width=True)

progress_texts = [
    "Panda sta scrivendo su whatsapp...",
    "Teo sta preparando le pagelle...",
    "Claud sta chiamando 1...",
    "Iachi sta aspettando il cambio...",
    "Il Rails sta preparando la kingscross...",
    "Gli avversari si stanno mettendo a zona...",
    "la squadra sta rispondendo ai sondaggi..."
    ]

my_bar = st.progress(0)
progress_text = random.choice(progress_texts)
for percent_complete in range(100):
    my_bar.progress(percent_complete + 1, text=progress_text)
    time.sleep(0.01)

time.sleep(1)
my_bar.empty()

# Percorso della cartella delle partite
json_folder = 'season_stats/match_stats'

# Carica i dati delle partite
matches = load_json_files(json_folder)

# Pagine disponibili
st.sidebar.title("Menù")
page = st.sidebar.selectbox("cosa vuoi analizzare?", ["Stats Partita", "Stats Giocatore"])

# Pagina: Stats Partita
if page == "Stats Partita":
    display_stats_partita(json_folder, matches)

# Pagina: Stats Giocatore
elif page == "Stats Giocatore":
    display_stats_giocatori(json_folder, matches)