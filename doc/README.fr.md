### Trailer Finder

### Description

Trailer Finder est un outil d'automatisation basé sur Python conçu pour rechercher et télécharger des bandes-annonces de films et de séries TV en utilisant les APIs de Radarr et Sonarr. Il interagit avec TMDB (The Movie Database) pour obtenir des informations sur les bandes-annonces et utilise yt-dlp pour les télécharger depuis YouTube. L'outil est configurable via un fichier YAML et prend en charge diverses options comme les mots-clés de recherche des bandes-annonces, la durée maximale des bandes-annonces et les paramètres de répertoire de sortie.

---

### Table des Matières

- [Trailer Finder](#trailer-finder)
- [Description](#description)
- [Table des Matières](#table-des-matières)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Configuration](#configuration)
- [Aperçu des Modules](#aperçu-des-modules)
  - [1. **Module Logger**](#1-module-logger)
  - [2. **Module Radarr**](#2-module-radarr)
  - [3. **Module Sonarr**](#3-module-sonarr)
  - [4. **Module Translator**](#4-module-translator)
  - [5. **Module Utils**](#5-module-utils)
- [Gestion des Erreurs](#gestion-des-erreurs)
- [Contributions](#contributions)
- [Docker](#docker)

---

### Installation

Pour exécuter Trailer Finder sans Docker, assurez-vous d'avoir les prérequis suivants installés sur votre système :

1. **Prérequis**:
   - Python 3.7 ou version ultérieure
   - `pip` (outil de gestion des paquets Python)
   - Clés d'API pour TMDB, Radarr et Sonarr

2. **Étapes d'Installation**:
   - Clonez le dépôt GitHub :
     ```bash
     git clone https://github.com/yourusername/trailer-finder.git
     cd trailer-finder
     ```

   - Installez les dépendances Python :
     ```bash
     pip install -r requirements.txt
     ```

3. **Configuration**:
   - Renommez le fichier `config.sample.yaml` en `config.yaml`.
   - Configurez les clés d'API pour TMDB, Radarr et Sonarr ainsi que d'autres paramètres nécessaires dans `config.yaml`.

---

### Utilisation

Pour exécuter Trailer Finder après l'installation et la configuration :

1. **Lancer l'outil**:
   ```bash
   python main.py
   ```

2. **Arrêter l'outil**:
   - Utilisez `Ctrl + C` dans la console pour arrêter l'exécution.

3. **Logs**:
   - Les logs sont affichés dans la console et peuvent être redirigés vers des fichiers de log si nécessaire.

---

### Configuration

La configuration de Trailer Finder est gérée à l'aide d'un fichier `config.yaml` situé dans le répertoire `config`. Voici un exemple de structure de fichier de configuration :

```yaml
# Configuration pour Sonarr
sonarr_host: "http://localhost:8989"
sonarr_api: "your_sonarr_api_key"

# Configuration pour Radarr
radarr_host: "http://localhost:7878"
radarr_api: "your_radarr_api_key"

# Clé API TMDB (The Movie Database)
tmdb_api: "your_tmdb_api_key"

# Répertoire de sortie pour les bandes-annonces
dir_backdrops: "backdrops"

# URL de base pour les liens YouTube
yt_link_base: "https://www.youtube.com/watch?v="

# Informations d'authentification YouTube (optionnelles)
auth_yt_user: "your_youtube_username"
auth_yt_pass: "your_youtube_password"

# Paramètres pour le téléchargement avec Youtube-DL
no_warnings: True
skip_intros: True
max_length: 200
thread_count: 4
buffer_size_ffmpeg: "1M"
filetype: "mkv"

# Temps de sommeil entre les exécutions en heures
sleep_time: 6

# Mots-clés de recherche YouTube pour les bandes-annonces
yt_search_keywords: "official trailer"

# Limiter le téléchargement à une bande-annonce par élément
only_one_trailer: True

# Espace disque libre minimum requis en Go
min_free_space_gb: 5

# Langue par défaut pour la traduction
default_locale: fr

# Langue par défaut pour les bandes-annonces
default_language_trailer: fr-FR

# Mode silencieux, supprime certains logs pour le processus yt_dlp et ffmpeg
quiet_mode: False
```

---

### Aperçu des Modules

#### 1. **Module Logger**

- Gère l'enregistrement des messages avec différents niveaux de gravité (info, succès, avertissement, erreur, débogage).
- Prise en charge du journal multilingue à l'aide de fichiers de traduction.
- Fournit une sortie colorée dans la console pour plus de clarté.

#### 2. **Module Radarr**

- Interagit avec l'API Radarr pour rechercher et télécharger des bandes-annonces de films.
- Vérifie l'existence de bandes-annonces et télécharge de nouvelles bandes-annonces en fonction des paramètres de configuration.
- Gère la gestion des répertoires et vérifie l'espace disponible avant de lancer les téléchargements.

#### 3. **Module Sonarr**

- Interagit avec l'API Sonarr pour rechercher et télécharger des bandes-annonces de séries TV.
- Gère le téléchargement de bandes-annonces au niveau des épisodes et assure un espace disque suffisant avant de lancer les téléchargements.

#### 4. **Module Translator**

- Fournit des fonctionnalités de traduction en utilisant des fichiers YAML stockés dans le répertoire `locales`.
- Prend en charge le formatage dynamique des messages en fonction des clés de traduction.

#### 5. **Module Utils**

- Contient des fonctions utilitaires pour diverses tâches telles que la vérification de l'espace disque, l'extraction des bandes-annonces depuis TMDB et le téléchargement des bandes-annonces à l'aide de yt-dlp.
- Intègre ffmpeg pour le post-traitement des bandes-annonces téléchargées et assure que les bandes-annonces respectent les critères de durée spécifiés.

---

### Gestion des Erreurs

- **Gestion des Exceptions**:
  - Capture les exceptions lors des interactions avec les API, les opérations de fichiers et l'exécution d'outils externes.
  - Enregistre les erreurs avec des messages d'erreur détaillés et des informations de contexte.

- **Journalisation**:
  - Enregistre les erreurs, avertissements et messages d'information pour assurer une visibilité sur le fonctionnement de l'outil et les problèmes rencontrés.

---

### Contributions

Les contributions sont les bienvenues ! Suivez ces étapes pour contribuer :

1. Forker le dépôt.
2. Créer une nouvelle branche (`git checkout -b feature/votre-feature`).
3. Commiter vos modifications (`git commit -am 'Ajouter une fonctionnalité'`).
4. Pousser la branche (`git push origin feature/votre-feature`).
5. Créer une nouvelle Pull Request.

---

### Docker

Utilisez Docker pour exécuter Trailer Finder de manière isolée :

1. **Utilisation avec Docker**

   Utilisez votre image Docker personnalisée `ldfe/trailer-finder:tagname` :

   ```bash
   docker pull ldfe/trailer-finder:tagname
   docker run -d --name trailer-finder-app ldfe/trailer-finder:tagname
   ```

2. **Utilisation avec Docker Compose**

   Utilisez Docker Compose pour gérer le déploiement de Trailer Finder avec les dépendances :

   Créez un fichier `docker-compose.yml` :

   ```yaml
   version: '3'
   services:
     trailer-finder:
       image: ldfe/trailer-finder:tagname
       container_name: trailer-finder-app
       restart: always
   ```

   Lancez le service avec Docker Compose :

   ```bash
   docker-compose up -d
   ```
