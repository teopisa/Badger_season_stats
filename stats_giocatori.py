import streamlit as st
import pandas as pd
from mplbasketball import Court
from stats_functions import *

def display_stats_giocatori(json_folder, matches):
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
            col1, col2, col3 = st.columns(3)

            
            with col1:
                fig = create_donut_chart("Tiri da 2", player_stats["Tiri da 2 Realizzati"], player_stats["Tiri da 2 Tentati"], "orange")
                st.pyplot(fig)
                
            with col2:
                fig = create_donut_chart("Tiri da 3", player_stats["Tiri da 3 Realizzati"], player_stats["Tiri da 3 Tentati"], "orange")
                st.pyplot(fig)
            with col3:
                fig = create_donut_chart("Tiri Liberi", player_stats["Tiri Liberi Realizzati"], player_stats["Tiri Liberi Tentati"], "orange")
                st.pyplot(fig)

            # Visualizza la mappa dei tiri
            st.subheader(f"Shot map per {selected_player}")

            court = Court(court_type="nba", origin="center", units="m")
            fig, ax = court.draw(showaxis=True, orientation="vu")

            # Filtra i tiri per il giocatore selezionato
            player_shots = get_player_shots(matches, selected_player)

            for x, y, shot_result in player_shots:
                color = 'orange' if shot_result else 'black'
                ax.plot(x, y, 'o', color=color, alpha=0.9, markersize=7)
                ax.set_xlim(-8, 8)  # x-axis from -8 to 8
                ax.set_ylim(0, 15)  # y-axis from 0 to 15

            st.pyplot(fig)
    else:
        st.write("Nessuna partita trovata nella cartella.")