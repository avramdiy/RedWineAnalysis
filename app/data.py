import os
from flask import Flask, render_template, request, jsonify
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from io import BytesIO
import base64
import joblib

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

# Load the trained model
model = joblib.load('wine_quality_model.pkl')

@app.route('/')
def home():
    return "Welcome to the Flask API. Use /bar-chart to load the bar chart interface. Use /3d-visualization to load the 3D model. Use /predict to load a user-oriented selection of values to calcuate wine quality based on the trained model from the dataset used for this week."

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
    
@app.route('/3d-visualization', methods=['GET', 'POST'])
def three_d_visualization():
    try:
        # Load the dataset
        data = pd.read_csv(DATA_PATH)

        if request.method == 'POST':
            # Get the selected features from the form
            x_feature = request.form.get('x_feature')
            y_feature = request.form.get('y_feature')
            z_feature = request.form.get('z_feature')

            # Validate selected features
            for feature in [x_feature, y_feature, z_feature]:
                if feature not in valid_features:
                    return jsonify({
                        "status": "error",
                        "message": f"Invalid feature selected: {feature}. Choose from {', '.join(valid_features)}"
                    }), 400

            # Generate the 3D plot using Plotly
            fig = px.scatter_3d(
                data, 
                x=x_feature, 
                y=y_feature, 
                z=z_feature,
                color="quality",  # Use wine quality as the color indicator
                title=f"3D Visualization: {x_feature} vs {y_feature} vs {z_feature}"
            )

            # Convert the Plotly figure to an HTML div
            graph_html = fig.to_html(full_html=False)

            return render_template(
                '3d_visualization.html',
                graph_html=graph_html,
                valid_features=valid_features,
                selected_x=x_feature,
                selected_y=y_feature,
                selected_z=z_feature
            )

        # Serve the form for selecting features if GET request
        return render_template(
            '3d_visualization.html', 
            graph_html=None, 
            valid_features=valid_features
        )

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            # Get values from the form
            density = float(request.form['density'])
            residual_sugar = float(request.form['residual_sugar'])
            alcohol = float(request.form['alcohol'])

            # Predict wine quality using the model
            prediction = model.predict([[density, residual_sugar, alcohol]])[0]

            return render_template('predict.html', prediction=prediction)

        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

    return render_template('predict.html', prediction=None)

if __name__ == '__main__':
    app.run(debug=True)
