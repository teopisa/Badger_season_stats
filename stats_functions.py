import os
import json
import pandas as pd
import streamlit as st


def convert_percentage_to_string(percentage, match):
    """
    Convert percentage to string format with appropriate handling based on the match context.
    """
    # if isinstance(percentage, str) and '%' in percentage:
    #     # If the percentage is already a string (e.g., '38.89%'), strip the '%' and convert to float
    #     percentage = float(percentage.strip('%'))
    # elif isinstance(percentage, (int, float)):
    #     # Convert numeric values to percentage string format
    #     percentage = f"{percentage:.0f}%"
    
    if match == 'season_stats/match_stats/badgers_potascetbasket_20241007.json':
        return f"{percentage:.0f}%"
    else:
        return f"{percentage}%"

# Update the part where you apply this conversion in your players' stats
def display_match_info(match):
    st.subheader(f"Info Partita: {match['info_partita']['home']} vs {match['info_partita']['away']} - {match['info_partita']['data']}")
    
    # Progressione partita
    progressione_partita = match['stats_partita']['Progressione_partita']
    progressione_df = pd.DataFrame(progressione_partita)
    st.subheader("Progressione della Partita")
    st.table(progressione_df)

    # Punti per partita
    punti_per_partita = match['stats_partita']['Punti_per_partita']
    punti_df = pd.DataFrame(punti_per_partita).astype(int)
    st.subheader("Punti per Partita")
    st.table(punti_df)

    # Statistiche squadra
    statistiche_squadra = match['stats_partita']['Statistiche_squadra']
    stats_df = pd.DataFrame({
        'Tipo': ['Free Throws', '2-Point Field Goals', '3-Point Field Goals'],
        'Made': [statistiche_squadra['ft']['made'], statistiche_squadra['2pt']['made'], statistiche_squadra['3pt']['made']],
        'Attempted': [statistiche_squadra['ft']['attempted'], statistiche_squadra['2pt']['attempted'], statistiche_squadra['3pt']['attempted']],
        'Percentage': [statistiche_squadra['ft']['percentage'], statistiche_squadra['2pt']['percentage'], statistiche_squadra['3pt']['percentage']]
    })
    # Handle percentage conversion in the 'Percentage' column to ensure it is Arrow-compatible
    stats_df['Percentage'] = stats_df['Percentage'].apply(lambda x: convert_percentage_to_string(x, match))
    st.subheader("Statistiche della Squadra")
    st.table(stats_df)

    # Statistiche giocatori
    stats_giocatori = match['stats_giocatore']
    players_df = pd.DataFrame(stats_giocatori).drop(columns=['shots'], errors='ignore')

    players_df['ft_%'] = players_df['ft_%'].apply(lambda x: convert_percentage_to_string(x, match))
    players_df['2p_%'] = players_df['2p_%'].apply(lambda x: convert_percentage_to_string(x, match))
    players_df['3p_%'] = players_df['3p_%'].apply(lambda x: convert_percentage_to_string(x, match))

    st.subheader("Statistiche Giocatori")
    st.table(players_df)


# Carica i file JSON dalla cartella
def load_json_files(folder):
    data = []
    for filename in os.listdir(folder):
        if filename.endswith('.json'):
            with open(os.path.join(folder, filename)) as f:
                match_data = json.load(f)
                data.append(match_data)
    return data


# Estrai tiri per i giocatori
def get_shots_for_players(matches, selected_match):
    shots_data = []
    for player in selected_match['stats_giocatore']:
        if 'shots' in player:
            for shot in player['shots']:
                x = shot.get('X')
                y = shot.get('Y')
                shot_result = shot.get('Made')
                if x is not None and y is not None:
                    shots_data.append((x, y, shot_result))
    return shots_data

# Ottieni nomi unici dei giocatori
def get_unique_player_names(matches):
    player_names = set()
    for match in matches:
        for player in match['stats_giocatore']:
            player_names.add(player['name'])
    return sorted(player_names)

# Calcola le statistiche per un giocatore
def calculate_player_stats(matches, player_name):
    total_stats = {
        "Punti Totali": 0,
        "Tiri da 2 Realizzati": 0,
        "Tiri da 2 Tentati": 0,
        "Tiri da 3 Realizzati": 0,
        "Tiri da 3 Tentati": 0,
        "Tiri Liberi Realizzati": 0,
        "Tiri Liberi Tentati": 0,
    }

    for match in matches:
        for player in match['stats_giocatore']:
            if player['name'] == player_name:
                total_stats["Punti Totali"] += player['pts']
                total_stats["Tiri da 2 Realizzati"] += player['2p_made']
                total_stats["Tiri da 2 Tentati"] += player['2p_taken']
                total_stats["Tiri da 3 Realizzati"] += player['3p_made']
                total_stats["Tiri da 3 Tentati"] += player['3p_taken']
                total_stats["Tiri Liberi Realizzati"] += player['ft_made']
                total_stats["Tiri Liberi Tentati"] += player['ft_taken']

    # Calcola percentuali
    total_stats["% Tiri da 2"] = f"{(total_stats['Tiri da 2 Realizzati'] / total_stats['Tiri da 2 Tentati'] * 100):.2f}%" if total_stats['Tiri da 2 Tentati'] > 0 else "0%"
    total_stats["% Tiri da 3"] = f"{(total_stats['Tiri da 3 Realizzati'] / total_stats['Tiri da 3 Tentati'] * 100):.2f}%" if total_stats['Tiri da 3 Tentati'] > 0 else "0%"
    total_stats["% Tiri Liberi"] = f"{(total_stats['Tiri Liberi Realizzati'] / total_stats['Tiri Liberi Tentati'] * 100):.2f}%" if total_stats['Tiri Liberi Tentati'] > 0 else "0%"

    return total_stats

# Mostra statistiche del giocatore
def display_player_stats(player_name, stats):
    st.subheader(f"Statistiche di {player_name}")
    stats_df = pd.DataFrame({
        "Statistiche": list(stats.keys()),
        "Valore": list(stats.values())
    })
    st.table(stats_df)

def get_player_shots(matches, player_name):
    """
    Estrae i tiri di un giocatore specifico da tutte le partite.
    """
    player_shots = []
    for match in matches:
        for player in match['stats_giocatore']:
            if player['name'] == player_name and 'shots' in player:
                for shot in player['shots']:
                    x = shot.get('X')
                    y = shot.get('Y')
                    shot_result = shot.get('Made')
                    if x is not None and y is not None:
                        player_shots.append((x, y, shot_result))
    return player_shots
