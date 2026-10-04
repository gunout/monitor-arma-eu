<!-- Badges -->
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![HTML5](https://img.shields.io/badge/HTML-5-E34F26?logo=html5&logoColor=white)](https://developer.mozilla.org/docs/Web/HTML)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES2022-F7DF1E?logo=javascript&logoColor=black)](https://developer.mozilla.org/docs/Web/JavaScript)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Node.js](https://img.shields.io/badge/Node.js-18+-339933?logo=node.js&logoColor=white)](https://nodejs.org/)
[![Made in Ukraine](https://img.shields.io/badge/Made%20in-Ukraine-0057B7?logo=ukraine&logoColor=FFD700)](https://data.gov.ua/)

![Files](https://img.shields.io/badge/files-11-blue)
![Indicators](https://img.shields.io/badge/indicators%20extracted-172-green)
![Status](https://img.shields.io/badge/status-operational-success)

---

# 🇺🇦 Монітор АРМА — Експертиза бюджетних програм

> **Dashboard d'analyse** des rapports annuels d'exécution des passeports budgétaires de l'**ARMA** — Національне агентство України з питань виявлення, розшуку та управління активами, одержаними від корупційних та інших злочинів.

---

## 📖 Table des matières

- [Contexte](#-contexte)
- [Fonctionnalités](#-fonctionnalités)
- [Résultats](#-résultats)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Parser ARMA](#-parser-arma)
- [Structure du projet](#-structure-du-projet)
- [Feuille de route](#-feuille-de-route)
- [Contribuer](#-contribuer)
- [Licence](#-licence)
- [Sources](#-sources)

---

## 🌍 Contexte

L'**ARMA** (Національне агентство України з питань виявлення, розшуку та управління активами) publie chaque année un **rapport d'exécution du passeport budgétaire** — un document structuré contenant :

- Les métadonnées administratives (КПКВК, розпорядник, програма)
- Les 10 sections réglementaires
- **4 groupes d'indicateurs** : затрат / продукту / ефективності / якості
- Le plan, le factuel et le taux d'exécution pour chaque indicateur

Ces rapports sont publiés sur [data.gov.ua](https://data.gov.ua/) dans des formats **Crystal Reports** (`.xls`) et **Excel modernes** (`.xlsx`), **difficilement exploitables** en l'état.

**Ce projet** fournit un dashboard qui **parse, normalise et visualise** ces rapports automatiquement.

---

## ✨ Fonctionnalités

### 🔬 Analyse automatique

- **Détection du format** — reconnaît `.xls` (Crystal Reports 2018-2024) et `.xlsx` (2025)
- **Extraction des 10 sections** du passeport budgétaire
- **Parsing des 4 groupes d'indicateurs** avec plan/factuel/écart/%
- **Calcul automatique** du taux d'exécution

### 🎨 Interface

- **Bandeau Ukraine** (bleu/jaune) et design responsive
- **Recherche** par titre, description, tags, organisation
- **Filtres** par catégorie (8 catégories thématiques)
- **Pagination** configurable (10 / 25 / 50 par page)
- **3 vues** : Résultats / Expertise / Monitoring

### 📊 Visualisation

- **Graphiques** Chart.js (types, remplissage, cardinalité, distribution)
- **Tableaux** statistiques par colonne
- **Aperçu** des 10 premières lignes
- **Comparaison** entre datasets

### 🔒 Sécurité

- **Détection PII** : emails, IBAN UA, téléphones, ІПН, ЄДРПОУ
- **Alertes** critiques vs avertissements
- **Export PDF** des rapports

### 🛠️ Infrastructure

- **Serveur Express** pour servir les fichiers statiques
- **Proxy CORS** whitelist (data.europa.eu, data.gov.ua)
- **Cloudflare Worker** alternatif (sans backend)
- **Générateur** `arma.json` depuis l'API ou les fichiers locaux

---

## 📊 Résultats

**Analyse de 4 rapports annuels — 172 indicateurs extraits :**

| Année | Format | Sections | Indicateurs | Затрат | Продукту | Ефект. | Якості |
|:-----:|:------:|:--------:|:-----------:|:------:|:--------:|:------:|:------:|
| **2018** | `.xls` | 8 | **42** | 11 | 15 | 9 | 7 |
| **2021** | `.xls` | 9 | **40** | 13 | 20 | 3 | 4 |
| **2024** | `.xls` | 9 | **39** | 15 | 15 | 2 | 7 |
| **2025** | `.xlsx` | 10 | **51** | 16 | 19 | 7 | 9 |
| | | | **172** | 55 | 69 | 21 | 27 |

**Score de conformité global : 100/100**

---

## 🏗️ Architecture

Le projet est **100% client-side** pour le parsing, avec un serveur Express minimal pour servir les fichiers statiques.

| Couche | Composant | Rôle |
|--------|-----------|------|
| Client | `index.html` | UI + parser ARMA (1300 lignes) |
| Client | Chart.js | Graphiques |
| Client | SheetJS | Parsing Excel |
| Client | jsPDF | Export PDF |
| Serveur | `server.js` (Express) | Fichiers statiques + proxy CORS |
| Serveur | `worker.js` (Cloudflare) | Alternative serverless |
| Données | `arma.json` | Catalogue des datasets |

**Technologies** : HTML5 · CSS3 · JavaScript ES2022 · SheetJS 0.18.5 · Chart.js 4.4.0 · jsPDF 2.5.1 · Express 4.19.2 · Python 3.10+

---

## 🚀 Installation

### Prérequis

| Outil | Version | Usage |
|-------|---------|-------|
| **Node.js** | >= 18 | Serveur Express |
| **Python** | >= 3.10 | Génération arma.json |
| **Git** | >= 2.30 | Versionnage |

### Étapes

1. Cloner le dépôt : `git clone https://github.com/gunout/monitor-arma-eu.git`
2. Aller dans le dossier : `cd monitor-arma-eu`
3. Installer les dépendances Node : `npm install`
4. Placer les 4 fichiers Excel ARMA à la racine (téléchargeables depuis data.gov.ua)
5. Générer arma.json : `python3 build_local.py`
6. Lancer le serveur : `node server.js`
7. Ouvrir : http://localhost:3000/index.html

---

## 💻 Utilisation

### Analyser un rapport

1. Cliquer sur le **dataset ARMA** dans la liste
2. Aller dans l'onglet **Експертиза**
3. Cliquer sur **Експертиза** pour chaque ressource

### Ce que vous obtenez

- Metadonnees : 643 / 6431000 / 6431010 / 0111
- Sections : 10 (2018) ou 8 (2025)
- Indicateurs : 42 a 51 selon l'annee
- Repartition : Затрат / Продукту / Ефективності / Якості
- Plan / Fakt / % d'execution par indicateur

### Fonctions avancees

| Action | Ou |
|---|---|
| Export PDF | Bouton "Експорт PDF" |
| Comparer 2 datasets | Bouton "Порівняти" |
| Monitoring automatique | Onglet "Моніторинг" |
| Scan PII | Onglet "PII" |
| Tout expertiser | Bouton "Експертиза всіх" |

---

## ⚙️ Parser ARMA

### Detection du format

Le parser cherche **10 marqueurs textuels** dans les 200 premieres lignes :

- Version 2025 : "Цілі державної політики", "Мета бюджетної програми", "Завдання бюджетної програми"
- Version 2018-2024 : "Стратегічні цілі", "Видатки за бюджетною програмою", "Напрями використання бюджетних коштів"
- Commun : "Результативні показники бюджетної програми", "Головного розпорядника", "Відповідального виконавця"

Si >= 2 marqueurs trouves, c'est un passeport ARMA.

### Extraction des sections

Identifie les sections numerotees (1. a 10.) et les associe a leur role :

| Version | Sections 1-3 | Section 4 | Section 5 | Section 6 | Section 9 |
|---|---|---|---|---|---|
| 2025 | Entites | Цілі політики | Мета | Завдання | Показники |
| 2018-2024 | Entites | Стратегічні цілі | Видатки | Напрями | Показники |

### Extraction des indicateurs

Detecte les 4 groupes par cellule isolee :

    затрат -> продукту -> ефективності -> якості

Pour chaque indicateur : N° / Nom / Unite / Source / Plan / Fakt / Ecart

---

## 📁 Structure du projet

    monitor-arma-eu/
    ├── index.html              # Dashboard complet
    ├── server.js               # Serveur Express + proxy CORS
    ├── worker.js               # Cloudflare Worker
    ├── build_local.py          # Generateur arma.json (local)
    ├── build_arma_json.py      # Generateur arma.json (API)
    ├── arma.json               # Catalogue des datasets
    ├── requirements.txt        # Dependances Python
    ├── package.json            # Dependances Node
    ├── README.md               # Ce fichier
    ├── LICENSE                 # MIT
    └── .gitignore              # Exclusions Git

---

## 🗺️ Feuille de route

### Fait

- [x] Parser multi-format .xls / .xlsx
- [x] Extraction des 10 sections
- [x] Extraction des 4 groupes d'indicateurs
- [x] Detection PII ukrainienne
- [x] Export PDF
- [x] Interface responsive
- [x] Depot GitHub + README + LICENSE

### En cours

- [ ] Correction "Мета" tronquee sur 2018
- [ ] Correction plan/fakt inverses sur .xls
- [ ] Affinage du PII (faux positifs dates)
- [ ] Selecteur de feuille Excel

### Prevu

- [ ] Deploiement en ligne (Cloudflare Pages / GitHub Pages)
- [ ] GitHub Actions pour CI/CD
- [ ] Comparaison pluriannuelle automatique
- [ ] Export Excel en plus du PDF
- [ ] API REST pour integration externe
- [ ] Tests unitaires (Jest / Pytest)
- [ ] Docker pour deploiement self-hosted

---

## 🤝 Contribuer

Les contributions sont bienvenues.

Processus :

1. Fork le projet
2. Creer une branche (`git checkout -b feature/ma-fonctionnalite`)
3. Commit (`git commit -m 'Add some feature'`)
4. Push (`git push origin feature/ma-fonctionnalite`)
5. Ouvrir une Pull Request

Signaler un bug : ouvrez une issue sur https://github.com/gunout/monitor-arma-eu/issues

---

## ⚖️ Licence

Distribue sous licence **MIT**. Voir [LICENSE](LICENSE).

MIT License - Copyright (c) 2026 gunout

---

## 🔗 Sources

- data.gov.ua - Donnees brutes ARMA
- data.europa.eu - Portail EU Open Data
- arma.gov.ua - Site de l'agence
- SheetJS - Parsing Excel
- Chart.js - Graphiques
- jsPDF - Export PDF

---

Слава Україні! Героям слава!

Developpe avec amour pour la transparence budgetaire ukrainienne.

---

<div align="center">

### 🇫🇷 Gunout · 2026

![Made in France](https://img.shields.io/badge/Made_in-France-002395?style=flat-square&labelColor=FFFFFF&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA5MDAgNjAwIj48cmVjdCB3aWR0aD0iOTAwIiBoZWlnaHQ9IjYwMCIgZmlsbD0iIzAwMjM5NSIvPjxyZWN0IHdpZHRoPSI5MDAiIGhlaWdodD0iNDAwIiB5PSIxMDAiIGZpbGw9IiNmZmYiLz48cmVjdCB3aWR0aD0iOTAwIiBoZWlnaHQ9IjIwMCIgeT0iNDAwIiBmaWxsPSIjZWQyOTM5Ii8+PC9zdmc+)
![GitHub](https://img.shields.io/badge/GitHub-gunout-181717?style=flat-square&logo=github&logoColor=white)
![Year](https://img.shields.io/badge/2026-ED2939?style=flat-square&labelColor=FFFFFF)

<sub>© 2026 <strong>Gunout</strong> — Tous droits réservés.</sub>

</div>

