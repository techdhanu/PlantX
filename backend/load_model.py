import pickle
import os

# Get absolute path to model
MODEL_PATH = os.path.join("models", "crop_recommendation_model.pkl")

def predict_crop(features: list):
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)

    prediction = model.predict([features])
    return prediction[0]
