from flask import Flask, render_template, request
import math
from owlready2 import *

# Initialize Flask app
app = Flask(__name__)

# Load the ontology from the OWL file
onto = get_ontology("shapes.owl").load()

# Manually define descriptions and area formulas for shapes
shape_descriptions = {
    "Triangle": "A triangle has three sides. Its area is calculated as 0.5 × base × height.",
    "Rectangle": "A rectangle has four sides with opposite sides equal. Its area is length × width.",
    "Circle": "A circle is a round shape. Its area is π × radius².",
    "Square": "A square has four equal sides. Its area is side²."
}

shape_area_formulas = {
    "Triangle": "0.5 * base * height",
    "Rectangle": "length * width",
    "Circle": "π * radius²",
    "Square": "side²"
}

# Function to get shape description from the dictionary
def get_shape_description(shape):
    return shape_descriptions.get(shape, "No description available.")

# Function to get area formula for shape from the dictionary
def get_area_formula(shape):
    return shape_area_formulas.get(shape, "No formula available.")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/learn_geometry')
def learn_geometry():
    return render_template('learn_geometry.html')

@app.route('/learn_about_shape/<shape>')
def learn_about_shape(shape):
    try:
        description = get_shape_description(shape)
        area_formula = get_area_formula(shape)
    except Exception as e:
        description = "Information not available."
        area_formula = "No formula available."
    
    return render_template('learn_about_shape.html', shape=shape, description=description, area_formula=area_formula)

@app.route('/area_calculation/<shape>', methods=['GET', 'POST'])
def area_calculation(shape):
    area = None
    steps = ""
    if request.method == 'POST':
        if shape == 'Triangle':
            base = float(request.form['base'])
            height = float(request.form['height'])
            area = 0.5 * base * height
            steps = f"Area = 0.5 * {base} * {height} = {area}"
        elif shape == 'Rectangle':
            length = float(request.form['length'])
            width = float(request.form['width'])
            area = length * width
            steps = f"Area = {length} * {width} = {area}"
        elif shape == 'Circle':
            radius = float(request.form['radius'])
            area = math.pi * (radius ** 2)
            steps = f"Area = π * {radius}^2 = {area}"
        elif shape == 'Square':
            side = float(request.form['side'])
            area = side * side
            steps = f"Area = {side}^2 = {area}"

        return render_template('area_result.html', shape=shape, area=area, steps=steps)

    return render_template('area_calculation.html', shape=shape)

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        # Process quiz answers
        answers = request.form
        score = 0

        # Correct answers for each question
        correct_answers = {
            'q1': 'square',
            'q2': 'base*height/2',
            'q3': 'circle',
            'q4': '180',
            'q5': 'rectangle',
            'q6': 'cube'
        }

        # Grading logic
        for question, correct_answer in correct_answers.items():
            if answers.get(question) == correct_answer:
                score += 1

        # Feedback based on the score
        total_questions = len(correct_answers)
        if score == total_questions:
            feedback = "Excellent! You got all questions correct!"
        elif score >= total_questions / 2:
            feedback = "Good job! Keep practicing to get a perfect score!"
        else:
            feedback = "Keep practicing and try again!"

        # Pass score, feedback, and total questions to the result template
        return render_template(
            'quiz_result.html',
            score=score,
            feedback=feedback,
            total_questions=total_questions
        )

    # Render the quiz page for GET requests
    return render_template('quiz.html')


if __name__ == '__main__':
    app.run(debug=True)
