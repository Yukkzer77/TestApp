# Importez les modules nécessaires
import streamlit as st
import replicate
import random
import json
import requests

# Récupérez le modèle Stable-diffusion
model = replicate.models.get("prompthero/openjourney")

# Récupérez la version du modèle souhaitée
version = model.versions.get("9936c2001faa2194a261c01381f90e65261879985476014a0a37a334593a05eb")

# Définissez les paramètres du modèle par défaut
prompt = "mdjrny-v4 style portrait of female elf, intricate, elegant, highly detailed, digital painting, artstation, concept art, smooth, sharp focus, illustration, art by artgerm and greg rutkowski and alphonse mucha, 8k"
width = 512
height = 512
num_outputs = 1
num_inference_steps = 50
guidance_scale = 7
seed = None

# Créez une fonction pour exécuter le modèle avec les paramètres spécifiés
def generate_image(prompt, width, height, num_outputs, num_inference_steps, guidance_scale, seed):
  output = version.predict(prompt=prompt, width=width, height=height, num_outputs=num_outputs, num_inference_steps=num_inference_steps, guidance_scale=guidance_scale, seed=seed)
  return output[0]

# Créez un formulaire pour que l'utilisateur puisse entrer les paramètres du modèle
st.sidebar.header("Paramètres du modèle")
prompt = st.sidebar.text_input("Prompt", value=prompt)
width = st.sidebar.number_input("Largeur de l'image", value=width, min_value=128, max_value=1024)
height = st.sidebar.number_input("Hauteur de l'image", value=height, min_value=128, max_value=1024)
num_outputs = st.sidebar.number_input("Nombre d'images à générer", value=num_outputs, min_value=1, max_value=4)
num_inference_steps = st.sidebar.number_input("Nombre d'étapes de débruitage", value=num_inference_steps, min_value=1, max_value=10000)
guidance_scale = st.sidebar.number_input("Échelle de guidance", value=guidance_scale)
seed = st.sidebar.number_input("Graine aléatoire", format="%.0f")

# Génère un nombre aléatoire entre 1 et 10000 et l'affecte à seed si l'utilisateur ne renseigne rien
if seed == 0:
  seed = random.randint(1, 10000)

# Ajoutez un bouton pour lancer la génération d'image
if st.sidebar.button("Générer l'image"):
  images = generate_image(prompt, width, height, num_outputs, num_inference_steps, guidance_scale, scheduler, seed)
  # Ajoutez un bouton de téléchargement pour chaque image
  # Ajoutez un bouton de téléchargement pour chaque image
  # Créez une grille de deux colonnes
  col1, col2 = st.columns(2)
  for i, image_url in enumerate(images):
    with col1 if i % 2 == 0 else col2:
      st.image(image_url, caption=f"Image {i+1}")
    image_response = requests.get(image_url)
    btn = st.download_button(
              label=f"Télécharger l'image {i+1}",
              data=image_response.content,  # Utilisez .content pour obtenir les données binaires de l'image
              file_name=f"image_{i+1}.png",
              mime="image/png"
              )
