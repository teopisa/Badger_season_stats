import streamlit as st
import pandas as pd
import json
import os
import matplotlib.pyplot as plt
import mplbasketball as mpb
from mplbasketball import Court
import numpy as np
from drawshotarea import draw_shot_zones, transform_court_params
from mplbasketball import Court, utils
from mplbasketball.utils import transform



# Funzione per caricare i file JSON da una cartella
def load_json_files(folder):
    data = []
    for filename in os.listdir(folder):
        if filename.endswith('.json'):
            with open(os.path.join(folder, filename)) as f:
                match_data = json.load(f)
                data.append(match_data)
    return data

def get_shots_for_players(matches):
    shots_data = []
    for match in matches:
        stats_giocatori = match['stats_giocatore']
        for player in stats_giocatori:
            if 'shots' in player:  # Verifica se il giocatore ha dati sui tiri
                for shot in player['shots']:
                    x = shot.get('X', None)
                    y = shot.get('Y', None)
                    shot_result = shot.get('Made', None)
                    if x is not None and y is not None:
                        x = round(x, 2)
                        y = round(y, 2)
                        shot_result = shot_result
                        shots_data.append((x, y, shot_result))  # Aggiungi la coppia di coordinate
    return shots_data


# Percorso della cartella delle partite
json_folder = 'season_stats\match_stats'

# Carica i dati
matches = load_json_files(json_folder)

# Titolo della web app
st.title("Basketball Stats Web App")

# Se ci sono partite, visualizzale
if matches:
    st.write("Partite caricate:")
    for match in matches:
        # Estrai informazioni di base della partita
        data_partita = match['info_partita']['data']
        home_team = match['info_partita']['home']
        away_team = match['info_partita']['away']
        
        # Estrai le statistiche della partita
        progressione_partita = match['stats_partita']['Progressione_partita']
        punti_per_partita = match['stats_partita']['Punti_per_partita']
        statistiche_squadra = match['stats_partita']['Statistiche_squadra']

        # Mostra informazioni di base
        st.write(f"Data: {data_partita}, Home: {home_team}, Away: {away_team}")

        # Crea un DataFrame per la progressione della partita
        progressione_df = pd.DataFrame(progressione_partita)
        st.subheader("Progressione della Partita")
        st.table(progressione_df)

        # Rimuovi la chiave "OT" se esiste
        # punti_per_partita['Badgers'].pop('OT', None)  # Rimuovi OT per Badgers
        # punti_per_partita['PotascetBasket'].pop('OT', None)  # Rimuovi OT per PotascetBasket

        # Crea un DataFrame per i punti per partita
        punti_df = pd.DataFrame(punti_per_partita).astype(int)  # Arrotonda a interi
        st.subheader("Punti per Partita")
        st.table(punti_df)

        # Estrai statistiche della squadra
        stats_df = pd.DataFrame({
            'Tipo': ['Free Throws', '2-Point Field Goals', '3-Point Field Goals'],
            'Made': [statistiche_squadra['ft']['made'], statistiche_squadra['2pt']['made'], statistiche_squadra['3pt']['made']],
            'Attempted': [statistiche_squadra['ft']['attempted'], statistiche_squadra['2pt']['attempted'], statistiche_squadra['3pt']['attempted']],
            'Percentage': [statistiche_squadra['ft']['percentage'], statistiche_squadra['2pt']['percentage'], statistiche_squadra['3pt']['percentage']]
        })

        st.subheader("Statistiche della Squadra")
        st.table(stats_df)

        # Estrai e mostra le statistiche dei giocatori
        stats_giocatori = match['stats_giocatore']

        players_df = pd.DataFrame(stats_giocatori)
        # players_df = players_df.drop(columns=['shots'])


        # Modifica le statistiche per formattare le percentuali
        def convert_percentage_to_string(percentage):
            return f"{percentage * 100:.0f}%"  # Moltiplica per 100 e formatta senza decimali

        # Applica la funzione per formattare le percentuali
        players_df['ft_%'] = players_df['ft_%'].apply(convert_percentage_to_string)
        players_df['2p_%'] = players_df['2p_%'].apply(convert_percentage_to_string)
        players_df['3p_%'] = players_df['3p_%'].apply(convert_percentage_to_string)

        # Converti le altre colonne in interi, gestendo gli errori
        players_df = players_df.astype({'pts': int, 'reb': int, 'dreb': int, 'orib': int, 'ast': int, 'to': int, 'foul': int}, errors='ignore')  # Arrotonda a interi

        st.subheader("Statistiche Giocatori")
        st.table(players_df)

       

else:
    st.write("Nessuna partita trovata nella cartella.")


court = Court(court_type="nba", origin="center", units="m")
fig, ax = court.draw(showaxis=True, orientation="vu", court_color = 'white', paint_color = 'white', line_color = 'black', line_width = 0.2, pad = 1)

court_parameters = court.court_parameters
st.write(court_parameters)

court_params_transformed = transform_court_params(court_parameters, fr="h", to="vd", origin="center", court_dims=[28.651200000000003, 15.24])
st.write(court_params_transformed)



# Set the axis limits

shots_data = get_shots_for_players(matches)

# Estrai le coordinate x e y dei tiri e plottali come punti
for x, y, shot_result in shots_data:
    color = 'g' if shot_result else 'r'  # Verde se True (realizzato), Rosso se False (non realizzato)
    ax.plot(x, y, 'o', color=color, alpha=0.9, markersize=7)  # Alpha per trasparenza, markersize per dimensione del punto

# Mostra la visualizzazione
st.title("Heatmap dei Tiri")
draw_shot_zones(ax, court_params_transformed)
st.pyplot(fig)


