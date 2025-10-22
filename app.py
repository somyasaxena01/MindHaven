from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import numpy as np
import joblib

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# Load data from CSV
df = pd.read_csv("resources.csv")

# Load model and label binarizer 
model = joblib.load("model.pkl")
mlb = joblib.load("label_binarizer.pkl")

@app.route('/')
def home():
    return render_template('home.html') 

@app.route('/finder', methods=['GET', 'POST'])
def finder():
    category = request.args.get('category', '').strip().lower()
    region = request.args.get('region', '').strip().lower()
    searched = False
    results = df.copy()

    if category or region:
        searched = True
        if category:
            results = results[results['category'].str.lower().str.contains(category)]
        if region:
            results = results[results['region'].str.lower().str.contains(region)]
    
    return render_template(
        'finder.html',
        resources=results.to_dict(orient='records'),
        searched=searched
    )

@app.route('/finder/<disorder>')
def show_disorder(disorder):
    # Title colors for each disorder
    color_map = {
        "anxiety": "#007b8a",
        "depression": "#5e4b8b",
        "stress": "#f4a261",
        "burnout": "#e63946",
        "grief": "#6c757d",
        "self-esteem": "#f4a300",
        "ptsd": "#457b9d",
        "bipolar": "#e295b5",
        "ocd": "#00bcd4",
        "adhd": "#f9c74f",
        "eating-disorder": "#f06292",
        "addiction": "#4caf50",
        "loneliness": "#9e9e9e",
        "panic-attack": "#fb8500",
        "daydreaming": "#90caf9",
    }

    disorder_lower = disorder.lower()
    # Format disorder name for title 
    acronyms = {"ptsd", "adhd", "ocd"}
    if disorder_lower in acronyms:
        formatted_disorder =  disorder.replace("-", " ").upper()
    else:
        formatted_disorder = disorder.replace("-", " ").title()
    # Pass color if found, else fallback to black
    title_color = color_map.get(disorder.lower(), "#000000")
    image_filename = f"{disorder_lower}.svg"
    
    matched_resources = df[df['category'].str.lower().str.contains(disorder_lower)]
    
    return render_template(
        "issue_page.html",
        formatted_disorder=formatted_disorder,
        title_color=title_color,
        image = image_filename,
        resources= matched_resources.to_dict(orient='records'),
        issue=disorder_lower
    )

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

# Quiz answer mapping
answer_map = {'Never': 0, 'Rarely': 1, 'Sometimes': 2, 'Often': 3}

@app.route('/predict', methods=['POST'])
def predict():
    try:
        answers = [answer_map[request.form.get(f'Q{i+1}')] for i in range(20)]

        probs = []
        for clf in model.estimators_:
            proba = clf.predict_proba([answers])[0]
            probs.append(proba[1] if len(proba) > 1 else 0.0)

        threshold = 0.3
        predicted_indices = [i for i, prob in enumerate(probs) if prob >= threshold]
        predicted_labels = mlb.classes_[predicted_indices]

        # Store result in session for use in /quiz-result
        session['predicted_labels'] = list(predicted_labels)
        return redirect(url_for('quiz_result'))

    except Exception as e:
        return f"Error in prediction: {e}", 500

@app.route('/quiz-result')
def quiz_result():
    predicted_labels = session.pop('predicted_labels', [])

    if predicted_labels:
        feedback_message = (
            f"Our analysis suggests you might be experiencing symptoms of: "
            f"<strong>{', '.join(predicted_labels).title()}</strong>. Below are some resources you might find helpful."
        )
        matched_resources = df[df['category'].str.lower().isin([label.lower() for label in predicted_labels])]
        formatted_disorder = ", ".join(predicted_labels).title()
    else:
        feedback_message = (
            "Your responses don’t strongly indicate a specific issue. However, if you're feeling overwhelmed, "
            "please consider reaching out to a mental health professional or exploring the general support resources below."
        )
        matched_resources = df
        formatted_disorder = "No Major Issues Detected"

    return render_template(
        "issue_page.html",
        formatted_disorder=formatted_disorder,
        title_color="#2d5be3",
        resources=matched_resources.to_dict(orient="records"),
        issue="quiz-result",
        feedback_message=feedback_message
    )

if __name__ == '__main__':
    app.run()