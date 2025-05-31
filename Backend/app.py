import pandas as pd
import random
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime

# File to log session data
log_file = "../data/results.csv"
os.makedirs(os.path.dirname(log_file), exist_ok=True)

if not os.path.exists(log_file):
    with open(log_file, "w", encoding="utf-8") as f:
        f.write("timestamp,stress_level,feedback,tip,category\n")

# Flask setup
app = Flask(__name__)
CORS(app)

# Loading categorized CSVs
exercises_df = pd.read_csv("../data/Categorized_CalmBot_Exercises.csv")
motivations_df = pd.read_csv("../data/Categorized_CalmBot_Motivational_Quotes.csv")

# Helper function to categorize stress
def get_stress_category(stress_level):
    stress = int(stress_level)
    if stress <= 3:
        return "Low"
    elif stress <= 6:
        return "Medium"
    else:
        return "High"

@app.route('/get_tip', methods=['POST'])
def get_tip():
    data = request.get_json()
    stress = data.get('stress')
    feedback = data.get('feedback', "")
    category = get_stress_category(stress)

    # Combining matching tips
    matching_exercises = exercises_df[exercises_df['StressLevelCategory'] == category]
    matching_motivation = motivations_df[motivations_df['StressLevelCategory'] == category]

    # Adding category column
    matching_exercises = matching_exercises[['Category', 'Description']].rename(columns={"Description": "Tip"})
    matching_motivation = matching_motivation[['Category', 'Message']].rename(columns={"Message": "Tip"})

    combined = pd.concat([matching_exercises, matching_motivation], ignore_index=True)

    # Picking random tip and category
    if combined.empty:
        selected_tip = "Take a breath. You're doing great just by showing up!"
        tip_category = "General"
    else:
        chosen = combined.sample(1).iloc[0]
        selected_tip = chosen['Tip']
        tip_category = chosen['Category']

    # Clean feedback for CSV
    clean_feedback = str(feedback).replace(",", ";").replace("\n", " ").strip()

    # Log to results file
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()},{stress},{clean_feedback},{selected_tip},{tip_category}\n")

    return jsonify({
        "tip": selected_tip,
        "category": tip_category
    })

@app.route('/end_session', methods=['POST'])
def end_session():
    data = request.get_json()
    stress = data.get('stress')
    post_stress = data.get('post_stress')
    feedback = data.get('feedback', "")
    clean_feedback = str(feedback).replace(",", ";").replace("\n", " ").strip()

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()},{stress},{post_stress},{clean_feedback},(Session ended)\n")

    return jsonify({"message": "Thanks for your feedback!"})


if __name__ == '__main__':
    app.run(debug=True)
