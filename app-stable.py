# Importez les modules nécessaires
import streamlit as st
import replicate
import random
import json
import requests

# Récupérez le modèle Stable-diffusion
model = replicate.models.get("stability-ai/stable-diffusion")

# Récupérez la version du modèle souhaitée
version = model.versions.get("6359a0cab3ca6e4d3320c33d79096161208e9024d174b2311e5a21b6c7e1131c")

# Définissez les paramètres du modèle par défaut
prompt = "an astronaut riding a horse on mars artstation, hd, dramatic lighting, detailed"
negative_prompt = ""
width = 512
height = 512
prompt_strength = 0.8
num_outputs = 1
num_inference_steps = 30
guidance_scale = 7.5
scheduler = "DDIM"
seed = None

# Créez une fonction pour exécuter le modèle avec les paramètres spécifiés
def generate_image(prompt, negative_prompt, width, height, prompt_strength, num_outputs, num_inference_steps, guidance_scale, scheduler, seed):
  output = version.predict(prompt=prompt, negative_prompt=negative_prompt, width=width, height=height, prompt_strength=prompt_strength,
                          num_outputs=num_outputs, num_inference_steps=num_inference_steps, guidance_scale=guidance_scale,
                          scheduler=scheduler, seed=seed)
  return output

# Créez un formulaire pour que l'utilisateur puisse entrer les paramètres du modèle
st.sidebar.header("Paramètres du modèle")
prompt = st.sidebar.text_input("Prompt", value=prompt)
negative_prompt = st.sidebar.text_input("Negative prompt", value=negative_prompt)
width = st.sidebar.number_input("Largeur de l'image", value=width, min_value=128, max_value=1024)
height = st.sidebar.number_input("Hauteur de l'image", value=height, min_value=128, max_value=1024)
prompt_strength = st.sidebar.number_input("Force du prompt", value=prompt_strength, min_value=0.0, max_value=1.0)
num_outputs = st.sidebar.number_input("Nombre d'images à générer", value=num_outputs, min_value=1, max_value=4)
num_inference_steps = st.sidebar.number_input("Nombre d'étapes de débruitage", value=num_inference_steps, min_value=1, max_value=10000)
guidance_scale = st.sidebar.number_input("Échelle de guidance", value=guidance_scale)
scheduler = st.sidebar.selectbox("Planificateur", ["DDIM", "K_EULER", "DPMSolverMultistep"], index=0)
seed = st.sidebar.number_input("Graine aléatoire", format="%.0f")

# Génère un nombre aléatoire entre 1 et 10000 et l'affecte à seed si l'utilisateur ne renseigne rien
if seed == 0:
  seed = random.randint(1, 10000)


# Ajoutez un bouton pour lancer la génération d'image
if st.sidebar.button("Générer l'image"):
  images = generate_image(prompt, negative_prompt, width, height, prompt_strength, num_outputs, num_inference_steps, guidance_scale, scheduler, seed)
  # Ajoutez un bouton de téléchargement pour chaque image
    # Ajoutez un bouton de téléchargement pour chaque image
    
    
  # Créez une grille de deux colonnes
col1, col2 = st.columns(2)

for i, image_url in enumerate(images):
  with col1 if i % 2 == 0 else col2:
    st.image(image_url, width=width, caption=f"Image {i+1}")
  image_response = requests.get(image_url)
  btn = st.download_button(
            label=f"Télécharger l'image {i+1}",
            data=image_response.content,  # Utilisez .content pour obtenir les données binaires de l'image
            file_name=f"image_{i+1}.png",
            mime="image/png"
            )
