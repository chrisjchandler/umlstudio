from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Define template for UML code generation
uml_template = """
@startuml
{groupings}
{relationships}
@enduml
"""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_uml', methods=['POST'])
def generate_uml():
    groupings = {}
    relationships = []

    # Parse form data for groupings
    for key, value in request.form.items():
        if key.startswith('entities_group_'):
            group_name = key.split('_')[2]
            groupings[group_name] = value.split(',')

    # Parse form data for relationships and actions
    for key, value in request.form.items():
        if key.startswith('relationship_source_'):
            relationship_index = key.split('_')[2]
            source_group = value
            target_group = request.form[f'relationship_target_{relationship_index}']
            action = request.form[f'action_{relationship_index}']
            if source_group and target_group:
                # Enclose relationship label in double quotes
                relationships.append(f'"{source_group}" --> "{target_group}" : "{action}"')

    # Generate UML code for groupings
    grouping_code = '\n\n'.join([f'package {group_name} {{\n' +
                                 ''.join([f'class {entity} {{\n}}\n' for entity in entities]) +
                                 '}' for group_name, entities in groupings.items()])
    
    # Generate UML code for relationships
    relationship_code = '\n'.join([f'{relationship}\n' for relationship in relationships])

    uml_code = uml_template.format(groupings=grouping_code, relationships=relationship_code)
    return jsonify({'uml_code': uml_code})

if __name__ == '__main__':
    app.run(debug=True)
