# Data Analysis Project – FDEA WS26

Gruppenprojekt (max. 3 Personen, 30 Punkte) in Foundations of Data Engineering and Analytics.
Angabe: [Angabe/project.pdf](Angabe/project.pdf), Regeln: [Angabe/guidelines.pdf](Angabe/guidelines.pdf).

Thema: **Multi-Horizon Stock Market Return Forecasting, Factor Premiums, and Drawdown Dynamics**

Forschungsfrage: Wie gut sagen Bewertung (P/E, CAPE), Momentum, Volatilität und Drawdown die realen Aktienrenditen über 1, 5 und 10 Jahre voraus, und schlagen Timing- oder Faktorstrategien einfaches Buy-and-Hold?

## Team

| Name | GitHub |
|---|---|
| Michael Prokop | Prokaee |
| Raphael Erler | E3472 |
| Richard Zallinger | Richard12321 |

## Links

- Konzept (Google Doc): <https://docs.google.com/document/d/1FOaJ99wdJmuM_hL40cUTRf_Pdub8NUN0EDKZzbIuM78/edit?usp=sharing>
- Präsentation Konzept (Google Slides): <https://docs.google.com/presentation/d/1dBuTkAMHYQ3pNvWY-ldbyVkEiVOrH2IF/edit?usp=sharing&ouid=108864958121520797417&rtpof=true&sd=true>
- Repo: <https://github.com/Prokaee/Datapipelines_Projekt>
- Daten:
  - Robert Shiller, *U.S. Stock Markets 1871–Present*, <https://shillerdata.com/> (`ie_data.xls`, Stand 26.10.2026 in `data/raw/`)
  - Kenneth R. French Data Library, *Fama/French 3 Factors (1-Month U.S. Treasury Bill `RF`, 1926–2026)*, <https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html> (`F-F_Research_Data_Factors.csv` in `data/raw/`)

## Dateien

| Datei | Inhalt |
|---|---|
| `01_preprocessing.ipynb` / `.html` | Laden, Cleaning, Inflations-, Anleihen- (10Y & 1M T-Bill) und Aktien-Indizes, Features, Zielwerte |
| `02_eda.ipynb` / `.html` | Explorative Datenanalyse (uni-, bi- und multivariat, grafisch & nicht-grafisch, Implikationen für Feature Engineering & Modeling) |
| `eda_utils.py` | Wiederverwendbare Plot-, Statistik- und Export-Hilfsfunktionen für die EDA |
| `results/` | Direkt einsehbare EDA-Ergebnisse (`results/README.md`, `results/figures/*.png`, `results/tables/*.csv` & `*.md`) |
| `data/raw/ie_data.xls` | Shiller-Rohdaten (1871–2026), unverändert |
| `data/raw/F-F_Research_Data_Factors.csv` | Kenneth-French-Rohdaten inkl. 1M U.S. Treasury Bill Rate `RF` (1926–2026) |
| `data/shiller_clean.csv` | Bereinigte Daten (1.866 Monate, 32 Spalten), Basis für EDA und Modelle |
| `praesentation/index.html` / `deck.pdf` | Konzept-Präsentation (im Browser öffnen, F11, Pfeiltasten; PDF als Backup) |

## Deadlines (OLAT, jeweils 23:59)

| Datum | Abgabe |
|---|---|
| 27.10.2026 | Konzept (~2 Seiten), Preprocessing-Notebook (ipynb + html), Datasheet (pdf) |
| 24.11.2026 | Explorative Datenanalyse (ipynb + html) |
| 19.01.2027 | Finale Abgabe: Konzept, Datasheet, team.txt, Daten (csv), Notebooks (ipynb + html) |

Präsentationen: Konzept 04./11./18.11., EDA 02./09./16.12., Finale 20.01.2027.

## Punkte

| Teil | Punkte |
|---|---|
| Konzept | 4 |
| Data Processing | 4 |
| EDA | 6 |
| Modeling & Evaluation | 10 |
| Hypothesentest | 2 |
| Interpretation | 4 |

## Material

- `Folien/`: Vorlesungsfolien (neue Folien hier ablegen)
- Kurs-Notebooks als Vorlage für Methoden: <https://git.uibk.ac.at/informatik/dbis/dbis-teaching/data-engineering-analytics-notebooks>
- Datasheet-Vorlage: Gebru et al., *Datasheets for Datasets*, <https://arxiv.org/abs/1803.09010>

## Setup

Python-Umgebung wie in den Kurs-Notebooks: `pipenv install`, dann `pipenv run jupyter lab`.
