import os,re
from googleapiclient.discovery import build
from google import genai
from google.genai import types 

youtube_api = "AIzaSyCdMKKFAzmf3Y1aZ7yQw8FgXJC6uvDsJd8"

youtube = build("youtube","v3",developerKey=youtube_api)
# Permet de Creer un client pour l'API Youtube version 3

# Definition de nos fonctions
def search_video(name_video):
   requests = youtube.search().list(q = name_video,part="snippet",type="video",maxResults=2)
   # Ici on veut trouver l'ID d'une video via son nom
   response = requests.execute()
   # Ici on envoie une requete et on obtient une reponse
   
   if response["items"]:
       video = response["items"][0]["id"]["videoId"]
       # Ca recupere l'id de la video
       title = response["items"][0]["snippet"]["title"]
       stats = youtube.videos().list(part="statistics",id=video)
       stats_res = stats.execute()
       stats = stats_res["items"][0]["statistics"]
       like_count = stats.get("likeCount", "N/A")
       vues = stats.get("viewCount", "N/A")
       
       # recherche playlist
       req_playlist = youtube.search().list(q=name_video, part="snippet", type="playlist", maxResults=1)
       res_playlist = req_playlist.execute()
       playlist_id, playlist_title = (None, None)
       if res_playlist["items"]:
            playlist_id = res_playlist["items"][0]["id"]["playlistId"]
            playlist_title = res_playlist["items"][0]["snippet"]["title"]
       return (video,title,like_count,vues),(playlist_id,playlist_title)
   return None,None,None,None


# Pour recuperer le nombre de video d'une playlist
def info_playlist(playlist_id):
    request = youtube.playlistItems().list(part="snippet",playlistId=playlist_id,maxResults=50)
    
    response = request.execute()
    total_videos = response.get("pageInfo",{}).get("totalResults",0)
    return total_videos

# Code Pour Les Commentaires
def commentaries(video_id,max_results=10):
    comments = []
    requests = youtube.commentThreads().list(part = "snippet",videoId=video_id,textFormat="plainText",maxResults=max_results)
    # On a construit la requete pour recuperer les commentaires
    response = requests.execute()
    # Lancement de la requete
    for commentary in response["items"]:
        pet = commentary["snippet"]["topLevelComment"]["snippet"]
        #Ca va chercher le vrai commentaire
        text = pet["textDisplay"]
        #Recupere le texte du commentaire
        like = pet["likeCount"]
        comments.append((text,like))
    return comments



# Code Pour Analyser une Playlist
def analyse_playlist(playlist_id,playlist_title):
    videos = []
    req = youtube.playlistItems().list(part="snippet",playlistId=playlist_id,maxResults=20)
    res = req.execute()

    for item in res.get("items", []):
        title = item["snippet"]["title"]
        videos.append(title)

    if not videos:
        return "Impossible d’analyser : la playlist est vide."

    input_text = "\n".join([f"- {t}" for t in videos])

    prompt = f"""Voici les titres des vidéos de la playlist "{playlist_title}" :
    {input_text}
    Analyse cette playlist et réponds :
    1. Résume en quelques phrases ce que couvre cette playlist.
    2. Pour quel type de spectateurs est-elle adaptée ?
    3. Donne une note de pertinence /10.
    4. Dis si tu la recommanderais, et pourquoi.
    """

    client = genai.Client(api_key="AIzaSyAQBpi-rDqpY4rqSZbeFc0Szjg0dsCYixQ")
    model = "gemini-2.5-flash"

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)],
        )
    ]

    config = types.GenerateContentConfig(response_modalities=["TEXT"])

    output = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=config,
    ):
        if getattr(chunk, "text", None):
            output += chunk.text

    return output.strip()

# Code Recuperer Dans Google AI studio
def analyse_comments(comments):
    client = genai.Client(api_key=("AIzaSyAQBpi-rDqpY4rqSZbeFc0Szjg0dsCYixQ"))
    # Ici on prend les commentaires les plus likes
    input_text = "\n".join(
        [f"- {txt} ({likes} likes)" for txt,likes in sorted(comments,key=lambda x:x[1],reverse=True)[:5]]
    )

    prompt = f"""Voici des commentaires d'une vidéo récupérés sur YouTube : {input_text}
    Analyse ces commentaires et dit moi ci en 1 la video est pertinente , en 2 pour quelle type de spectatuers c'est reserver , en 3 tu donne une note /10 pour la pertinence , 
    en 4 tu donne une raison pour laquelle tu recommanderait cette video
    ."""

    model = "gemini-2.5-flash"

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)],
        )
    ]

    config = types.GenerateContentConfig(response_modalities=["TEXT"])

    output = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=config,
    ):
        if getattr(chunk, "text", None):
            output += chunk.text

    return output.strip()


# Ma fonction principale
def main():
    name = input("Entrer le nom de la video youtube a rechercher : ")
    (video_id,title,likes,vues),(playlist_id,playlist_title) = search_video(name)
    
    if not video_id :
        print("Video non trouver sur youtube")
        exit()
    
    if video_id:
        print(f"\n\tVideo trouvee : {title}")
        # Maintenez la touche controle puis utiliser la souris pour cliquez sur le lien
        print(f"lien : https://www.youtube.com/watch?v={video_id}")
        print(f"Nombres De Likes : {likes} | Vues : {vues} ")
        print("Analyses des commentaires des differentes video ...")
        comment = commentaries(video_id)
        print("Meilleur Commentaire Trouvee ")
        # Ici on affiche les meilleurs commentaires
        print(f"{len(comment)} commentaires recuperes.")
        for txt, likes in comment:
            print(f"- {txt} ({likes} likes)")
  
        recommandation = analyse_comments(comment)
        print("\n=== Video recommandee a partir des commentaires ===")
        print(recommandation)
    print("\n")
    if playlist_id :
        print(f"\n\t=== Meilleure Playlist Trouvée Pour {name} : {playlist_title} ===")
        print(f"-URL de la playlist : https://www.youtube.com/playlist?list={playlist_id}")
        total = info_playlist(playlist_id)
        print(f"Nombre De Video De La Playlist {total} videos")
        print("\n=== Recommandation de la Playlist ===")
        analyse = analyse_playlist(playlist_id, playlist_title)
        print(analyse)
    
main()