import numpy as np
import matplotlib.pyplot as plt

def lese_werte_aus_datei(dateipfad):
    try:
        with open(dateipfad, 'r') as datei:
            zeilen = datei.readlines()
            del zeilen[0]
            cl = []
            cd = []
            e = []
            for i, _ in enumerate(zeilen):
                werte = zeilen[i].split()
                cl_new = float(werte[0])
                cd_new = float(werte[1])
                e_new = float(werte[2])

                cl.append(cl_new)
                cd.append(cd_new)
                e.append(e_new)

            return cl, cd, e

    except Exception as e:
        print(f"Fehler beim Lesen der Datei: {e}")
        return None

# Beispielaufruf
dateipfad = 'aero_data/cruise_aero_data.txt'  # Ersetze dies durch den tatsächlichen Pfad zu deiner Textdatei
werte = lese_werte_aus_datei(dateipfad)

if werte is not None:
    cl = [0., 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.56, 0.57, 0.58, 0.59, 0.6, 0.65, 0.7, 0.75]
    cd = [0.0108, 0.0123, 0.0132, 0.0143, 0.0156, 0.0171, 0.0188, 0.0208, 0.0238, 0.0246, 0.0254, 0.0264, 0.0274, 0.0288, 0.0366, 0.0530, 0.0947]

    plt.plot(cd, cl, label="Reference")
    plt.scatter(werte[1], werte[0], label="Your Data")
    plt.grid('on')
    plt.legend()
    plt.show()
