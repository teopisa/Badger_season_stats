import streamlit as st
import pandas as pd
from mplbasketball import Court
from stats_functions import *
import matplotlib.lines as mlines


def display_stats_giocatori(json_folder, matches):
    create_title_text("Stats Giocatori")

    if matches:
        # Creazione della lista di giocatori unici
        player_names = get_unique_player_names(matches)
        selected_player = st.selectbox("Seleziona un Giocatore", player_names)

        if selected_player:
            # Calcola le statistiche del giocatore
            player_stats = calculate_player_stats(matches, selected_player)

            # Toggle per visualizzare statistiche totali o per partita
            col1, col2, col3 = st.columns(3)
            with col2:
                toggle_stats = st.toggle(
                    "Visualizza Statistiche Medie per partita:"
                )

            if toggle_stats:
                st.success('Hai selezionato Statistiche per partita!')
                player_stats = {
                    key: round(value / player_stats['Partite Giocate'], 2) if isinstance(value, (int, float)) else value
                    for key, value in player_stats.items()
                    }

            # KPI Section
            create_title_text(f"Statistiche Chiave {selected_player}")
            col1, col2, col3 = st.columns(3)

            with col1:
                    st.markdown(kpi_card(player_stats["Punti Totali"], "Punti"), unsafe_allow_html=True)
            with col2:
                    st.markdown(kpi_card(player_stats["Rimbalzi Attacco Totali"], "Rimbalzi Off"), unsafe_allow_html=True)
            with col3:
                    st.markdown(kpi_card(player_stats["Rimbalzi Difesa Totali"], "Rimbalzi Dif"), unsafe_allow_html=True)

                # Seconda riga con altri KPI
            st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)

            col4, col5, col6 = st.columns(3)

            with col4:
                    st.markdown(kpi_card(player_stats["Stoppate Totali"], "Stoppate"), unsafe_allow_html=True)
            with col5:
                    st.markdown(kpi_card(player_stats["Palle Rubate Totali"], "Recuperi"), unsafe_allow_html=True)
            with col6:
                    st.markdown(kpi_card(player_stats["Assist Totali"], "Assist"), unsafe_allow_html=True)
        # Donut charts per percentuali tiri
        player_stats = calculate_player_stats(matches, selected_player)

        create_title_text("Statistiche al Tiro")
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
        create_title_text(f"Mappa Tiri: {selected_player}")
        court = Court(court_type="nba", origin="center", units="m")
        fig, ax = court.draw(showaxis=True, orientation="vu")

        # Filtra i tiri per il giocatore selezionato
        player_shots = get_player_shots(matches, selected_player)
        for x, y, shot_result in player_shots:
            color = 'orange' if shot_result else 'black'
            ax.plot(x, y, 'o', color=color, alpha=0.9, markersize=7)
            ax.set_xlim(-8, 8)  # x-axis from -8 to 8
            ax.set_ylim(0, 15)  # y-axis from 0 to 15
            orange_patch = mlines.Line2D([], [], marker='o', color='w', markerfacecolor='orange', markersize=10, label='Tiri Realizzati')
            black_patch = mlines.Line2D([], [], marker='o', color='w', markerfacecolor='black', markersize=10, label='Tiri Sbagliati')

            ax.legend(handles=[orange_patch, black_patch])

        st.pyplot(fig)

    else:
        st.write("Nessuna partita trovata nella cartella.")
