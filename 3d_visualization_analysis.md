# Objective

- Analyze the relationship between alcohol content, residual sugar, and density, and how these features correlate with wine quality.

# Setup

- Dataset: Red Wine Quality Dataset (winequality-red.csv).

## Features Analyzed:
- X-axis: Alcohol
- Y-axis: Residual Sugar
- Z-axis: Density
- Color: Wine Quality (categorical)

# Analysis Process

## Hypothesis:

- Higher alcohol content, lower residual sugar, and lower density may contribute to higher-quality wine.

# Visualization Details:

- Created a 3D scatter plot using Plotly.
- Plotted selected features on the x, y, and z axes.
- Used wine quality as a color indicator.

# Execution Steps:

- Loaded the dataset.
- Allowed users to interactively select features for the 3D visualization.
- Generated a 3D scatter plot to observe patterns and trends.

# Insights and Observations

## Key Observations:

- Wines with lower residual sugar levels and higher alcohol content tend to correspond to higher quality (6–8 range).
- Density shows slight clustering, where higher-quality wines typically have slightly lower density.
- Lower-quality wines (3–5 range) tend to have higher residual sugar and density with lower alcohol content.

## Implications:

- These findings suggest that balancing residual sugar and maintaining higher alcohol levels may improve wine quality.
- Density, while less influential, still plays a role, possibly as an indicator of composition or production quality.

## Challenges

- Overlap of clusters for middle-quality wines (e.g., quality 5 and 6) makes it harder to identify distinct patterns for these ranges.
- The relationship between these variables is visual and qualitative; further quantitative analysis could solidify insights.

# Future Work (Fifth Commit)

## Train a Wine Quality Prediction Model:

- Develop a machine learning model to predict wine quality using key features like alcohol, residual sugar, and density.
- Split the data into training and testing sets and evaluate the model's accuracy.

## Feature Insights:

- Identify which features have the most impact on wine quality by analyzing the model's results.

## Deploy the Model:

- Add a feature to the Flask app that lets users input values and get a predicted wine quality.