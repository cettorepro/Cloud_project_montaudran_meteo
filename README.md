# Cloud_project_montaudran_meteo

🌦️ Pipeline de Données Météo – Architecture Serverless AWS (Quasi Temps Réel)

Présentation du projet

Ce projet met en place un pipeline de données pour la station météo du quartier Montaudran en quasi temps réel sur AWS.

L’objectif est de :

- Collecter les données de la station météo de montaudran via une API

- Stocker les données brutes dans Amazon S3

- Traiter et transformer les données

- Stocker les données transformées dans S3

- Définir le schéma des données  avec AWS Glue Crawler

- Interroger les données via Amazon Athena (SQL)

- Présenter les KPI sur un tableau de bord déployé sur instance EC2 Ubuntu

- Automatisation du déploiement du pipeline grâce à AWS Cloudformation (Iac)

L’architecture est entièrement serverless, scalable et orientée événements.

Services AWS utilisés : 

- AWS Lambda – Fonction Python pour appeler l’API météo

- Amazon EventBridge – Planification automatique (toutes les 15 minutes)

- Amazon S3 – Stockage des données brutes et transformées

- AWS Glue – Détection automatique du schéma

- Amazon Athena – Requêtes SQL directement sur S3

- AWS CloudFormation - Déploiement automatisé des ressources (Iac)

<img width="1684" height="944" alt="Capture d&#39;écran 2026-02-13 085812" src="https://github.com/user-attachments/assets/2e463f6a-eeec-40be-b2ec-e7c9aba72bc0" />

Compétences mises en œuvre durant ce projet : 

- Architecture serverless

- Data Lake sur AWS

- Pipeline de données

- Event-driven architecture

- Requêtage SQL sur S3

