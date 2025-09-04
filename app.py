from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory, render_template
from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel
import io
import os
from werkzeug.utils import secure_filename
TEMPLATES_AUTO_RELOAD = True

app = Flask(__name__)

device = "cuda" if torch.cuda.is_available() else "cpu"
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

character_db = {}
character_names = []
character_images = []
current_name = ''
current_images = []

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
#app.config['UPLOAD_FOLDER'] = os.path.join('static', 'characters')
#os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route("/")
def index():
    names = character_names
    return render_template('index.html', names=names)

@app.route("/", methods=["POST"])
def saveCharacter():
    character_names.append(current_name)
    character_images.append(current_images)
    names = character_names
    return render_template('index.html', names=names)

@app.route("/character_page", methods=["POST"])
def character_page():
    n = request.form.get('characterSelect')
    character_index = character_names.index(n)
    return render_template('page.html', images=character_images[character_index], name=character_names[character_index])

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
    path = os.path.join('static', 'characters', name)
    if not name or not files:
        return "Name and images required", 400
    
    if name in character_names:
        path = os.path.join('static', 'characters', name)
        return "Character already added", 400
    else:
        path = os.path.join('static', 'characters', name)
        os.mkdir(path, mode = 0o777)

    embeddings = [get_embedding(f.read()) for f in files]
    avg_embedding = torch.mean(torch.stack(embeddings), dim=0)
    character_db[name] = avg_embedding
    global current_name
    current_name = name
    global current_images
    current_images = files

    for file in files:
        imageObject = Image.open(file)
        savePath = os.path.join(path, file.filename)
        imageObject.save(savePath)

    return f"Character '{name}' uploaded with {len(files)} images!"

@app.route("/recognize", methods=["POST"])
def recognizeCharacter():
    if not character_db:
        return jsonify({"name": None, "score": 0})

    file = request.files["image"]
    test_emb = get_embedding(file.read())

    best_name = None
    best_score = -1
    for name, emb in character_db.items():
        score = torch.nn.functional.cosine_similarity(test_emb, emb).item()
        if score > best_score:
            best_score = score
            best_name = name

    character_index = character_names.index(best_name)
    character_images[character_index].append(file)


    return jsonify({"name": best_name, "score": best_score})

if __name__ == "__main__":
    app.run(debug=True)
