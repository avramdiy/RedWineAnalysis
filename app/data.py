from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

# Define the path to the dataset
DATA_PATH = r'C:\Users\Ev\Desktop\RedWineAnalysis\winequality-red.csv'

@app.route('/')
def home():
    return "Welcome to the Flask API. Use /load-data to load the dataset."

@app.route('/load-data', methods=['GET'])
def load_data():
    try:
        # Load the dataset
        data = pd.read_csv(DATA_PATH)
        
        # Convert the data to a JSON-friendly format
        data_json = data.to_dict(orient='records')
        
        return jsonify({"status": "success", "data": data_json}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
