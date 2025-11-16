from flask import Flask, request, render_template, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = 'some_secret_key'  # Required for session management

# Load the knowledge base dynamically
KB_PATH = os.path.join(os.path.dirname(__file__), 'knowledge_base.json')
if os.path.exists(KB_PATH):
    with open(KB_PATH, 'r') as f:
        kb = json.load(f)
else:
    raise FileNotFoundError("Error: knowledge_base.json not found!")

def evaluate_symptoms(user_data):
    """
    Implements a forward chaining inference engine.
    Evaluates user symptoms against predefined rules and returns relevant diagnoses, advice, and home remedies.
    """
    recommendations = []
    for rule in kb.get("rules", []):
        if rule_matches(rule.get("conditions", []), user_data):
            recommendations.append({
                "diagnosis": rule.get("diagnosis", "Unknown"),
                "description": rule.get("description", ""),
                "advice": rule.get("advice", "Please consult a healthcare professional."),
                "home_remedies": rule.get("home_remedies", "No specific home remedy available.")
            })
    return recommendations

def rule_matches(conditions, user_data):
    """
    Checks if user-provided symptoms match a rule's conditions.
    Supports:
    - Simple condition checks (symptom presence)
    - Numeric conditions (e.g., minimum duration)
    - Conditions with required severity
    - Nested OR logic using 'any' key
    """
    for cond in conditions:
        if "any" in cond:
            if not any(rule_matches([subcond], user_data) for subcond in cond["any"]):
                return False
        else:
            symptom = cond.get("symptom")
            if symptom not in user_data:
                return False
            details = user_data[symptom]
            if "min_duration" in cond:
                try:
                    duration = int(details.get("duration", 0))
                except ValueError:
                    duration = 0
                if duration < cond["min_duration"]:
                    return False
            if "required_severity" in cond:
                if details.get("severity", "").lower() != cond["required_severity"].lower():
                    return False
    return True

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Home page - allows users to select symptoms.
    """
    if request.method == 'POST':
        selected_symptoms = request.form.getlist('symptoms')
        if not selected_symptoms:
            return render_template('index.html', symptoms=kb.get("symptoms", []), error="Please select at least one symptom.")
        session['selected_symptoms'] = selected_symptoms
        return redirect(url_for('details'))
    return render_template('index.html', symptoms=kb.get("symptoms", []))

@app.route('/details', methods=['GET', 'POST'])
def details():
    """
    Collects additional details (duration & severity) for selected symptoms.
    """
    selected_symptoms = session.get('selected_symptoms', [])
    if not selected_symptoms:
        return redirect(url_for('index'))

    if request.method == 'POST':
        user_data = {}
        for symptom in selected_symptoms:
            duration = request.form.get(f"{symptom}_duration", "0")
            severity = request.form.get(f"{symptom}_severity", "mild")
            user_data[symptom] = {"duration": duration, "severity": severity}
        session['user_data'] = user_data
        return redirect(url_for('result'))
    
    return render_template('details.html', symptoms=selected_symptoms)

@app.route('/result')
def result():
    """
    Processes user input and displays results.
    """
    user_data = session.get('user_data', {})
    recommendations = evaluate_symptoms(user_data)
    return render_template('result.html', user_data=user_data, recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=5000)
