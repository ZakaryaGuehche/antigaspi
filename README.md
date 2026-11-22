# AntiGaspi

Application anti-gaspillage alimentaire : les commerçants publient leurs paniers d'invendus à prix réduit, les utilisateurs les consultent et les réservent.

Projet du cours Conteneurisation et orchestration (ESILV).

## Architecture

- front : interface web en HTML/JavaScript servie par nginx
- api : API REST en Python (FastAPI)
- db : base de données PostgreSQL

## Lancer le projet en local

À venir (docker compose up)

## Déploiement Kubernetes

À venir (dossier deploy/)

## Organisation Git

- main : production (protégée)
- develop : branche de travail
- feature/* : une branche par fonctionnalité, mergée dans develop


## Utilisation de l'IA

Outil utilisé : Claude (Anthropic), comme aide pour la configuration Docker/Kubernetes et une partie du code. Tout a été relu, testé et adapté par moi.