# Health Symptom Checker Documentation

## 1. System Overview
The Health Symptom Checker is a web application built using the Flask framework. It allows users to select symptoms, provide additional details (duration and severity), and receive potential diagnoses and recommendations based on predefined rules.

## 2. Architecture
- **Framework**: The application is built using Flask, a lightweight web framework for Python.
- **Routing**: The application has three main routes:
  - `/`: Home page for symptom selection.
  - `/details`: Page for entering additional details about selected symptoms.
  - `/result`: Page displaying the diagnosis results.
- **Session Management**: User sessions are managed to store selected symptoms and user input.

## 3. User Interface
- **index.html**: 
  - Allows users to select symptoms using checkboxes.
  - Displays an error message if no symptoms are selected.
  
- **details.html**: 
  - Prompts users to provide the duration and severity for each selected symptom.
  - Includes form validation to ensure all fields are filled.

- **result.html**: 
  - Displays the user's reported symptoms along with their duration and severity.
  - Lists potential conditions and recommendations based on the evaluated symptoms.

## 4. Knowledge Base
The knowledge base is stored in `knowledge_base.json`, which includes:
- **Symptoms**: A list of recognized symptoms.
- **Rules**: Conditions for diagnosis, including symptoms, required attributes (like duration or severity), and associated recommendations.

## 5. Functionality
- **evaluate_symptoms(user_data)**: Evaluates user symptoms against predefined rules and returns relevant diagnoses, advice, and home remedies.
- **rule_matches(conditions, user_data)**: Checks if user-provided symptoms match a rule's conditions, supporting various checks (e.g., duration, severity).

## 6. Usage Instructions
1. Navigate to the home page to select symptoms.
2. Provide additional details for the selected symptoms.
3. View the diagnosis results and recommendations.

## 7. How to Run the System
To run the Health Symptom Checker system, follow these steps:
1. Ensure you have Python installed on your machine.
2. Install the required dependencies by running:
   ```
   pip install Flask
   ```
3. Run the application using the command:
   ```
   python app.py
   ```
4. Open your web browser and go to `http://127.0.0.1:5000` to access the application.
