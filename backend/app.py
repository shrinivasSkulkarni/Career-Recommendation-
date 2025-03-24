from flask import Flask, request, jsonify
from flask_cors import CORS
from recommender import CareerRecommender
from job_market import JobMarket
from roadmap import RoadmapGenerator
from nlp_utils import ResumeOptimizer
from config import DATASET_PATH, JOB_MARKET_PATH
from models import db
import os

app = Flask(__name__)
CORS(app)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///careerpath.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

with app.app_context():
    db.init_app(app)
    db.create_all()

# Ensure dataset files exist
if not os.path.exists(DATASET_PATH):
    print(f"Error: Dataset file not found at {DATASET_PATH}")
    raise FileNotFoundError(f"Dataset file not found: {DATASET_PATH}")

if not os.path.exists(JOB_MARKET_PATH):
    print(f"Error: Job market file not found at {JOB_MARKET_PATH}")
    raise FileNotFoundError(f"Job market data file not found: {JOB_MARKET_PATH}")

# Initialize Components
recommender = CareerRecommender(DATASET_PATH)
if not hasattr(recommender, "vectors"):
    recommender.train()

job_market = JobMarket(JOB_MARKET_PATH)
roadmap_generator = RoadmapGenerator()
resume_optimizer = ResumeOptimizer()

@app.route('/')
def home():
    return "Welcome to CareerPath AI!"

@app.route('/recommend', methods=['POST'])
def recommend():
    """API endpoint to provide career recommendations"""
    try:
        data = request.json
        skills = data.get('skills', '').strip()
        interests = data.get('interests', '').strip()
        academic_background = data.get('academic_background', '').strip()

        if not skills or not interests or not academic_background:
            return jsonify({"error": "All fields are required"}), 400

        recommendations = recommender.recommend(skills, interests, academic_background)

        print("DEBUG: Career Recommendations:", recommendations)  # Debug log

        return jsonify(recommendations)  # Now properly formatted for frontend
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/job_market', methods=['GET'])
def get_job_market():
    """API endpoint to fetch job market trends"""
    try:
        trends = job_market.get_trends()
        return jsonify({"trends": trends})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/roadmap', methods=['POST'])
def generate_roadmap():
    """API endpoint to generate a roadmap for a career"""
    try:
        data = request.json
        career = data.get('career', '').strip()
        if not career:
            return jsonify({"error": "Career field is required"}), 400
        roadmap = roadmap_generator.generate(career)
        return jsonify({"roadmap": roadmap})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/optimize_resume', methods=['POST'])
def optimize_resume():
    """API endpoint to optimize a resume"""
    try:
        data = request.json
        resume_text = data.get('resume_text', '').strip()
        if not resume_text:
            return jsonify({"error": "Resume text is required"}), 400
        optimized_text = resume_optimizer.optimize(resume_text)
        return jsonify({"optimized_resume": optimized_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("Starting CareerPath AI Backend...")
    print(f"Using dataset from: {DATASET_PATH}")
    print(f"Using job market data from: {JOB_MARKET_PATH}")
    app.run(debug=True, port=5000)
