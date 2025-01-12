import streamlit as st
from stats_functions import *
from mplbasketball import Court

# Percorso della cartella delle partite
json_folder = 'season_stats/match_stats'

# Carica i dati delle partite
matches = load_json_files(json_folder)

# Pagine disponibili
st.sidebar.title("Menù")
page = st.sidebar.selectbox("Seleziona una pagina", ["Stats Partita", "Stats Giocatore"])

# Pagina: Stats Partita
if page == "Stats Partita":
    st.title("Statistiche della Partita")

    if matches:
        # Seleziona la partita
        match_options = [
            f"{match['info_partita']['home']} vs {match['info_partita']['away']} ({match['info_partita']['data']})" 
            for match in matches
        ]
        selected_match_name = st.selectbox("Seleziona una partita", match_options)
        selected_match = matches[match_options.index(selected_match_name)]

        # Mostra le informazioni della partita
        display_match_info(selected_match)

        # Visualizza la mappa dei tiri
        st.subheader("Shot Map")
        court = Court(court_type="nba", origin="center", units="m")
        fig, ax = court.draw(showaxis=True, orientation="vu", court_color='white', paint_color='white', line_color='black')
        ax.set_xlim(-8, 8)  # x-axis from -8 to 8
        ax.set_ylim(0, 15)  # y-axis from 0 to 15
        # Estrai e plotta i tiri
        shots_data = get_shots_for_players(matches, selected_match)
        for x, y, shot_result in shots_data:
            color = 'g' if shot_result else 'r'
            ax.plot(x, y, 'o', color=color, alpha=0.9, markersize=7)

        st.pyplot(fig)
    else:
        st.write("Nessuna partita trovata nella cartella.")

# Pagina: Stats Giocatore
elif page == "Stats Giocatore":
    st.title("Statistiche del Giocatore")

    if matches:
        # Creazione della lista di giocatori unici
        player_names = get_unique_player_names(matches)
        selected_player = st.selectbox("Seleziona un Giocatore", player_names)

        if selected_player:
            # Calcola le statistiche del giocatore
            player_stats = calculate_player_stats(matches, selected_player)

            # Mostra le statistiche del giocatore
            display_player_stats(selected_player, player_stats)

            # Visualizza la mappa dei tiri
            st.subheader(f"Shot map per {selected_player}")

            court = Court(court_type="nba", origin="center", units="m")
            fig, ax = court.draw(showaxis=True, orientation="vu", court_color='orange', paint_color='black', line_color='white')

            # Filtra i tiri per il giocatore selezionato
            player_shots = get_player_shots(matches, selected_player)

            for x, y, shot_result in player_shots:
                color = 'g' if shot_result else 'r'
                ax.plot(x, y, 'o', color=color, alpha=0.9, markersize=7)
                ax.set_xlim(-8, 8)  # x-axis from -8 to 8
                ax.set_ylim(0, 15)  # y-axis from 0 to 15

            st.pyplot(fig)
    else:
        st.write("Nessuna partita trovata nella cartella.")