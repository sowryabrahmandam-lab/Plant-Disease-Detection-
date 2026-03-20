"""
PlantGuard AI — app.py
Flask Backend with 3 routes: /, /submit, /success
"""

from flask import Flask, request, render_template, redirect, url_for, flash
import numpy as np
from PIL import Image
import os
os.environ['TF_USE_LEGACY_KERAS'] = '1'
import tensorflow as tf

app = Flask(__name__)
app.secret_key = 'plantguard-secret-key-2024'   # needed for flash messages

# ── Config ──────────────────────────────────────────
UPLOAD_FOLDER  = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024   # 10MB max upload

# ── Load Model ───────────────────────────────────────
MODEL_PATH = os.path.join('model', 'plant_disease_model.h5')

try:
    model = tf.keras.models.load_model(MODEL_PATH)
    print("✅ Model loaded successfully.")
except Exception as e:
    model = None
    print(f"⚠️  Model not found at {MODEL_PATH}. Running in demo mode.\n   Error: {e}")


# ── Class Names (PlantVillage — 38 classes) ──────────
CLASS_NAMES = [
    'Apple___Apple_scab',
    'Apple___Black_rot',
    'Apple___Cedar_apple_rust',
    'Apple___healthy',
    'Blueberry___healthy',
    'Cherry_(including_sour)___Powdery_mildew',
    'Cherry_(including_sour)___healthy',
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
    'Corn_(maize)___Common_rust_',
    'Corn_(maize)___Northern_Leaf_Blight',
    'Corn_(maize)___healthy',
    'Grape___Black_rot',
    'Grape___Esca_(Black_Measles)',
    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
    'Grape___healthy',
    'Orange___Haunglongbing_(Citrus_greening)',
    'Peach___Bacterial_spot',
    'Peach___healthy',
    'Pepper,_bell___Bacterial_spot',
    'Pepper,_bell___healthy',
    'Potato___Early_blight',
    'Potato___Late_blight',
    'Potato___healthy',
    'Raspberry___healthy',
    'Soybean___healthy',
    'Squash___Powdery_mildew',
    'Strawberry___Leaf_scorch',
    'Strawberry___healthy',
    'Tomato___Bacterial_spot',
    'Tomato___Early_blight',
    'Tomato___Late_blight',
    'Tomato___Leaf_Mold',
    'Tomato___Septoria_leaf_spot',
    'Tomato___Spider_mites Two-spotted_spider_mite',
    'Tomato___Target_Spot',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
    'Tomato___Tomato_mosaic_virus',
    'Tomato___healthy',
]

# ── Treatment Tips Dictionary ─────────────────────────
TREATMENTS = {
    'Apple___Apple_scab':
        'Apply fungicides such as Captan or Mancozeb at 7–10 day intervals. Remove and destroy all fallen infected leaves. Prune trees to improve air circulation.',
    'Apple___Black_rot':
        'Prune and destroy infected branches. Apply copper-based fungicide in early spring. Avoid wounding the bark and remove mummified fruits.',
    'Apple___Cedar_apple_rust':
        'Apply myclobutanil fungicide before and during wet spring weather. Remove nearby juniper/cedar trees if possible.',
    'Apple___healthy':
        'Your apple plant looks healthy! Maintain regular watering, balanced fertilization, and inspect leaves weekly for early signs of disease.',
    'Blueberry___healthy':
        'Great news — your blueberry plant is healthy! Water consistently and apply acidic fertilizer to maintain soil pH between 4.5–5.5.',
    'Cherry_(including_sour)___Powdery_mildew':
        'Apply sulfur-based fungicide or potassium bicarbonate. Improve air circulation by pruning. Avoid overhead irrigation.',
    'Cherry_(including_sour)___healthy':
        'Your cherry plant is healthy! Ensure proper spacing, regular pruning, and monitor for pests during flowering season.',
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot':
        'Apply fungicides containing azoxystrobin or pyraclostrobin. Use resistant corn hybrids and practice crop rotation.',
    'Corn_(maize)___Common_rust_':
        'Apply foliar fungicides with triazoles or strobilurins. Plant rust-resistant hybrid varieties for future seasons.',
    'Corn_(maize)___Northern_Leaf_Blight':
        'Apply propiconazole fungicide at early disease stages. Use blight-resistant hybrids and practice crop rotation.',
    'Corn_(maize)___healthy':
        'Your corn is healthy! Maintain consistent watering, side-dress with nitrogen fertilizer, and monitor for pests.',
    'Grape___Black_rot':
        'Apply captan, myclobutanil, or mancozeb fungicide. Remove infected berries and mummified fruit. Prune for better airflow.',
    'Grape___Esca_(Black_Measles)':
        'No complete cure exists. Remove affected wood by pruning. Apply wound sealants. Avoid water stress and overloading the vine.',
    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)':
        'Apply copper-based fungicides. Improve vine canopy management for better air circulation. Destroy infected leaf debris.',
    'Grape___healthy':
        'Your grapevine is healthy! Maintain proper trellising, regular pruning, and monitor irrigation levels.',
    'Orange___Haunglongbing_(Citrus_greening)':
        'No cure is available. Remove and destroy infected trees immediately to prevent spread. Control psyllid insects with insecticides. Plant certified disease-free saplings.',
    'Peach___Bacterial_spot':
        'Apply copper-based bactericides early in the season. Select resistant varieties for new plantings. Avoid overhead irrigation.',
    'Peach___healthy':
        'Your peach tree is healthy! Thin fruits to improve size, water deeply but infrequently, and apply dormant spray in winter.',
    'Pepper,_bell___Bacterial_spot':
        'Apply copper-based bactericide. Remove infected leaves. Avoid overhead watering and rotate crops annually.',
    'Pepper,_bell___healthy':
        'Your pepper plant is healthy! Ensure full sunlight, consistent moisture, and stake plants to support heavy fruit loads.',
    'Potato___Early_blight':
        'Apply mancozeb or chlorothalonil fungicide every 7–10 days. Remove infected leaves. Practice crop rotation and avoid overhead irrigation.',
    'Potato___Late_blight':
        'Apply metalaxyl or cymoxanil fungicide immediately. Remove and destroy all infected plant material. Avoid waterlogging and practice strict crop rotation.',
    'Potato___healthy':
        'Your potato plant is healthy! Hill up soil around stems, maintain even moisture, and monitor for Colorado potato beetles.',
    'Raspberry___healthy':
        'Your raspberry canes are healthy! Prune old canes after fruiting, mulch generously, and fertilize in early spring.',
    'Soybean___healthy':
        'Your soybean crop is healthy! Maintain proper row spacing, monitor for aphids, and ensure adequate phosphorus and potassium levels.',
    'Squash___Powdery_mildew':
        'Apply neem oil, potassium bicarbonate, or sulfur-based fungicide. Remove heavily infected leaves. Improve air circulation between plants.',
    'Strawberry___Leaf_scorch':
        'Apply captan or myclobutanil fungicide. Remove infected leaves. Avoid overhead irrigation and ensure good soil drainage.',
    'Strawberry___healthy':
        'Your strawberry plant is healthy! Remove runners, refresh mulch annually, and renovate beds after harvest.',
    'Tomato___Bacterial_spot':
        'Apply copper-based bactericide. Remove infected plants. Use disease-free seeds and avoid working in the garden when plants are wet.',
    'Tomato___Early_blight':
        'Apply azoxystrobin or chlorothalonil fungicide. Remove lower infected leaves. Mulch around the base and ensure proper plant spacing.',
    'Tomato___Late_blight':
        'Apply chlorothalonil fungicide immediately. Remove and destroy all infected plants. Avoid overhead watering and improve drainage.',
    'Tomato___Leaf_Mold':
        'Apply copper-based fungicide. Improve greenhouse ventilation if applicable. Remove infected leaves and water at the base only.',
    'Tomato___Septoria_leaf_spot':
        'Apply mancozeb or copper fungicide every 7–10 days. Remove infected lower leaves. Avoid wetting foliage during irrigation.',
    'Tomato___Spider_mites Two-spotted_spider_mite':
        'Apply miticide or insecticidal soap. Spray water on undersides of leaves to dislodge mites. Introduce predatory mites as biological control.',
    'Tomato___Target_Spot':
        'Apply fungicides containing chlorothalonil or azoxystrobin. Remove infected leaves. Ensure proper spacing and airflow.',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus':
        'No cure available. Remove infected plants to prevent spread. Control whitefly populations with yellow sticky traps and insecticides. Use resistant varieties.',
    'Tomato___Tomato_mosaic_virus':
        'No chemical cure. Remove and destroy infected plants. Disinfect tools with bleach solution. Wash hands before handling plants. Use virus-resistant varieties.',
    'Tomato___healthy':
        'Your tomato plant is healthy! Water deeply 2–3 times per week, stake or cage plants, and pinch suckers for better yield.',
}

DEFAULT_TREATMENT = (
    'Consult a certified agronomist for accurate diagnosis. '
    'As a general precaution: remove infected plant parts, avoid overhead watering, '
    'ensure proper air circulation, and consider applying a broad-spectrum fungicide.'
)


# ── Helper Functions ──────────────────────────────────
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def preprocess_image(path):
    """Load image, resize to 224x224, normalize to [0,1], add batch dim."""
    img   = Image.open(path).convert('RGB').resize((224, 224))
    arr   = np.array(img, dtype=np.float32) / 255.0
    return np.expand_dims(arr, axis=0)


def format_label(raw_label):
    """
    Convert 'Tomato___Late_blight' → ('Tomato', 'Late blight')
    """
    parts   = raw_label.split('___')
    plant   = parts[0].replace('_', ' ').replace(',', '')
    disease = parts[1].replace('_', ' ') if len(parts) > 1 else 'Unknown'
    return plant, disease


# ── Route 1: Home Page (/') ───────────────────────────
@app.route('/')
def index():
    return render_template('index.html')


# ── Route 2: Form Submission ('/submit') ──────────────
@app.route('/submit', methods=['POST'])
def submit():

    # ── Validation 1: File present? ──
    if 'file' not in request.files:
        flash('No file part in the request.', 'error')
        return render_template('index.html', error='No file uploaded. Please select a leaf image.')

    file = request.files['file']

    # ── Validation 2: File selected? ──
    if file.filename == '':
        return render_template('index.html', error='No file selected. Please choose an image.')

    # ── Validation 3: Allowed extension? ──
    if not allowed_file(file.filename):
        return render_template('index.html', error='Invalid file type. Please upload JPG, PNG, or WEBP.')

    # ── Save file ──
    from werkzeug.utils import secure_filename
    import time
    # Add timestamp to avoid filename collisions
    timestamp    = str(int(time.time()))
    safe_name    = secure_filename(file.filename)
    final_name   = f"{timestamp}_{safe_name}"
    filepath     = os.path.join(app.config['UPLOAD_FOLDER'], final_name)
    file.save(filepath)

    # ── Model not loaded → demo mode ──
    if model is None:
        plant, disease = 'Tomato', 'Late blight'
        confidence     = 92.5
        is_healthy     = False
        treatment      = TREATMENTS.get('Tomato___Late_blight', DEFAULT_TREATMENT)
        flash('⚠️ Running in demo mode — model file not found.', 'warning')
    else:
        # ── Predict ──
        img_array   = preprocess_image(filepath)
        predictions = model.predict(img_array)
        confidence  = round(float(np.max(predictions)) * 100, 2)
        label       = CLASS_NAMES[int(np.argmax(predictions))]
        plant, disease = format_label(label)
        is_healthy  = disease.lower() == 'healthy'
        treatment   = TREATMENTS.get(label, DEFAULT_TREATMENT)

    # ── Route 3 redirect with results ──
    return redirect(url_for(
        'success',
        plant      = plant,
        disease    = disease,
        confidence = confidence,
        is_healthy = is_healthy,
        img        = final_name if model is None else final_name,
        treatment  = treatment
    ))


# ── Route 3: Show Results ('/success') ────────────────
@app.route('/success')
def success():
    # Retrieve from query params (passed via redirect)
    plant      = request.args.get('plant', 'Unknown')
    disease    = request.args.get('disease', 'Unknown')
    confidence = request.args.get('confidence', '0')
    is_healthy = request.args.get('is_healthy', 'False') == 'True'
    img        = request.args.get('img', '')
    treatment  = request.args.get('treatment', DEFAULT_TREATMENT)

    return render_template(
        'result.html',
        plant      = plant,
        disease    = disease,
        confidence = confidence,
        is_healthy = is_healthy,
        img        = img,
        treatment  = treatment
    )


# ── Run App ───────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True)
