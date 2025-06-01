# backend/load_model.py

import pickle
import os

# Crop recommendation model
CROP_MODEL_PATH = os.path.join("models", "crop_recommendation_model.pkl")

def predict_crop(features: list):
    with open(CROP_MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    prediction = model.predict([features])
    return prediction[0]

# ✅ Yield prediction model (AdaBoost + TabNet)
YIELD_MODEL_PATH = os.path.join("models", "ada_best_yield_model.pkl")

def predict_yield(features: list):
    with open(YIELD_MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    prediction = model.predict([features])
    return prediction[0]
