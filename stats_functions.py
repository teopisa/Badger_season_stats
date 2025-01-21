import os
import json
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


def convert_percentage_to_string(percentage, match):
    """
    Convert percentage to string format with appropriate handling based on the match context.
    """
    
    if match == 'season_stats/match_stats/badgers_potascetbasket_20241007.json':
        return f"{percentage * 100}%"
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
        "Punti per Partita": 0,
        "Rimbalzi Totali": 0,
        "Rimbalzi Difesa Totali": 0,
        "Rimbalzi Attacco Totali": 0,
        "Rimbalzi per Partita": 0,
        "Assist Totali": 0,
        "Assist per Partita": 0,
        "Stoppate Totali": 0,
        "Stoppate per Partita": 0,
        "Falli Totali": 0,
        "Falli per Partita": 0,
        "Tiri da 2 Realizzati": 0,
        "Tiri da 2 Tentati": 0,
        "Tiri da 3 Realizzati": 0,
        "Tiri da 3 Tentati": 0,
        "Tiri Liberi Realizzati": 0,
        "Tiri Liberi Tentati": 0,
    }

    matches_played = 0

    for match in matches:
        for player in match['stats_giocatore']:
            if player['name'] == player_name:
                matches_played += 1
                total_stats["Punti Totali"] += player['pts']
                total_stats["Rimbalzi Totali"] += player['reb']
                total_stats["Rimbalzi Difesa Totali"] += player['dreb']
                total_stats["Rimbalzi Attacco Totali"] += player['orib']
                total_stats["Assist Totali"] += player['ast']
                total_stats["Stoppate Totali"] += player['bk']
                total_stats["Falli Totali"] += player['foul']
                total_stats["Tiri da 2 Realizzati"] += player['2p_made']
                total_stats["Tiri da 2 Tentati"] += player['2p_taken']
                total_stats["Tiri da 3 Realizzati"] += player['3p_made']
                total_stats["Tiri da 3 Tentati"] += player['3p_taken']
                total_stats["Tiri Liberi Realizzati"] += player['ft_made']
                total_stats["Tiri Liberi Tentati"] += player['ft_taken']

    # Calcolo delle statistiche per partita
    if matches_played > 0:
        total_stats["Punti per Partita"] = (total_stats["Punti Totali"] / matches_played)
        total_stats["Rimbalzi per Partita"] = (total_stats["Rimbalzi Totali"] / matches_played)
        total_stats["Assist per Partita"] = (total_stats["Assist Totali"] / matches_played)
        total_stats["Stoppate per Partita"] = (total_stats["Stoppate Totali"] / matches_played)
        total_stats["Falli per Partita"] = (total_stats["Falli Totali"] / matches_played)

    # Calcola percentuali
    total_stats["% Tiri da 2"] = f"{(total_stats['Tiri da 2 Realizzati'] / total_stats['Tiri da 2 Tentati'] * 100):.0f}%" if total_stats['Tiri da 2 Tentati'] > 0 else "0%"
    total_stats["% Tiri da 3"] = f"{(total_stats['Tiri da 3 Realizzati'] / total_stats['Tiri da 3 Tentati'] * 100):.0f}%" if total_stats['Tiri da 3 Tentati'] > 0 else "0%"
    total_stats["% Tiri Liberi"] = f"{(total_stats['Tiri Liberi Realizzati'] / total_stats['Tiri Liberi Tentati'] * 100):.0f}%" if total_stats['Tiri Liberi Tentati'] > 0 else "0%"

    return total_stats


# Mostra statistiche del giocatore
def display_player_stats(player_name, stats):
    st.subheader(f"Statistiche di {player_name}")
    stats_df = pd.DataFrame({
        "Statistiche": list(stats.keys()),
        "Valore": list(stats.values())
    })
    styled_df = (
    stats_df.style)
    st.dataframe(styled_df, hide_index= True, use_container_width= True, height=460)

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


def create_donut_chart(label, value, total, color):
    """Crea un grafico a ciambella uniforme con il testo al centro."""
    if value == 0:
        # Se nessun tiro è stato tentato, mostra un testo invece del grafico
        fig, ax = plt.subplots()
        ax.text(
            0.5, 0.5, f"Nessun {label} tentato",
            ha='center', va='center', fontsize=14,
            bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="lightgray")
        )
        ax.axis('off')  # Rimuove gli assi
        return fig

    fig, ax = plt.subplots(figsize=(4, 4))  # Dimensione uniforme
    ax.pie(
        [value, total - value],
        startangle=90,
        colors=[color, 'black'],
        wedgeprops=dict(width=0.3, edgecolor='white')  # Imposta spessore ciambella
    )
    
    # Aggiungi testo al centro
    percentage = int((value / total) * 100) if total > 0 else 0
    ax.text(0, 0, f"{label}\n{value}/{total}\n{percentage}%", 
            ha='center', va='center', fontsize=14, color='black', weight='bold')
    
    # Rimuovi il contorno esterno
    ax.set_aspect('equal')  # Assicura che sia perfettamente rotondo
    return fig

def calculate_player_evaluation(matches, player_name):
    total_evaluation = 0
    matches_played = 0

    for match in matches:
        for player in match['stats_giocatore']:
            if player['name'] == player_name:
                matches_played += 1

                # Calcolo della valutazione per la partita
                evaluation = (
                    player['pts'] +
                    player['reb'] +
                    player['ast'] +
                    player['bk'] +
                    player['stl'] -
                    (player['2p_taken'] - player['2p_made']) -
                    (player['3p_taken'] - player['3p_made']) -
                    (player['ft_taken'] - player['ft_made']) -
                    player['to'] -
                    player['foul']
                )
                total_evaluation += evaluation

    # Calcolo media della valutazione
    average_evaluation = round(total_evaluation / matches_played, 1) if matches_played > 0 else 0
    return {"Valutazione Totale": total_evaluation, "Valutazione Media": average_evaluation}
