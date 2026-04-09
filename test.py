import replicate
import requests
import jwt
import time
from dotenv import load_dotenv
import os
import base64

load_dotenv()

# Étape 1 — Générer l'image avec Flux Dev
print("Génération de l'image...")
output = replicate.run(
    "black-forest-labs/flux-dev",
    input={"prompt": "A professional advertising photo of a perfume bottle on a luxury marble table, cinematic lighting, ultra realistic"}
)

for url in output:
    image_url = str(url)
    image_data = requests.get(image_url).content
    with open("output.jpg", "wb") as f:
        f.write(image_data)
    print("Image générée ✅")

# Étape 2 — Générer le token JWT pour Kling
access_key = os.getenv("KLING_ACCESS_KEY")
secret_key = os.getenv("KLING_SECRET_KEY")

token = jwt.encode(
    {"iss": access_key, "exp": int(time.time()) + 1800, "nbf": int(time.time()) - 5},
    secret_key, algorithm="HS256"
)

# Étape 3 — Envoyer l'image à Kling 3.0
print("Animation avec Kling 3.0...")
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

with open("output.jpg", "rb") as f:
    image_b64 = base64.b64encode(f.read()).decode()

response = requests.post(
    "https://api.klingai.com/v1/videos/image2video",
    headers=headers,
    json={
        "model_name": "kling-v3",
        "image": image_b64,
        "prompt": "The perfume bottle glows softly, luxury cinematic camera move",
        "duration": "5",
        "mode": "pro"
    }
)

task = response.json()
print("Réponse Kling:", task)
task_id = task["data"]["task_id"]
print(f"Tâche créée : {task_id}")

# Étape 4 — Attendre le résultat
print("En attente du rendu...")
while True:
    status = requests.get(
        f"https://api.klingai.com/v1/videos/image2video/{task_id}",
        headers=headers
    ).json()
    
    if status["data"]["task_status"] == "succeed":
        video_url = status["data"]["task_result"]["videos"][0]["url"]
        video_data = requests.get(video_url).content
        with open("output.mp4", "wb") as f:
            f.write(video_data)
        print("Vidéo sauvegardée : output.mp4 ✅")
        break
    elif status["data"]["task_status"] == "failed":
        print("Erreur Kling")
        break
    else:
        print("Rendu en cours...")
        time.sleep(10)