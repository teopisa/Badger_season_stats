import streamlit as st
import pandas as pd
from mplbasketball import Court
from stats_functions import *
import matplotlib.pyplot as plt
import matplotlib.lines as mlines



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

    # Info partita
    home_team = selected_match['info_partita']['home']
    away_team = selected_match['info_partita']['away']
    punti_home = selected_match['stats_partita']['Punti_per_partita'][home_team]['TOT']
    punti_away = selected_match['stats_partita']['Punti_per_partita'][away_team]['TOT']

     # Punti per partita come testo
    punti_per_partita = selected_match['stats_partita']['Punti_per_partita']
    punti_text = "".join([
    f"<p style='font-size: 30px;'>{quarter}: {scores}-{punti_per_partita[away_team][quarter]}</p>"
    for quarter, scores in punti_per_partita[home_team].items() if quarter != 'TOT'
    ])

    # Titolo e punteggio centrati
    st.markdown(
    f"""
    <div style="text-align: center;">
        <h1 style="font-size: 50px;">{home_team} vs {away_team}</h1>
        <h2 style="font-size: 50px;">{"Risultato:"}</h2>
        <h3 style="font-size: 50px;">{punti_home} - {punti_away}</h3>
    </div>
    """,
    unsafe_allow_html=True
    )
    col1, col2, col3 = st.columns(3)

    with col2:
        st.dataframe(punti_per_partita, use_container_width=True)
    # Statistiche giocatori
    stats_giocatori = selected_match['stats_giocatore']

    for player in stats_giocatori:
        player_evaluation(player)

    players_df = pd.DataFrame(stats_giocatori).drop(columns=['shots'], errors='ignore')
    players_df['ft_%'] = players_df['ft_%'].apply(lambda x: convert_percentage_to_string(x, selected_match))
    players_df['2p_%'] = players_df['2p_%'].apply(lambda x: convert_percentage_to_string(x, selected_match))
    players_df['3p_%'] = players_df['3p_%'].apply(lambda x: convert_percentage_to_string(x, selected_match))

    columns_to_select = ['shirtnumber', 'name', 'pts', 'evaluation',  'ft_%', 'ft_made', 'ft_taken',
                         '2p_made', '2p_taken', 
                         '2p_%', '3p_made', '3p_taken', '3p_%', 'reb', 'dreb', 
                         'orib', 'ast', 'to', 'foul', 'stl', 'bk']
    valid_columns = [col for col in columns_to_select if col in players_df.columns]
    players_df = players_df[valid_columns].reset_index(drop=True)

    create_title_text("Stats Giocatori")

    # Mostra la tabella con stile personalizzato
    styled_df = (
        players_df.style)
    
    st.dataframe(styled_df, hide_index= True, use_container_width= True, height=460)

    

    # Display MVP details
    st.markdown(
        f"""
        <div style="text-align: center; font-size: 22px; font-weight: bold; margin-top: 20px;">
            {define_mvp_match(players_df=players_df)}
        </div>
        """,
        unsafe_allow_html=True
    )

    # Grafici a ciambella (Donut Chart)
    create_title_text("Stats al tiro")

    statistiche_squadra = selected_match['stats_partita']['Statistiche_squadra']
    col1, col2, col3 = st.columns(3)

    with col1:
        fig = create_donut_chart("Free Throws", statistiche_squadra['ft']['made'], statistiche_squadra['ft']['attempted'], "orange")
        st.pyplot(fig)
    with col2:
        fig = create_donut_chart("2-Point FG", statistiche_squadra['2pt']['made'], statistiche_squadra['2pt']['attempted'], "orange")
        st.pyplot(fig)
    with col3:
        fig = create_donut_chart("3-Point FG", statistiche_squadra['3pt']['made'], statistiche_squadra['3pt']['attempted'], "orange")
        st.pyplot(fig)

    # Mappa tiri
    court = Court(court_type="nba", origin="center", units="m")
    fig, ax = court.draw(showaxis=True, orientation="vu", court_color='white', paint_color='white', line_color='black')

    player_names = [player['name'] for player in stats_giocatori]
    selected_players = st.multiselect("Puoi selezionare anche più di un giocatore", ["Tutti"] + player_names)

    if "Tutti" in selected_players or not selected_players:
        shots_data = get_shots_for_players(matches, selected_match)
    else:
        shots_data = []
        for player_name in selected_players:
            player_shots = next(player['shots'] for player in stats_giocatori if player['name'] == player_name)
            shots_data.extend([(shot['X'], shot['Y'], shot['Made']) for shot in player_shots])

    for x, y, shot_result in shots_data:
        color = 'orange' if shot_result else 'black'
        ax.plot(x, y, 'o', color=color, alpha=0.9, markersize=7)

    ax.set_xlim(-8, 8)
    ax.set_ylim(0, 15)
    orange_patch = mlines.Line2D([], [], marker='o', color='w', markerfacecolor='orange', markersize=10, label='Tiri Realizzati')
    black_patch = mlines.Line2D([], [], marker='o', color='w', markerfacecolor='black', markersize=10, label='Tiri Sbagliati')

    ax.legend(handles=[orange_patch, black_patch])

    create_title_text("Mappa Tiri")
    st.pyplot(fig)
