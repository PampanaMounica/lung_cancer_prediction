from flask import Flask, render_template, request
import numpy as np
import joblib

app = Flask(__name__)

# Load saved objects
model = joblib.load("lung_cancer_model.pkl")
scaler = joblib.load("scaler.pkl")
encoder = joblib.load("label_encoder.pkl")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    # Read input values
    gender = request.form["gender"]
    age = float(request.form["age"])
    smoking = float(request.form["smoking"])
    yellow_fingers = float(request.form["yellow_fingers"])
    anxiety = float(request.form["anxiety"])
    peer_pressure = float(request.form["peer_pressure"])
    chronic_disease = float(request.form["chronic_disease"])
    fatigue = float(request.form["fatigue"])
    allergy = float(request.form["allergy"])
    wheezing = float(request.form["wheezing"])
    alcohol = float(request.form["alcohol"])
    coughing = float(request.form["coughing"])
    shortness_of_breath = float(request.form["shortness_of_breath"])
    swallowing_difficulty = float(request.form["swallowing_difficulty"])
    chest_pain = float(request.form["chest_pain"])

    # Encode gender
    gender_encoded = encoder.transform([gender])[0]

    # Create input array
    input_data = np.array([[gender_encoded, age, smoking, yellow_fingers,
                            anxiety, peer_pressure, chronic_disease, fatigue,
                            allergy, wheezing, alcohol, coughing,
                            shortness_of_breath, swallowing_difficulty,
                            chest_pain]])

    # Scale input
    input_scaled = scaler.transform(input_data)

    # Prediction
    prediction = model.predict(input_scaled)[0]

    result = "LUNG CANCER DETECTED" if prediction == 1 else "NO LUNG CANCER"

    return render_template("index.html", prediction=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

