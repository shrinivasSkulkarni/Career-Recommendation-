from flask_sqlalchemy import SQLAlchemy


# Initialize SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    """
    User model to store user information.
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    skills = db.Column(db.String(200), nullable=True)
    interests = db.Column(db.String(200), nullable=True)
    academic_background = db.Column(db.String(200), nullable=True)

    # Relationship to recommendations
    recommendations = db.relationship('Recommendation', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"

class Recommendation(db.Model):
    """
    Recommendation model to store career recommendations for users.
    """
    __tablename__ = 'recommendations'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    career = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"<Recommendation {self.career}>"

class JobMarketData(db.Model):
    """
    Job market data model to store industry trends and insights.
    """
    __tablename__ = 'job_market_data'
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(200), nullable=False)
    demand_level = db.Column(db.String(50), nullable=False)  # e.g., High, Medium, Low
    salary_range = db.Column(db.String(100), nullable=False)  # e.g., $50,000 - $70,000
    skills_required = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f"<JobMarketData {self.job_title}>"

class Roadmap(db.Model):
    """
    Roadmap model to store step-by-step career roadmaps.
    """
    __tablename__ = 'roadmaps'
    id = db.Column(db.Integer, primary_key=True)
    career = db.Column(db.String(200), nullable=False)
    steps = db.Column(db.String(1000), nullable=False)  # JSON or comma-separated steps

    def __repr__(self):
        return f"<Roadmap {self.career}>"