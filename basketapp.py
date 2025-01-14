import streamlit as st
from stats_functions import *
from mplbasketball import Court
from stats_partita import display_stats_partita
from stats_giocatori import display_stats_giocatori 

# Percorso della cartella delle partite
json_folder = 'season_stats/match_stats'

# Carica i dati delle partite
matches = load_json_files(json_folder)

# Pagine disponibili
st.sidebar.title("Menù")
page = st.sidebar.selectbox("Seleziona una pagina", ["Stats Partita", "Stats Giocatore"])

# Pagina: Stats Partita
if page == "Stats Partita":
    display_stats_partita(json_folder, matches)

# Pagina: Stats Giocatore
elif page == "Stats Giocatore":
    display_stats_giocatori(json_folder, matches)