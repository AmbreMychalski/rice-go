from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
from back import *

app = Flask(__name__, static_folder='react_build')
cors = CORS(app)

@app.route('/api/search', methods=['POST'])
def receive_question():
    
    try:
        data = request.get_json()
        query = data.get('query')
        # Perform your search logic here
        results = {'message': f'Searched for: {query}'}  # Example response
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=3001, debug=True) 