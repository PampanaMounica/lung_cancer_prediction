from flask import Flask, request, jsonify
import numpy as np
import joblib
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow React requests

# Load ML objects
model = joblib.load("lung_cancer_model.pkl")
scaler = joblib.load("scaler.pkl")
gender_encoder = joblib.load("gender_encoder.pkl")
target_encoder = joblib.load("target_encoder.pkl")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    try:
        gender = data["gender"]  # "M" or "F"
        age = float(data["age"])
        smoking = float(data["smoking"])
        yellow_fingers = float(data["yellow_fingers"])
        anxiety = float(data["anxiety"])
        peer_pressure = float(data["peer_pressure"])
        chronic_disease = float(data["chronic_disease"])
        fatigue = float(data["fatigue"])
        allergy = float(data["allergy"])
        wheezing = float(data["wheezing"])
        alcohol = float(data["alcohol"])
        coughing = float(data["coughing"])
        shortness_of_breath = float(data["shortness_of_breath"])
        swallowing_difficulty = float(data["swallowing_difficulty"])
        chest_pain = float(data["chest_pain"])

        gender_encoded = gender_encoder.transform([gender])[0]

        input_data = np.array([[
            gender_encoded, age, smoking, yellow_fingers,
            anxiety, peer_pressure, chronic_disease, fatigue,
            allergy, wheezing, alcohol, coughing,
            shortness_of_breath, swallowing_difficulty,
            chest_pain
        ]])

        input_scaled = scaler.transform(input_data)
        prediction = model.predict(input_scaled)[0]
        result = target_encoder.inverse_transform([prediction])[0]

        return jsonify({
            "prediction": result
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
