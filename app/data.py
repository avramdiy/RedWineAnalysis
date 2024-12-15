import os
from flask import Flask, render_template, request, jsonify
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# Set the correct path to the templates folder in the root directory
app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'))

# Define the path to the dataset
DATA_PATH = r'C:\Users\Ev\Desktop\RedWineAnalysis\winequality-red.csv'

# List of valid features
valid_features = [
    "alcohol", "chlorides", "citric acid", "density", "fixed acidity", 
    "free sulfur dioxide", "pH", "quality", "residual sugar", 
    "sulphates", "total sulfur dioxide", "volatile acidity"
]

@app.route('/')
def home():
    return "Welcome to the Flask API. Use /bar-chart to load the bar chart interface."

@app.route('/bar-chart', methods=['GET', 'POST'])
def bar_chart():
    try:
        if request.method == 'POST':
            # Get the feature names from the form
            x_feature = request.form.get('x_feature')
            y_feature = request.form.get('y_feature')

            # Validate features
            if x_feature not in valid_features:
                return jsonify({"status": "error", "message": f"Invalid x-axis feature: {x_feature}. Choose from {', '.join(valid_features)}"}), 400
            if y_feature != 'count' and y_feature not in valid_features:
                return jsonify({"status": "error", "message": f"Invalid y-axis feature: {y_feature}. Choose from {', '.join(valid_features)}"}), 400

            # Load the dataset
            data = pd.read_csv(DATA_PATH)

            # If y_feature is 'count', we need to count the occurrences of the x_feature values
            if y_feature == 'count':
                feature_counts = data[x_feature].value_counts().sort_index()
            else:
                feature_counts = data.groupby(x_feature)[y_feature].mean()

            # Create the plot
            plt.figure(figsize=(8, 6))
            feature_counts.plot(kind='bar', color='skyblue')
            plt.title(f'{x_feature.capitalize()} vs {y_feature.capitalize()}' if y_feature != 'count' else f'{x_feature.capitalize()} Distribution', fontsize=16)
            plt.xlabel(x_feature.capitalize(), fontsize=14)
            plt.ylabel(y_feature.capitalize() if y_feature != 'count' else 'Count', fontsize=14)
            plt.grid(axis='y', linestyle='--', alpha=0.7)

            # Save the plot to a BytesIO buffer
            buf = BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            plot_url = base64.b64encode(buf.getvalue()).decode('utf8')
            buf.close()

            return render_template('bar_chart.html', plot_url=plot_url, valid_features=valid_features, selected_x=x_feature, selected_y=y_feature)
        
        # Serve the form for selecting features if GET request
        return render_template('bar_chart.html', valid_features=valid_features, plot_url=None)
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
