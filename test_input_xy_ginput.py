import matplotlib.pyplot as plt
from mplbasketball import Court

# Configura il campo
court = Court(court_type="nba", origin="center", units="m")  # Puoi cambiare il tipo di campo se serve
fig, ax = court.draw(orientation="h")

# Prompt per inserire i punti
plt.title("Clicca sui punti di tiro e chiudi la finestra quando hai finito.")
plt.xlabel("X - Coordinate (m)")
plt.ylabel("Y - Coordinate (m)")

# Usa ginput per prendere le coordinate con i clic
num_points = int(input("Quanti tiri vuoi registrare? "))
print("Seleziona i punti sul campo (clicca e premi Enter su ogni punto).")

# Attiva la selezione di punti
shot_coordinates = plt.ginput(num_points, timeout=-1)  # timeout -1 permette selezioni senza limiti di tempo
plt.close(fig)  # Chiude la finestra dopo aver selezionato i punti

# Stampa e salva le coordinate
for i, coord in enumerate(shot_coordinates, start=1):
    print(f"Tiro {i}: X = {coord[0]:.2f}, Y = {coord[1]:.2f}")

# Se vuoi salvare i risultati, li puoi mettere in un file JSON o CSV
import json
shot_data = [{"Tiro": i + 1, "X": coord[0], "Y": coord[1]} for i, coord in enumerate(shot_coordinates)]

with open("shot_data.json", "w") as f:
    json.dump(shot_data, f)

print("Coordinate salvate in shot_data.json")
