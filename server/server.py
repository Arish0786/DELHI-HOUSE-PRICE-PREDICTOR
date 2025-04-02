from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import util

app = Flask(__name__, static_folder='../client', template_folder='../client')
CORS(app)  # Enable CORS

# Load model artifacts at startup (Fix for Gunicorn)
util.load_saved_artifacts()

@app.route('/<path:filename>')
def serve_static_files(filename):
    return app.send_static_file(filename)

@app.route('/')
def home():
    return render_template('app.html')

@app.route('/api/get_location_names', methods=['GET'])
def get_location_names():
    response = jsonify({
        'locations': util.get_location_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/api/predict_home_price', methods=['POST'])
def predict_home_price():
    data = request.get_json()

    try:
        area = float(data['area'])
        bhk = int(data['bhk'])
        bath = int(data['bath'])
        location = data['location']
        estimated_price = util.get_estimated_price(location, area, bhk, bath)
        response = jsonify({
            'estimated_price': estimated_price
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    except KeyError as e:
        return jsonify({'error': f'Missing key: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting Python Flask Server For Home Price Prediction...")
    app.run(host="0.0.0.0", port=5000, debug=True)
