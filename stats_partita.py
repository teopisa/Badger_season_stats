import streamlit as st
import pandas as pd
from mplbasketball import Court
from stats_functions import *
import matplotlib.pyplot as plt



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
    f"<p style='font-size: 40px;'>{quarter}: {scores}-{punti_per_partita[away_team][quarter]}</p>"
    for quarter, scores in punti_per_partita[home_team].items() if quarter != 'TOT'
    ])
    # Titolo e punteggio centrati
    st.markdown(
    f"""
    <div style="text-align: center;">
        <h1 style="font-size: 50px;">{home_team} vs {away_team}</h1>
        <h2 style="font-size: 50px;">{"Risultato:"}</h2>
        <h3 style="font-size: 50px;">{punti_home} - {punti_away}</h3>
        <h4 style="font-size: 50px;">{punti_text}</h4>
    </div>
    """,
    unsafe_allow_html=True
    )

   
    # Statistiche giocatori
    stats_giocatori = selected_match['stats_giocatore']

    for player in stats_giocatori:
        player['evaluation'] = (
            player['pts'] +
            player['reb'] +
            player['ast'] +
            player['bk'] +
            player['stl'] -
            player['2p_made'] - 
            player['3p_made']-
            player['ft_made'] -
            player['to'] -
            player['foul']
        )

    players_df = pd.DataFrame(stats_giocatori).drop(columns=['shots'], errors='ignore')
    players_df['ft_%'] = players_df['ft_%'].apply(lambda x: convert_percentage_to_string(x, selected_match))
    players_df['2p_%'] = players_df['2p_%'].apply(lambda x: convert_percentage_to_string(x, selected_match))
    players_df['3p_%'] = players_df['3p_%'].apply(lambda x: convert_percentage_to_string(x, selected_match))

    columns_to_select = ['shirtnumber', 'name', 'pts', 'evaluation',  'ft_%', '2p_made', '2p_taken', 
                         '2p_%', '3p_made', '3p_taken', '3p_%', 'reb', 'dreb', 
                         'orib', 'ast', 'to', 'foul', 'stl', 'bk', 'ft_made', 'ft_taken']
    valid_columns = [col for col in columns_to_select if col in players_df.columns]
    players_df = players_df[valid_columns].reset_index(drop=True)

    st.markdown(
    f"""
    <div style="text-align: center;">
        <h1 style="font-size: 50px;">{"Stats Giocatori"}</h1>
    </div>
    """,
    unsafe_allow_html=True
    )
    # Mostra la tabella con stile personalizzato
    styled_df = (
        players_df.style)
    
    st.dataframe(styled_df, hide_index= True, use_container_width= True, height=460)

    mvp = players_df.loc[players_df['evaluation'].idxmax()]
    mvp_text = (
        f"MVP: numero: {mvp['shirtnumber']}, {mvp['name']} | "
        f"Valutazione: {mvp['evaluation']} | "
        f"Punti:{mvp['pts']} | "
        f"Assist: {mvp['ast']} | "
        f"Rimbalzi: {mvp['reb']} | "
        f"Palle Recuperate: {mvp['stl']} | "
        f"Stoppate: {mvp['bk']}"
    )

    # Display MVP details
    st.markdown(
        f"""
        <div style="text-align: center; font-size: 22px; font-weight: bold; margin-top: 20px;">
            {mvp_text}
        </div>
        """,
        unsafe_allow_html=True
    )

    # Grafici a ciambella (Donut Chart)
    st.subheader("Statistiche della Squadra")
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
    selected_players = st.multiselect("Seleziona giocatori per visualizzare i tiri", ["Tutti"] + player_names)

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
    st.markdown(
    f"""
    <div style="text-align: center;">
        <h1 style="font-size: 50px;">{"Mappa Tiri"}</h1>
    </div>
    """,
    unsafe_allow_html=True
    )
    st.pyplot(fig)
