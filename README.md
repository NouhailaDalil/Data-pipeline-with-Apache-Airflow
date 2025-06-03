#  Data Pipeline with Apache Airflow
![Capture d'écran 2025-01-29 114111](https://github.com/user-attachments/assets/b36c1255-ad65-4a48-86c0-3966e556741c)

Ce projet met en place un pipeline de données automatisé permettant d'extraire, charger et stocker des données générées dynamiquement via une API, le tout orchestré avec Apache Airflow sous Docker.

## 🎯 Objectif du projet

L’objectif est de construire un pipeline **modulaire, reproductible et automatisé**, démontrant la maîtrise des outils d’orchestration modernes (Airflow) et des bases de données relationnelles (PostgreSQL) dans un environnement conteneurisé (Docker).

---

## 📌 Données utilisées

- **Source** : API Mockaroo – permet de simuler un flux de données transactionnelles (clients, ventes, etc.)
- **Format** : Données JSON récupérées par requêtes HTTP

---

## ⚙️ Architecture du pipeline

Le pipeline suit le schéma **ETL** :

1. **Extraction (E)** : appel à l’API Mockaroo pour récupérer des données JSON.
2. **Transformation (T)** : parsing et préparation des données via Python.
3. **Chargement (L)** : insertion des données nettoyées dans une base PostgreSQL structurée en 3 couches :
   - `raw_layer`
   - `refined_layer`
   - `report_layer`

Le tout est orchestré avec **Apache Airflow**, installé via Docker.

---

## 🧰 Stack technique

| Outil         | Usage                                |
|---------------|--------------------------------------|
| Python        | Scripts d'extraction et traitement   |
| Apache Airflow| Orchestration du pipeline            |
| PostgreSQL    | Stockage relationnel des données     |
| Docker        | Conteneurisation de l’environnement  |

---

## 🧪 Résultat

Une fois lancé, le DAG dans Airflow permet de :

- Collecter automatiquement les données à intervalles réguliers
- Alimenter les trois couches de la base PostgreSQL
- Garder un historique exploitable pour une future modélisation BI ou analytique

