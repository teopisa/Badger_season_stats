# Badger Season Stats

Benvenuto nel progetto **Badger Season Stats**! Questo progetto raccoglie e analizza le statistiche delle partite di una stagione di basket, fornendo una panoramica delle performance di squadra e dei singoli giocatori.

## Descrizione

Questo progetto consente di caricare, visualizzare e analizzare le statistiche delle partite della stagione, sia per l'intera squadra che per ogni singolo giocatore. Puoi visualizzare le statistiche delle partite e dei giocatori, inclusi punti, assist, rimbalzi, e altre metriche rilevanti.

Le principali funzionalità di questa applicazione sono:

- Visualizzazione delle statistiche delle partite.
- Analisi delle statistiche per giocatore.
- Grafici e tabelle per esplorare i dati delle partite.

## Tecnologie utilizzate

- **Streamlit**: per la creazione dell'interfaccia utente e la visualizzazione dei dati.
- **Pandas**: per la gestione e l'analisi dei dati.
- **Matplotlib**: per la creazione di grafici (se usato nel progetto).
- **mplbasketball** (se utilizzato).

## Requisiti

Per eseguire l'applicazione localmente, assicurati di avere installato Python e le seguenti librerie:

- **streamlit** >= 1.0
- **pandas** >= 1.0
- **matplotlib** >= 3.0 (se utilizzato)
- **mplbasketball** (se utilizzato)

Puoi installare le librerie necessarie utilizzando `pip`:

```bash
pip install -r requirements.txt
git clone https://github.com/teopisa/Badger_season_stats.git
cd Badger_season_stats
pip install -r requirements.txt
streamlit run basketapp.py

Badger_season_stats/
├── basketapp.py               # Script principale che esegue l'app Streamlit
├── stats_functions.py         # Funzioni per caricare e manipolare i dati
├── stats_partita.py           # Funzioni per la visualizzazione delle statistiche delle partite
├── stats_giocatori.py         # Funzioni per la visualizzazione delle statistiche dei giocatori
├── season_stats/              # Cartella che contiene i dati delle partite (file JSON)
│   └── match_stats/
├── requirements.txt           # File con le librerie necessarie
└── README.md                  # Questo file
