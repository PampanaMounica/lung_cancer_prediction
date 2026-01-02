import React, { useState } from "react";
import { predictCancer } from "./api";
import "./App.css";

function App() {
  const [formData, setFormData] = useState({
    gender: "M",
    age: "",
    smoking: 0,
    yellow_fingers: 0,
    anxiety: 0,
    peer_pressure: 0,
    chronic_disease: 0,
    fatigue: 0,
    allergy: 0,
    wheezing: 0,
    alcohol: 0,
    coughing: 0,
    shortness_of_breath: 0,
    swallowing_difficulty: 0,
    chest_pain: 0,
  });

  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult("");

    try {
      const res = await predictCancer(formData);
      setResult(res.data.prediction);
    } catch {
      setResult("ERROR");
    }
    setLoading(false);
  };

  const yesNoField = (name, label) => (
    <div className="field">
      <label>{label}</label>
      <select name={name} onChange={handleChange}>
        <option value={0}>No</option>
        <option value={1}>Yes</option>
      </select>
    </div>
  );

  return (
    <div className="container">
      <h1>Lung Cancer Prediction System</h1>
      <p className="subtitle">
        AI-based medical decision support (educational purpose)
      </p>

      <form onSubmit={handleSubmit}>
        <div className="grid">
          <div className="field">
            <label>Gender</label>
            <select name="gender" onChange={handleChange}>
              <option value="M">Male</option>
              <option value="F">Female</option>
            </select>
          </div>

          <div className="field">
            <label>Age</label>
            <input
              type="number"
              name="age"
              required
              onChange={handleChange}
            />
          </div>

          {yesNoField("smoking", "Smoking")}
          {yesNoField("yellow_fingers", "Yellow Fingers")}
          {yesNoField("anxiety", "Anxiety")}
          {yesNoField("peer_pressure", "Peer Pressure")}
          {yesNoField("chronic_disease", "Chronic Disease")}
          {yesNoField("fatigue", "Fatigue")}
          {yesNoField("allergy", "Allergy")}
          {yesNoField("wheezing", "Wheezing")}
          {yesNoField("alcohol", "Alcohol Consumption")}
          {yesNoField("coughing", "Coughing")}
          {yesNoField("shortness_of_breath", "Shortness of Breath")}
          {yesNoField("swallowing_difficulty", "Swallowing Difficulty")}
          {yesNoField("chest_pain", "Chest Pain")}
        </div>

        <button type="submit">Predict Result</button>
      </form>

      {loading && <div className="loading">Analyzing data...</div>}

      {result && !loading && (
        <div
          className={`result ${
            result === "YES" ? "red" : "green"
          }`}
        >
          {result === "YES"
            ? "⚠️ High Risk of Lung Cancer Detected"
            : "✅ No Lung Cancer Detected"}
        </div>
      )}
    </div>
  );
}

export default App;
