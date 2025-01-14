import streamlit as st
import pandas as pd
from mplbasketball import Court
from stats_functions import *

def display_stats_partita(json_folder, matches):
    match_dict = {
        f"{match['info_partita']['home']} vs {match['info_partita']['away']} ({match['info_partita']['data']})": match
        for match in matches
    }

    # Creazione della lista ordinata di opzioni
    match_options = sorted(match_dict.keys(), key=lambda x: x.split("(")[-1])

    # Selezione della partita
    selected_match_name = st.selectbox("Seleziona una partita", match_options)

    # Accesso alla partita selezionata
    selected_match = match_dict[selected_match_name]

    # Debugging: stampa dei valori
    # st.write(selected_match)
    # st.write(selected_match_name)
    # Info partita
    data_partita = selected_match['info_partita']['data']
    home_team = selected_match['info_partita']['home']
    away_team = selected_match['info_partita']['away']
    punti_home = selected_match['stats_partita']['Punti_per_partita'][home_team]['TOT']
    punti_away = selected_match['stats_partita']['Punti_per_partita'][away_team]['TOT']
    st.title(f"{home_team} vs {away_team}")
    st.subheader(f"{punti_home} - {punti_away}")

    # Punti per partita
    punti_per_partita = selected_match['stats_partita']['Punti_per_partita']
    punti_df = pd.DataFrame(punti_per_partita).astype(int)
    st.subheader("Punti per Partita")
    st.table(punti_df)

    # Statistiche giocatori
    stats_giocatori = selected_match['stats_giocatore']
    players_df = pd.DataFrame(stats_giocatori).drop(columns=['shots'], errors='ignore')

    players_df['ft_%'] = players_df['ft_%'].apply(lambda x: convert_percentage_to_string(x, selected_match))
    players_df['2p_%'] = players_df['2p_%'].apply(lambda x: convert_percentage_to_string(x, selected_match))
    players_df['3p_%'] = players_df['3p_%'].apply(lambda x: convert_percentage_to_string(x, selected_match))

    st.subheader("Statistiche Giocatori")
    st.table(players_df)

    # Statistiche squadra
    statistiche_squadra = selected_match['stats_partita']['Statistiche_squadra']
    stats_df = pd.DataFrame({
        'Tipo': ['Free Throws', '2-Point Field Goals', '3-Point Field Goals'],
        'Made': [statistiche_squadra['ft']['made'], statistiche_squadra['2pt']['made'], statistiche_squadra['3pt']['made']],
        'Attempted': [statistiche_squadra['ft']['attempted'], statistiche_squadra['2pt']['attempted'], statistiche_squadra['3pt']['attempted']],
        'Percentage': [statistiche_squadra['ft']['percentage'], statistiche_squadra['2pt']['percentage'], statistiche_squadra['3pt']['percentage']]
    })
    st.subheader("Statistiche della Squadra")
    st.table(stats_df)

    # Mappa tiri
    court = Court(court_type="nba", origin="center", units="m")
    fig, ax = court.draw(showaxis=True, orientation="vu", court_color='white', paint_color='white', line_color='black')

    shots_data = get_shots_for_players(matches, selected_match)
    for x, y, shot_result in shots_data:
        color = 'g' if shot_result else 'r'
        ax.plot(x, y, 'o', color=color, alpha=0.9, markersize=7)

    st.subheader("Mappa dei Tiri")
    st.pyplot(fig)

