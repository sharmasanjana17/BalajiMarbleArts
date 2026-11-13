from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

# Create db instance - will be initialized in app.py
db = SQLAlchemy()

class Project(db.Model):
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    short_description = db.Column(db.Text)
    category = db.Column(db.String(200))
    location = db.Column(db.String(100))
    client_type = db.Column(db.String(50))
    architect_name = db.Column(db.String(100))
    completion_date = db.Column(db.Date)
    materials = db.Column(db.Text)
    images = db.Column(db.Text)
    videos = db.Column(db.Text)
    before_after_images = db.Column(db.Text)
    challenge = db.Column(db.Text)
    solution = db.Column(db.Text)
    approach = db.Column(db.Text)
    implementation = db.Column(db.Text)
    results = db.Column(db.Text)
    case_study_format = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default='completed')
    featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Service(db.Model):
    __tablename__ = 'services'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(100))
    benefits = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Material(db.Model):
    __tablename__ = 'materials'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50))
    origin = db.Column(db.String(100))
    characteristics = db.Column(db.Text)
    images = db.Column(db.Text)
    finishes = db.Column(db.Text)
    best_use_cases = db.Column(db.Text)
    durability = db.Column(db.String(50))
    price_range = db.Column(db.String(50))
    maintenance = db.Column(db.Text)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Finish(db.Model):
    __tablename__ = 'finishes'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    images = db.Column(db.Text)
    characteristics = db.Column(db.Text)
    benefits = db.Column(db.Text)
    applications = db.Column(db.Text)
    maintenance = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Testimonial(db.Model):
    __tablename__ = 'testimonials'
    
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    rating = db.Column(db.Integer)
    text = db.Column(db.Text, nullable=False)
    photo = db.Column(db.String(200))
    images = db.Column(db.Text)  # JSON array or comma-separated string of image filenames
    location = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    project = db.relationship('Project', backref='testimonials')

class BlogPost(db.Model):
    __tablename__ = 'blog_posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    category = db.Column(db.String(100))
    author = db.Column(db.String(100))
    published_date = db.Column(db.Date)
    featured_image = db.Column(db.String(200))
    images = db.Column(db.Text)  # JSON array or comma-separated string of image filenames
    excerpt = db.Column(db.Text)
    content = db.Column(db.Text)
    tags = db.Column(db.Text)
    seo_keywords = db.Column(db.String(200))
    related_posts = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class FAQ(db.Model):
    __tablename__ = 'faqs'
    
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100))
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ContactLead(db.Model):
    __tablename__ = 'contact_leads'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    project_type = db.Column(db.String(50))
    location = db.Column(db.String(100))
    budget_range = db.Column(db.String(50))
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='new')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Settings(db.Model):
    __tablename__ = 'settings'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text)
    description = db.Column(db.String(200))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

