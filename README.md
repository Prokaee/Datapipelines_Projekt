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
- Daten: Robert Shiller, *U.S. Stock Markets 1871–Present*, <https://shillerdata.com/> (`ie_data.xls`, Stand 26.10.2026 in `data/raw/`)

## Dateien

| Datei | Inhalt |
|---|---|
| `01_preprocessing.ipynb` / `.html` | Laden, Cleaning, Features, Zielwerte |
| `data/raw/ie_data.xls` | Rohdaten, unverändert |
| `data/shiller_clean.csv` | bereinigte Daten, Basis für EDA und Modelle |
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
