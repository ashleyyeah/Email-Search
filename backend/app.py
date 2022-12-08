from flask import Flask, request, jsonify
from flask_cors import CORS

from index_search import index_search

app = Flask(__name__)
CORS(app) 

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

@app.route('/api/search', methods=['GET'])
def search():
    # Call the Python function here
    query = request.args['query']
    print(query)
    result = index_search(query)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='localhost', port=5000)