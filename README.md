# 🌿 PlantGuard AI — Plant Disease Detector

A full-stack web application that uses a CNN model to detect plant diseases from leaf images.

![PlantGuard AI](https://img.shields.io/badge/Flask-3.0-green) ![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15-orange) ![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-blue)

---

## 📌 Project Description

PlantGuard AI allows farmers and gardeners to upload a photo of a plant leaf and instantly receive:
- **Disease name** detected by a CNN model
- **Confidence score** with an animated progress bar
- **Treatment tips** specific to the detected disease
- Support for **38 disease classes** across **14 plant species**

---

## 🛠️ Technologies Used

| Layer      | Technology                          |
|------------|-------------------------------------|
| Frontend   | HTML5, Bootstrap 5, CSS3            |
| Behavior   | JavaScript, jQuery                  |
| Backend    | Python, Flask, Jinja2               |
| ML Model   | TensorFlow, MobileNetV2, NumPy      |
| Image Proc | Pillow (PIL)                        |

---

## 📁 Project Structure

```
plant-disease-detector/
├── app.py                     ← Flask main file (3 routes)
├── requirements.txt
├── model/
│   └── plant_disease_model.h5 ← Pre-trained CNN model
├── static/
│   ├── css/
│   │   └── style.css          ← Custom styles + dark mode
│   ├── js/
│   │   └── main.js            ← jQuery logic + validations
│   └── uploads/               ← Uploaded leaf images
└── templates/
    ├── base.html              ← Jinja2 base layout
    ├── index.html             ← Home + upload page
    └── result.html            ← Results display page
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/plant-disease-detector.git
cd plant-disease-detector
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add the model file
Download the pre-trained model and place it at:
```
model/plant_disease_model.h5
```
Get the model from: https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset

### 4. Run the app
```bash
python app.py
```

### 5. Open in browser
```
http://localhost:5000
```

---

## 🌐 Flask Routes

| Route      | Method    | Description                        |
|------------|-----------|------------------------------------|
| `/`        | GET       | Home page with upload form         |
| `/submit`  | POST      | Receives image, runs prediction    |
| `/success` | GET       | Displays results with Jinja2 vars  |

---

## ✅ Features

- 📤 Drag & Drop or Browse file upload
- 🔍 CNN-powered disease detection (38 classes, 14 plants)
- 📊 Animated confidence progress bar
- 💊 Specific treatment tips per disease
- ✅ jQuery form validation (type, size, empty checks)
- 📱 Fully responsive Bootstrap layout
- 🔒 Secure file handling with Werkzeug

---


MIT License — free to use and modify.
