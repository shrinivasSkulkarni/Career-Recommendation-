import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class CareerRecommender:
    def __init__(self, data_path):
        abs_path = os.path.abspath(data_path)
        print(f"Looking for dataset at: {abs_path}")

        if not os.path.exists(abs_path):
            raise FileNotFoundError(f"Dataset file not found: {abs_path}")

        self.data = pd.read_csv(abs_path)

        # Debugging: Print dataset columns
        print("Columns in dataset:", self.data.columns.tolist())

        # Ensure required columns exist
        required_columns = {"Skills", "Interests", "Academic Background", "Recommended_Career"}  # Updated column name
        missing_columns = required_columns - set(self.data.columns)

        if missing_columns:
            raise ValueError(f"Missing columns in dataset: {', '.join(missing_columns)}")

        self.vectorizer = TfidfVectorizer()

    def train(self):
        """Train the vectorizer on the dataset"""
        self.data.fillna('', inplace=True)  # Replace NaN values with empty strings
        self.data['combined'] = self.data['Skills'] + " " + self.data['Interests'] + " " + self.data['Academic Background']
        self.vectors = self.vectorizer.fit_transform(self.data['combined'])

    def recommend(self, skills, interests, academic_background):
        input_text = f"{skills} {interests} {academic_background}"
        print("User Input:", input_text)  # Debugging

        try:
            input_vector = self.vectorizer.transform([input_text])
            similarities = cosine_similarity(input_vector, self.vectors).flatten()
            
            # Debugging: Print similarity scores
            print("Similarity Scores:", similarities)

            sorted_indices = similarities.argsort()[::-1]
            recommended_careers = self.data.iloc[sorted_indices]['Recommended_Career'].tolist()

            print("Recommended Careers:", recommended_careers[:5])  # Debugging
            return {"recommendations": recommended_careers[:5]}  
        except Exception as e:
            print(f"Error: {e}")
            return {"error": "An error occurred while generating recommendations."}

