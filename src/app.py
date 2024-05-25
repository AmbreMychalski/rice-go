from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
from back import *

app = Flask(__name__, static_folder='react_build')
cors = CORS(app)

@app.route('/api/search', methods=['POST'])
def receive_question():
    
    try:
        data = request.get_json()
        dna_seq = data.get('query')
        if len(dna_seq)==0 or dna_seq.isspace():
            return jsonify({'error': 'La pregunta esta vacia'}), 204
        print(dna_seq)
        # Perform your search logic here
        (predicted_class_labels_go0, predicted_class_labels_go1, namespace, prot_seq) = predict(dna_seq)
        print(predicted_class_labels_go0, predicted_class_labels_go1, namespace, prot_seq)
        response = {
            'dna_seq': f"{dna_seq}",
            'prot_seq': f'{prot_seq}',
            'go0': f"{predicted_class_labels_go0}",
            'go1': f"{predicted_class_labels_go1}",
            'namespace': f"{namespace.replace('_', ' ')}",
        }
        results = {'message': response}  # Example response
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=3001, debug=True) 