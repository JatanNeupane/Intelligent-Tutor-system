from flask import Flask, render_template, request
import math
from rdflib import Graph, URIRef, Literal, Namespace

# Initialize Flask app
app = Flask(__name__)

# Load ontology using RDFLib
ontology_file = "shapes.owl"
graph = Graph()
graph.parse(ontology_file, format="xml")

# Define namespaces
EX = Namespace("http://www.semanticweb.org/ontologies/2024/12/ShapeOntology#")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")

# Fallback dictionary for shape descriptions
default_shape_descriptions = {
    "Triangle": "A triangle has three sides. Its area is calculated as 0.5 × base × height.",
    "Rectangle": "A rectangle has four sides with opposite sides equal. Its area is length × width.",
    "Circle": "A circle is a round shape. Its area is π × radius².",
    "Square": "A square has four equal sides. Its area is side²."
}

# Query for shape descriptions from ontology
def get_shape_description(shape):
    shape_uri = EX[shape]
    query = (
        "SELECT ?comment WHERE { "
        f"<" + str(shape_uri) + "> <" + str(RDFS.comment) + "> ?comment. "
        "}"
    )
    result = graph.query(query)
    for row in result:
        return str(row.comment)
    return default_shape_descriptions.get(shape, "No description available.")

# Query for data properties dynamically
def get_datatype_properties(shape):
    shape_uri = EX[shape]
    query = (
        "SELECT ?property WHERE { "
        f"<" + str(shape_uri) + "> ?property ?value. "
        "FILTER (strstarts(str(?property), \"http://www.semanticweb.org/ontologies/2024/12/ShapeOntology#\")) "
        "}"
    )
    properties = []
    for row in graph.query(query):
        property_name = str(row.property).split("#")[-1]
        properties.append(property_name)
    return properties

# Function to compute area based on properties
shape_area_calculators = {
    "Triangle": lambda props: 0.5 * props['base'] * props['height'],
    "Rectangle": lambda props: props['length'] * props['width'],
    "Circle": lambda props: math.pi * (props['radius'] ** 2),
    "Square": lambda props: props['side'] ** 2
}

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
        properties = get_datatype_properties(shape)
    except Exception as e:
        description = "Information not available."
        properties = []

    return render_template('learn_about_shape.html', shape=shape, description=description, properties=properties)

@app.route('/area_calculation/<shape>', methods=['GET', 'POST'])
def area_calculation(shape):
    area = None
    steps = ""
    if request.method == 'POST':
        try:
            # Fetch required properties for the shape dynamically
            properties = get_datatype_properties(shape)
            inputs = {prop: float(request.form[prop]) for prop in properties}

            # Calculate the area
            if shape in shape_area_calculators:
                area = shape_area_calculators[shape](inputs)
                steps = f"Area calculated using {inputs}: {area}"
        except Exception as e:
            steps = f"Error in calculation: {str(e)}"

        return render_template('area_result.html', shape=shape, area=area, steps=steps)

    return render_template('area_calculation.html', shape=shape)

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        # Process quiz answers
        answers = request.form
        score = 0

        # Example logic for grading the quiz
        if answers.get('q1') == 'a':  # Assume correct answer for q1 is "a"
            score += 1

        # Add feedback based on the score
        feedback = "Great job!" if score == 1 else "Keep practicing!"

        # Pass both score and feedback to the template
        return render_template('quiz_result.html', score=score, feedback=feedback)

    # Render the quiz page for GET requests
    return render_template('quiz.html')

if __name__ == '__main__':
    app.run(debug=True)
