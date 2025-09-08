from pathlib import Path
from flask import Flask, request, jsonify, render_template, url_for
from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel
import io
import os
TEMPLATES_AUTO_RELOAD = True

app = Flask(__name__)

device = "cuda" if torch.cuda.is_available() else "cpu"
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

character_db = {}
character_path = os.path.join('static', 'characters')

THRESHOLD = 0.75

ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"}

@app.route("/")
def index():
    names = os.listdir(character_path)
    return render_template('index.html', names=names)

@app.route("/character_page", methods=["POST"])
def character_page():
    name = request.form.get('characterSelect')
    image_folder = os.path.join('static', 'characters', name)
    image_filenames = os.listdir(image_folder)
    image_urls = []
    for filename in image_filenames:
        path = os.path.join('characters', name, filename)
        path = path.replace("\\", "/")
        image_urls.append(url_for('static', filename=path))
    return render_template('page.html', image_urls=image_urls, name = name)

#Extract CLIP embedding
def get_embedding(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    inputs = processor(images=image, return_tensors="pt").to(device)
    with torch.no_grad():
        image_emb = model.get_image_features(**inputs)
    image_emb = image_emb / image_emb.norm(dim=-1, keepdim=True)
    return image_emb.cpu()

@app.route("/upload", methods=["POST"])
def uploadCharacter():
    name = request.form.get("name")
    files = request.files.getlist("images")
    for file in files:
        if not allowed_files(file.filename):
            return "Only images allowed", 400
    path = os.path.join('static', 'characters', name)
    character_names = os.listdir(character_path)
    if not name or not files:
        return "Name and images required", 400
    
    if name in character_names:
        path = os.path.join('static', 'characters', name)
        for file in files:
            imageObject = Image.open(file)
            savePath = os.path.join(path, file.filename)
            imageObject.save(savePath)
        return "Character added to existing list", 400
    else:
        path = os.path.join('static', 'characters', name)
        os.mkdir(path, mode = 0o777)
        character_names.append(name)

    embeddings = [get_embedding(f.read()) for f in files]
    avg_embedding = torch.mean(torch.stack(embeddings), dim=0)
    character_db[name] = avg_embedding

    for file in files:
        imageObject = Image.open(file)
        savePath = os.path.join(path, file.filename)
        imageObject.save(savePath)

    return f"Character '{name}' uploaded with {len(files)} images!"

def recognizeCharacter(file):
    if not character_db:
        return jsonify({"name": None, "score": 0})

    test_emb = get_embedding(file.read())

    best_name = None
    best_score = -1
    for name, emb in character_db.items():
        score = torch.nn.functional.cosine_similarity(test_emb, emb).item()
        if score > best_score:
            best_score = score
            best_name = name

    if best_score > THRESHOLD:
        path = os.path.join('static', 'characters', best_name)
        imageObject = Image.open(file)
        filename = os.path.basename(file.filename)
        savePath = os.path.join(path, filename)
        imageObject.save(savePath)

@app.route("/recognize", methods=["POST"])
def recognize():
    files = request.files.getlist("images")
    for file in files:
        if not allowed_files(file.filename):
            return "Only images allowed", 400
    for file in files:
        recognizeCharacter(file)
    
    return f"All characters recognized and sorted"

def allowed_files(filename):
    isImage = False
    for i in ALLOWED_EXTENSIONS:
        if i in filename:
            isImage = True
    return isImage
    

if __name__ == "__main__":
    app.run(debug=True)
