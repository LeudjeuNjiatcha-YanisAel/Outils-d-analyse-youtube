📺 Analyse de vidéos et playlists YouTube avec Google Colab
🚀 Description

Ce projet permet de rechercher une vidéo YouTube ou une playlist, puis :

Afficher ses informations principales (titre, likes, vues).

Récupérer et nettoyer les meilleurs commentaires (avec expressions régulières).

Générer une analyse automatique des commentaires grâce à Google Gemini.

Si une playlist est trouvée : compter le nombre de vidéos, donner une recommandation et produire une analyse IA basée sur les titres des vidéos.

Le projet est conçu pour être exécuté facilement dans Google Colab.

🛠️ Technologies utilisées

Python 3

Google Colab (environnement d’exécution)

YouTube Data API v3 (via googleapiclient)

Google Generative AI (Gemini) (via google.genai)

Regex (re) pour nettoyer et améliorer les commentaires

📂 Fonctionnalités principales

🔎 Recherche de vidéo YouTube

Récupère l’ID, le titre, les vues et le nombre de likes.

Affiche l’URL de la vidéo.

💬 Commentaires YouTube

Récupère les 10 premiers commentaires.

Nettoie le texte avec des expressions régulières : suppression de liens, emails, emojis, répétitions abusives.

Affiche les meilleurs commentaires avec leurs likes.

Analyse les commentaires avec Gemini pour donner :

Pertinence de la vidéo.

Public cible.

Note sur 10.

Recommandation.

📂 Playlist YouTube

Recherche une playlist liée au même mot-clé.

Affiche le titre et l’URL de la playlist.

Compte le nombre de vidéos.

Donne une recommandation automatique (petite, moyenne ou grande playlist).

Analyse IA avec Gemini pour résumer et recommander la playlist.

⚙️ Installation et utilisation
1. Lancer sur Google Colab

Ouvrez Google Colab
.

Créez un nouveau notebook Python 3.

Collez le contenu du script dans une cellule.

2. Installer les dépendances

Exécutez dans une cellule Colab :

!pip install google-api-python-client google-genai

3. Ajouter vos clés API

Activez l’API YouTube Data v3 dans la Google Cloud Console.

Activez l’API Google Generative AI (Gemini) dans Google AI Studio.

Remplacez les clés API dans le script :

youtube_api = "VOTRE_CLE_YOUTUBE_API"
client = genai.Client(api_key="VOTRE_CLE_GEMINI_API")

4. Exécuter

Lancez la fonction principale :

main()


Entrez un mot-clé (par ex. Python) et laissez le script récupérer et analyser les données.

📊 Exemple d’exécution
Entrer le nom de la video youtube a rechercher : Python

🎬 Vidéo trouvée : Python Tutorial for Beginners
URL : https://www.youtube.com/watch?v=abcd1234
Likes : 15234 | Vues : 1 234 567

💬 10 commentaires récupérés :
- Great tutorial, very clear! (350 likes)
- Thanks a lot, this helped me! (120 likes)
...

🤖 Analyse IA (Gemini) :
1. La vidéo est pertinente pour les débutants.
2. Adaptée aux étudiants et développeurs juniors.
3. Note : 9/10
4. Je recommande cette vidéo car elle est claire et progressive.

✅ Améliorations prévues

Détection automatique du sentiment des commentaires (positif, négatif, spam).

Exportation des résultats en CSV / JSON.

Interface web interactive avec Streamlit ou Flask.

👨‍💻 Auteur

Projet développé pour l’apprentissage de :

APIs Google

Traitement de texte (Regex)

IA générative (Gemini)

Python sur Google Colab
