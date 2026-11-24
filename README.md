# Student Management System — DevOps CI/CD Project

**Institution :** ISG Sousse — Département Informatique (3 LIG)  
**Année universitaire :** 2026–2027  
**Module :** Introduction au DevOps – Projet  

## 1. Présentation du Projet
Application web de gestion académique développée avec **Python (Flask)**, **Bootstrap 5** et **MySQL**, intégrée dans un workflow DevOps complet reposant sur **Git/GitHub**, **Jenkins** et **Docker**.

## 2. Architecture & Modules
- **Authentification & RBAC :** Connexion sécurisée (`admin` / `teacher`), hachage des mots de passe et gestion de session.
- **Dashboard :** Indicateurs clés (étudiants, enseignants, cours, inscriptions, moyenne générale et taux de réussite).
- **Gestion complète (CRUD) :** Étudiants, Enseignants, Cours, Inscriptions et Notes.
- **Endpoint de santé :** `GET /health` pour la supervision et les Smoke Tests CI/CD.

## 3. Workflow Git & Pipelines Jenkins
- `main` : Branche de production protégée.
- `dev` : Branche d'intégration continue.
- `feature/*` : Branches de développement fonctionnel.
- **Pipeline 1 (`jenkins/Jenkinsfile.pr`) :** Build & Smoke Test sur Pull Request vers `dev`.
- **Pipeline 2 (`jenkins/Jenkinsfile.dev`) :** Build complet avec parallélisation Python 3.11 / 3.12 sur push `dev`.
- **Pipeline 3 (`jenkins/Jenkinsfile.release`) :** Build versionné sur tag `vX.Y.Z` avec archivage des artefacts.