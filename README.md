# Cloud_project_montaudran_meteo

🌦️ Pipeline de Données Météo – Architecture Serverless AWS (Quasi Temps Réel)

Présentation du projet

Ce projet met en place un pipeline de données pour la station météo du quartier Montaudran en quasi temps réel sur AWS.

L’objectif est de :

- Collecter les données de la station météo de montaudran via une API

- Stocker les données brutes dans Amazon S3

- Traiter et transformer les données

- Stocker les données transformées dans S3

- Cataloguer les données avec AWS Glue

- Interroger les données via Amazon Athena (SQL)

L’architecture est entièrement serverless, scalable et orientée événements.
