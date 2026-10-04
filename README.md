# 🇺🇦 Монітор АРМА — Експертиза бюджетних програм

Dashboard d'analyse des rapports annuels d'exécution des passeports budgétaires de l'ARMA (Національне агентство України з питань виявлення, розшуку та управління активами, одержаними від корупційних та інших злочинів).

## 🎯 Fonctionnalités

- **Analyse automatique** des rapports annuels (2018, 2021, 2024, 2025)
- **Extraction** des métadonnées (КПКВК, розпорядник, програма)
- **Détection** des sections 1-10 du паспорт бюджетної програми
- **Extraction** des 4 groupes d'indicateurs : затрат / продукту / ефективності / якості
- **Calcul** du taux d'exécution (План / Факт / %) par indicateur
- **Détection PII** (emails, IBAN UA, téléphones, ІПН, ЄДРПОУ)
- **Export PDF** des rapports d'analyse
- **Comparaison** de jeux de données

## 📊 Résultats (4 fichiers analysés)

| Année | Sections | Indicateurs | Затрат | Продукту | Ефект. | Якості |
|-------|----------|-------------|--------|----------|--------|--------|
| 2018  | 8        | 42          | 11     | 15       | 9      | 7      |
| 2021  | 9        | 40          | 13     | 20       | 3      | 4      |
| 2024  | 9        | 39          | 15     | 15       | 2      | 7      |
| 2025  | 10       | 51          | 16     | 19       | 7      | 9      |

**Total : 172 indicateurs extraits.**

## 🚀 Installation

### Prérequis

- Node.js >= 18
- Python >= 3.10 (pour générer arma.json)

### Démarrage

    # 1. Cloner le dépôt
    git clone https://github.com/gunout/monitor-arma-eu.git
    cd monitor-arma-eu

    # 2. Installer les dépendances Node
    npm install

    # 3. Placer les fichiers Excel ARMA à la racine
    #    (téléchargeables depuis data.gov.ua)

    # 4. Générer arma.json
    python3 build_local.py

    # 5. Lancer le serveur
    node server.js

Ouvrir : http://localhost:3000/index.html

## 📁 Structure

    monitor-arma-eu/
    ├── index.html              # Dashboard complet (client-side)
    ├── server.js               # Serveur Express + proxy CORS
    ├── worker.js               # Cloudflare Worker (proxy alternatif)
    ├── build_local.py          # Génère arma.json depuis les fichiers locaux
    ├── build_arma_json.py      # Génère arma.json depuis data.europa.eu
    ├── arma.json               # Catalogue des datasets
    ├── package.json
    ├── requirements.txt
    ├── .gitignore
    ├── LICENSE
    └── README.md

## 🛠️ Architecture

- **Frontend** : HTML / CSS / JavaScript vanilla
- **Parsing Excel** : SheetJS (xlsx.full.min.js)
- **Graphiques** : Chart.js
- **Export PDF** : jsPDF + autoTable
- **Backend** : Express (Node.js) — fichiers statiques + proxy CORS

## ⚙️ Parser ARMA

Le parser détecte automatiquement la structure du паспорт бюджетної програми :

1. **Détection** : isARMAPassport() cherche les marqueurs textuels
2. **Sections** : parseARMAPassport() identifie les 10 sections
3. **Indicateurs** : parseIndicatorsSection() parse les 4 groupes
4. **Compatible** avec .xls (Crystal Reports 2018-2024) et .xlsx (2025)

## 📜 License

MIT — voir LICENSE

## 🔗 Sources

- data.gov.ua — données brutes (АРМА)
- data.europa.eu — portail EU Open Data
