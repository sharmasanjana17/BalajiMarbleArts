# Eventlet monkey patching must be executed before anything else for high-concurrency non-blocking I/O
try:
    import eventlet
    eventlet.monkey_patch()
except (ImportError, Exception):
    pass

from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask_socketio import SocketIO, emit, join_room, leave_room
from datetime import datetime
import os
import json
import urllib.parse
import urllib.request
from werkzeug.utils import secure_filename

# Helper function to safely parse JSON
def safe_json_loads(json_string, default=None):
    """Safely parse JSON or comma-separated string, return list/dict/default"""
    if default is None:
        default = []
    if not json_string:
        return default
    if isinstance(json_string, list):
        return [str(x).strip() for x in json_string if str(x).strip()]
    if isinstance(json_string, str):
        json_string = json_string.strip()
        if not json_string:
            return default
        try:
            parsed = json.loads(json_string)
            if isinstance(parsed, list):
                return [str(x).strip() for x in parsed if str(x).strip()]
            return parsed
        except (json.JSONDecodeError, ValueError, TypeError):
            if isinstance(default, list):
                return [x.strip() for x in json_string.split(',') if x.strip()]
            return default
    return default

app = Flask(__name__)

# Aggressive browser caching for static assets (CSS, JS, 455 project photos)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000  # 1 year

@app.after_request
def add_performance_headers(response):
    """Add browser caching headers to make page navigation ultra-fast"""
    if request.path.startswith('/static/'):
        response.headers['Cache-Control'] = 'public, max-age=31536000, immutable'
    elif response.content_type and 'text/html' in response.content_type:
        response.headers['Cache-Control'] = 'no-cache, must-revalidate'
    return response

# SocketIO initialization with fallback for Windows / Python environments
try:
    import eventlet
    socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')
except (ImportError, Exception):
    socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# File Upload Configuration
UPLOAD_FOLDER = 'static'
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'webm', 'ogg', 'mov'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

def allowed_file(filename, file_type='image'):
    """Check if file extension is allowed"""
    if '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    if file_type == 'image':
        return ext in ALLOWED_IMAGE_EXTENSIONS
    elif file_type == 'video':
        return ext in ALLOWED_VIDEO_EXTENSIONS
    return False

# Business Information (Change here and it will update everywhere)
BUSINESS_NAME = "Balaji Marble Arts"
OWNER_NAME = "Ashok Sharma"
BUSINESS_EMAIL = "balajimarbleartss@gmail.com"
BUSINESS_PHONE = "+91 9242401059"
BUSINESS_LOCATION = "Bengaluru, Karnataka, India"

# Telegram Bot Configuration
# Get your bot token from @BotFather on Telegram
# Get your chat ID from @userinfobot or @getidsbot
# For group chats, chat ID will be negative (e.g., -1001234567890)
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')  # Set via environment variable or change here
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', '')  # Set via environment variable or change here

def get_setting(key, default=''):
    """Get setting value from database"""
    try:
        setting = Settings.query.filter_by(key=key).first()
        if setting and setting.value:
            return setting.value
    except:
        pass
    return default

def set_setting(key, value, description=''):
    """Set setting value in database"""
    try:
        setting = Settings.query.filter_by(key=key).first()
        if setting:
            setting.value = value
            if description:
                setting.description = description
        else:
            setting = Settings(key=key, value=value, description=description)
            db.session.add(setting)
        db.session.commit()
        return True
    except Exception as e:
        print(f"Error saving setting: {e}")
        db.session.rollback()
        return False

def send_telegram_message(message_text):
    """Send message to Telegram bot - works with both individual and group chat IDs"""
    # Get settings from database, fallback to environment variables
    bot_token = get_setting('telegram_bot_token') or TELEGRAM_BOT_TOKEN
    chat_id = get_setting('telegram_chat_id') or TELEGRAM_CHAT_ID
    
    if not bot_token or not chat_id:
        print("Telegram bot not configured. Set telegram_bot_token and telegram_chat_id in admin panel.")
        return False
    
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        
        # Prepare data - chat_id can be positive (individual) or negative (group)
        data = {
            'chat_id': chat_id,  # Works with both positive and negative IDs
            'text': message_text,
            'parse_mode': 'HTML'
        }
        
        # Encode data
        data = urllib.parse.urlencode(data).encode('utf-8')
        
        # Send request
        req = urllib.request.Request(url, data=data)
        with urllib.request.urlopen(req, timeout=10) as response:
            result = response.read().decode('utf-8')
            return True
    except Exception as e:
        print(f"Telegram error: {e}")
        return False

# Configuration directly in app.py
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')

# Admin Credentials (Change these in production!)
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')

# Database file in root folder (not in database/ folder)
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app.db').replace('\\', '/')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Email configuration (if using Flask-Mail)
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

from src.models import db
db.init_app(app)
mail = Mail(app)

def parse_json(value):
    if not value:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str):
        value = value.strip()
        if not value:
            return []
        if value.startswith('['):
            try:
                loaded = json.loads(value)
                if isinstance(loaded, list):
                    return [str(item).strip() for item in loaded if str(item).strip()]
            except:
                pass
        # Comma-separated fallback
        items = value.split(',')
        return [item.strip() for item in items if item.strip()]
    return []

# Make get_setting available in all templates
@app.context_processor
def inject_get_setting():
    return dict(get_setting=get_setting)

# Make safe_json_loads and split_benefits available in templates
@app.context_processor
def inject_json_loader():
    def parse_json(value):
        if not value:
            return []
        if isinstance(value, list):
            return [str(item).strip() for item in value if str(item).strip()]
        if isinstance(value, str):
            value = value.strip()
            if not value:
                return []
            if value.startswith('['):
                try:
                    loaded = json.loads(value)
                    if isinstance(loaded, list):
                        return [str(item).strip() for item in loaded if str(item).strip()]
                except:
                    pass
            # Comma-separated fallback
            items = value.split(',')
            return [item.strip() for item in items if item.strip()]
        return []

    def split_benefits(value):
        if not value:
            return []
        if isinstance(value, list):
            return [str(x).strip() for x in value if str(x).strip()]
        if isinstance(value, str):
            value = value.strip()
            if '\n' in value:
                return [line.strip() for line in value.split('\n') if line.strip()]
            if ',' in value:
                return [item.strip() for item in value.split(',') if item.strip()]
            return [value] if value else []
        return []

    return dict(parse_json=parse_json, split_benefits=split_benefits)

# Database migration and initialization - Add videos column if missing (runs on startup)
from src.database import migrate_database, init_database
migrate_database(app)

# Import models (needed for initialization)
from src.models import Project, Service, Material, Finish, Testimonial, BlogPost, FAQ, ContactLead, Settings

# Initialize database with sample data if empty
with app.app_context():
    # Create tables if they don't exist
    db.create_all()
    
    # Initialize default settings if they don't exist
    try:
        if not Settings.query.filter_by(key='telegram_bot_token').first():
            set_setting('telegram_bot_token', '', 'Telegram Bot Token from @BotFather')
        if not Settings.query.filter_by(key='telegram_chat_id').first():
            set_setting('telegram_chat_id', '', 'Telegram Chat ID (individual or group)')
    except:
        pass
    
    # Check if database is empty and initialize with sample data
    try:
        project_count = Project.query.count()
        if project_count == 0:
            print("Database is empty. Initializing with sample data...")
            init_database(app)
        else:
            print(f"Database already has {project_count} projects.")
    except Exception as e:
        print(f"Error checking database: {e}. Initializing database...")
        init_database(app)

# Routes
# Context processor to make business info available in all templates
@app.context_processor
def inject_business_info():
    return {
        'business_name': BUSINESS_NAME,
        'owner_name': OWNER_NAME,
        'business_email': BUSINESS_EMAIL,
        'business_phone': BUSINESS_PHONE,
        'business_location': BUSINESS_LOCATION
    }

@app.route('/')
def index():
    featured_projects = Project.query.filter_by(featured=True).limit(6).all()
    testimonials = Testimonial.query.limit(4).all()
    services = Service.query.all()
    return render_template('index.html', 
                         featured_projects=featured_projects,
                         testimonials=testimonials,
                         services=services)

@app.route('/portfolio')
def portfolio():
    category = request.args.get('category', 'all')
    search = request.args.get('search', '')
    
    # Get all projects, not just completed ones
    query = Project.query
    
    if category != 'all':
        query = query.filter(Project.category.contains(category))
    
    if search:
        query = query.filter(
            Project.title.contains(search) |
            Project.location.contains(search) |
            Project.description.contains(search)
        )
    
    from sqlalchemy import desc, case
    projects = query.order_by(
        case((Project.completion_date.isnot(None), Project.completion_date), else_=Project.created_at).desc()
    ).all()
    
    # If no projects, return empty list (will show "No projects found" message)
    return render_template('portfolio.html', projects=projects, current_category=category, search=search)

@app.route('/portfolio/<int:project_id>')
def project_detail(project_id):
    project = Project.query.get_or_404(project_id)
    related_projects = Project.query.filter(
        Project.id != project_id,
        Project.category.contains(project.category.split(',')[0] if project.category else '')
    ).limit(3).all()
    return render_template('project_detail.html', project=project, related_projects=related_projects)

@app.route('/services')
def services():
    services = Service.query.all()
    return render_template('services.html', services=services)

@app.route('/materials')
def materials():
    category = request.args.get('category', 'all')
    finish_filter = request.args.get('finish', 'all')
    
    query = Material.query
    if category != 'all':
        query = query.filter_by(type=category)
    
    materials = query.all()
    finishes = Finish.query.all()
    return render_template('materials.html', materials=materials, finishes=finishes, 
                         current_category=category, current_finish=finish_filter)

@app.route('/about')
def about():
    total_projects = Project.query.count()
    residential_count = Project.query.filter_by(client_type='Residential').count()
    commercial_count = Project.query.filter_by(client_type='Commercial').count()
    
    about_description = get_setting('about_description', '')
    about_specialization = get_setting('about_specialization', '')
    projects_completed = get_setting('projects_completed', '60+')
    residential_projects = get_setting('residential_projects', '40')
    commercial_projects = get_setting('commercial_projects', '20')
    years_experience = get_setting('years_experience', '20+')
    serving_text = get_setting('serving_text', '')
    
    return render_template('about.html', 
                         total_projects=total_projects,
                         residential_count=residential_count,
                         commercial_count=commercial_count,
                         about_description=about_description,
                         about_specialization=about_specialization,
                         projects_completed=projects_completed,
                         residential_projects=residential_projects,
                         commercial_projects=commercial_projects,
                         years_experience=years_experience,
                         serving_text=serving_text)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        project_type = request.form.get('project_type')
        location = request.form.get('location')
        budget_range = request.form.get('budget_range')
        message = request.form.get('message')
        
        lead = ContactLead(
            name=name,
            email=email,
            phone=phone,
            project_type=project_type,
            location=location,
            budget_range=budget_range,
            message=message,
            status='new'
        )
        db.session.add(lead)
        db.session.commit()
        
        # Send Telegram notification
        telegram_message = f"""
🔔 <b>New Contact Form Submission</b>

👤 <b>Name:</b> {name}
📧 <b>Email:</b> {email}
📱 <b>Phone:</b> {phone}
🏗️ <b>Project Type:</b> {project_type or 'Not specified'}
📍 <b>Location:</b> {location or 'Not specified'}
💰 <b>Budget Range:</b> {budget_range or 'Not specified'}

💬 <b>Message:</b>
{message}

⏰ <b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        send_telegram_message(telegram_message)
        
        # Send email notification
        try:
            msg = Message(
                subject=f'New Contact Form Submission - {name}',
                sender=app.config['MAIL_USERNAME'],
                recipients=[app.config['MAIL_USERNAME']],
                body=f'''
                New lead from website:
                
                Name: {name}
                Email: {email}
                Phone: {phone}
                Project Type: {project_type}
                Location: {location}
                Budget Range: {budget_range}
                
                Message:
                {message}
                '''
            )
            mail.send(msg)
        except:
            pass  # Email sending failed, but lead is saved
        
        flash('Thank you! We will contact you soon.', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

@app.route('/testimonials')
def testimonials():
    testimonials = Testimonial.query.order_by(Testimonial.created_at.desc()).all()
    return render_template('testimonials.html', testimonials=testimonials)

@app.route('/blog')
def blog():
    posts = BlogPost.query.filter(BlogPost.published_date <= datetime.now().date()).order_by(BlogPost.published_date.desc()).all()
    return render_template('blog.html', posts=posts)

@app.route('/blog/<int:post_id>')
def blog_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    related_posts = BlogPost.query.filter(
        BlogPost.id != post_id,
        BlogPost.category == post.category
    ).limit(3).all()
    return render_template('blog_post.html', post=post, related_posts=related_posts)

@app.route('/faq')
def faq():
    category = request.args.get('category', 'all')
    query = FAQ.query
    if category != 'all':
        query = query.filter_by(category=category)
    faqs = query.order_by(FAQ.order).all()
    categories = db.session.query(FAQ.category).distinct().all()
    return render_template('faq.html', faqs=faqs, categories=[c[0] for c in categories], current_category=category)

# ============================================
# ADMIN ROUTES
# ============================================

def admin_required(f):
    """Decorator to require admin login"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            flash('Please login to access admin panel', 'warning')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            flash('Login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash('Logged out successfully', 'info')
    return redirect(url_for('admin_login'))

@app.route('/admin')
@admin_required
def admin_dashboard():
    # Get all data for single page admin
    testimonials = Testimonial.query.order_by(Testimonial.created_at.desc()).all()
    projects = Project.query.order_by(Project.created_at.desc()).all()
    blog_posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    faqs = FAQ.query.order_by(FAQ.order, FAQ.created_at).all()
    services = Service.query.all()
    materials = Material.query.all()
    contacts = ContactLead.query.order_by(ContactLead.created_at.desc()).all()
    
    # About page stats
    total_projects = Project.query.count()
    residential_count = Project.query.filter_by(client_type='Residential').count()
    commercial_count = Project.query.filter_by(client_type='Commercial').count()
    
    # Get Telegram settings
    telegram_bot_token = get_setting('telegram_bot_token', '')
    telegram_chat_id = get_setting('telegram_chat_id', '')
    
    # Get About page settings
    about_description = get_setting('about_description', '')
    about_specialization = get_setting('about_specialization', '')
    projects_completed = get_setting('projects_completed', '60')
    residential_projects = get_setting('residential_projects', '40')
    commercial_projects = get_setting('commercial_projects', '20')
    years_experience = get_setting('years_experience', '20+')
    serving_text = get_setting('serving_text', '')
    
    return render_template('admin/manage.html', 
                         testimonials=testimonials,
                         projects=projects,
                         blog_posts=blog_posts,
                         faqs=faqs,
                         services=services,
                         materials=materials,
                         contacts=contacts,
                         total_projects=total_projects,
                         residential_count=residential_count,
                         commercial_count=commercial_count,
                         telegram_bot_token=telegram_bot_token,
                         telegram_chat_id=telegram_chat_id,
                         about_description=about_description,
                         about_specialization=about_specialization,
                         projects_completed=projects_completed,
                         residential_projects=residential_projects,
                         commercial_projects=commercial_projects,
                         years_experience=years_experience,
                         serving_text=serving_text)

# ============================================
# TESTIMONIALS MANAGEMENT
# ============================================

@app.route('/admin/testimonials')
@admin_required
def admin_testimonials():
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/testimonials/add', methods=['POST'])
@admin_required
def admin_add_testimonial():
    try:
        testimonial = Testimonial(
            client_name=request.form.get('client_name'),
            location=request.form.get('location'),
            rating=int(request.form.get('rating')),
            text=request.form.get('text'),
            project_id=request.form.get('project_id') or None
        )
        db.session.add(testimonial)
        db.session.commit()
        flash('Testimonial added successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding testimonial: {str(e)}', 'danger')
    
    return redirect(url_for('admin_dashboard') + '#testimonials')

@app.route('/admin/testimonials/edit/<int:id>')
@admin_required
def admin_edit_testimonial(id):
    testimonial = Testimonial.query.get_or_404(id)
    projects = Project.query.all()
    # Return to single page admin with edit modal data
    return render_template('admin/edit_testimonial.html', testimonial=testimonial, projects=projects)

@app.route('/admin/testimonials/update/<int:id>', methods=['POST'])
@admin_required
def admin_update_testimonial(id):
    try:
        testimonial = Testimonial.query.get_or_404(id)
        testimonial.client_name = request.form.get('client_name')
        testimonial.location = request.form.get('location')
        testimonial.rating = int(request.form.get('rating'))
        testimonial.text = request.form.get('text')
        testimonial.project_id = request.form.get('project_id') or None
        db.session.commit()
        flash('Testimonial updated successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating testimonial: {str(e)}', 'danger')
    
    return redirect(url_for('admin_dashboard') + '#testimonials')

@app.route('/admin/testimonials/delete/<int:id>')
@admin_required
def admin_delete_testimonial(id):
    try:
        testimonial = Testimonial.query.get_or_404(id)
        db.session.delete(testimonial)
        db.session.commit()
        flash('Testimonial deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting testimonial: {str(e)}', 'danger')
    
    return redirect(url_for('admin_dashboard') + '#testimonials')

# ============================================
# PROJECTS MANAGEMENT
# ============================================

@app.route('/admin/projects')
@admin_required
def admin_projects():
    return redirect(url_for('admin_dashboard') + '#projects')

@app.route('/admin/projects/add', methods=['GET', 'POST'])
@admin_required
def admin_add_project():
    if request.method == 'POST':
        try:
            # Handle file uploads
            uploaded_images = []
            uploaded_videos = []
            
            # Process uploaded images
            if 'project_images' in request.files:
                files = request.files.getlist('project_images')
                for file in files:
                    if file and file.filename and allowed_file(file.filename, 'image'):
                        filename = secure_filename(file.filename)
                        # Add timestamp to avoid conflicts
                        from time import time
                        filename = f"{int(time())}_{filename}"
                        filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'images', 'projects', filename)
                        os.makedirs(os.path.dirname(filepath), exist_ok=True)
                        file.save(filepath)
                        uploaded_images.append(filename)
            
            # Process uploaded videos
            if 'project_videos' in request.files:
                files = request.files.getlist('project_videos')
                for file in files:
                    if file and file.filename and allowed_file(file.filename, 'video'):
                        filename = secure_filename(file.filename)
                        from time import time
                        filename = f"{int(time())}_{filename}"
                        filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'videos', 'projects', filename)
                        os.makedirs(os.path.dirname(filepath), exist_ok=True)
                        file.save(filepath)
                        uploaded_videos.append(filename)
            
            # Also support manual filenames if entered in text input
            text_images = request.form.get('images', '').strip()
            if text_images:
                uploaded_images.extend([x.strip() for x in text_images.split(',') if x.strip()])

            images_json = json.dumps(uploaded_images) if uploaded_images else '[]'
            videos_json = json.dumps(uploaded_videos) if uploaded_videos else '[]'
            
            project = Project(
                title=request.form.get('title'),
                description=request.form.get('description'),
                short_description=request.form.get('short_description'),
                category=request.form.get('category'),
                location=request.form.get('location'),
                client_type=request.form.get('client_type'),
                architect_name=request.form.get('architect_name'),
                completion_date=datetime.strptime(request.form.get('completion_date'), '%Y-%m-%d').date() if request.form.get('completion_date') else None,
                materials=request.form.get('materials'),
                images=images_json,
                videos=videos_json,
                featured=request.form.get('featured') == 'on',
                status=request.form.get('status', 'completed')
            )
            db.session.add(project)
            db.session.commit()
            flash('Project added successfully!', 'success')
            return redirect(url_for('admin_dashboard') + '#projects')
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding project: {str(e)}', 'danger')
    
    return render_template('admin/add_project.html')

@app.route('/admin/projects/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_project(id):
    project = Project.query.get_or_404(id)
    
    # Parse existing images and videos for display
    existing_images = safe_json_loads(project.images, [])
    existing_videos = safe_json_loads(project.videos, [])
    
    if request.method == 'POST':
        try:
            # Get existing images and videos
            existing_images = safe_json_loads(project.images, [])
            existing_videos = safe_json_loads(project.videos, [])
            
            # Handle new file uploads
            uploaded_images = []
            uploaded_videos = []
            
            # Process uploaded images
            if 'project_images' in request.files:
                files = request.files.getlist('project_images')
                for file in files:
                    if file and file.filename and allowed_file(file.filename, 'image'):
                        filename = secure_filename(file.filename)
                        from time import time
                        filename = f"{int(time())}_{filename}"
                        filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'images', 'projects', filename)
                        os.makedirs(os.path.dirname(filepath), exist_ok=True)
                        file.save(filepath)
                        uploaded_images.append(filename)
            
            # Process uploaded videos
            if 'project_videos' in request.files:
                files = request.files.getlist('project_videos')
                for file in files:
                    if file and file.filename and allowed_file(file.filename, 'video'):
                        filename = secure_filename(file.filename)
                        from time import time
                        filename = f"{int(time())}_{filename}"
                        filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'videos', 'projects', filename)
                        os.makedirs(os.path.dirname(filepath), exist_ok=True)
                        file.save(filepath)
                        uploaded_videos.append(filename)
            
            # Remove deleted images
            deleted_images = request.form.getlist('deleted_images')
            remaining_images = [img for img in existing_images if img not in deleted_images]
            all_images = remaining_images + uploaded_images
            
            # Remove deleted videos
            deleted_videos = request.form.getlist('deleted_videos')
            remaining_videos = [vid for vid in existing_videos if vid not in deleted_videos]
            all_videos = remaining_videos + uploaded_videos
            
            project.title = request.form.get('title')
            project.description = request.form.get('description')
            project.short_description = request.form.get('short_description')
            project.category = request.form.get('category')
            project.location = request.form.get('location')
            project.client_type = request.form.get('client_type')
            project.architect_name = request.form.get('architect_name')
            if request.form.get('completion_date'):
                project.completion_date = datetime.strptime(request.form.get('completion_date'), '%Y-%m-%d').date()
            project.materials = request.form.get('materials')
            project.featured = request.form.get('featured') == 'on'
            project.status = request.form.get('status', 'completed')
            project.images = json.dumps(all_images) if all_images else '[]'
            project.videos = json.dumps(all_videos) if all_videos else '[]'
            project.updated_at = datetime.utcnow()
            db.session.commit()
            flash('Project updated successfully!', 'success')
            return redirect(url_for('admin_dashboard') + '#projects')
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating project: {str(e)}', 'danger')
    
    project_images = safe_json_loads(project.images, [])
    project_videos = safe_json_loads(project.videos, [])
    return render_template('admin/edit_project.html', project=project, 
                         project_images=project_images, project_videos=project_videos)

@app.route('/admin/projects/delete/<int:id>')
@admin_required
def admin_delete_project(id):
    try:
        project = Project.query.get_or_404(id)
        db.session.delete(project)
        db.session.commit()
        flash('Project deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting project: {str(e)}', 'danger')
    
    return redirect(url_for('admin_projects'))

# ============================================
# BLOG MANAGEMENT
# ============================================

@app.route('/admin/blog')
@admin_required
def admin_blog():
    return redirect(url_for('admin_dashboard') + '#blog')

@app.route('/admin/blog/add', methods=['GET', 'POST'])
@admin_required
def admin_add_blog():
    if request.method == 'POST':
        try:
            # Generate slug from title
            import re
            title = request.form.get('title')
            slug = re.sub(r'[^\w\s-]', '', title.lower())
            slug = re.sub(r'[-\s]+', '-', slug)
            
            post = BlogPost(
                title=request.form.get('title'),
                slug=slug,
                category=request.form.get('category'),
                author=request.form.get('author', OWNER_NAME),
                published_date=datetime.strptime(request.form.get('published_date'), '%Y-%m-%d').date() if request.form.get('published_date') else datetime.now().date(),
                featured_image=request.form.get('featured_image'),
                excerpt=request.form.get('excerpt'),
                content=request.form.get('content'),
                tags=request.form.get('tags'),
                seo_keywords=request.form.get('seo_keywords')
            )
            db.session.add(post)
            db.session.commit()
            flash('Blog post added successfully!', 'success')
            return redirect(url_for('admin_dashboard') + '#blog')
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding blog post: {str(e)}', 'danger')
    
    return render_template('admin/add_blog.html')

@app.route('/admin/blog/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_blog(id):
    post = BlogPost.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            post.title = request.form.get('title')
            post.category = request.form.get('category')
            post.author = request.form.get('author')
            if request.form.get('published_date'):
                post.published_date = datetime.strptime(request.form.get('published_date'), '%Y-%m-%d').date()
            post.featured_image = request.form.get('featured_image')
            post.excerpt = request.form.get('excerpt')
            post.content = request.form.get('content')
            post.tags = request.form.get('tags')
            post.seo_keywords = request.form.get('seo_keywords')
            post.updated_at = datetime.utcnow()
            db.session.commit()
            flash('Blog post updated successfully!', 'success')
            return redirect(url_for('admin_dashboard') + '#blog')
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating blog post: {str(e)}', 'danger')
    
    return render_template('admin/edit_blog.html', post=post)

@app.route('/admin/blog/delete/<int:id>')
@admin_required
def admin_delete_blog(id):
    try:
        post = BlogPost.query.get_or_404(id)
        db.session.delete(post)
        db.session.commit()
        flash('Blog post deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting blog post: {str(e)}', 'danger')
    
    return redirect(url_for('admin_blog'))

# ============================================
# FAQ MANAGEMENT
# ============================================

@app.route('/admin/faq')
@admin_required
def admin_faq():
    return redirect(url_for('admin_dashboard') + '#faq')

@app.route('/admin/faq/add', methods=['POST'])
@admin_required
def admin_add_faq():
    try:
        faq = FAQ(
            category=request.form.get('category'),
            question=request.form.get('question'),
            answer=request.form.get('answer'),
            order=int(request.form.get('order', 0))
        )
        db.session.add(faq)
        db.session.commit()
        flash('FAQ added successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding FAQ: {str(e)}', 'danger')
    
    return redirect(url_for('admin_dashboard') + '#faq')

@app.route('/admin/faq/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_faq(id):
    faq = FAQ.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            faq.category = request.form.get('category')
            faq.question = request.form.get('question')
            faq.answer = request.form.get('answer')
            faq.order = int(request.form.get('order', 0))
            db.session.commit()
            flash('FAQ updated successfully!', 'success')
            return redirect(url_for('admin_dashboard') + '#faq')
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating FAQ: {str(e)}', 'danger')
    
    return render_template('admin/edit_faq.html', faq=faq)

@app.route('/admin/faq/delete/<int:id>')
@admin_required
def admin_delete_faq(id):
    try:
        faq = FAQ.query.get_or_404(id)
        db.session.delete(faq)
        db.session.commit()
        flash('FAQ deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting FAQ: {str(e)}', 'danger')
    
    return redirect(url_for('admin_dashboard') + '#faq')

# ============================================
# SERVICES MANAGEMENT
# ============================================

@app.route('/admin/services')
@admin_required
def admin_services():
    return redirect(url_for('admin_dashboard') + '#services')

@app.route('/admin/services/add', methods=['POST'])
@admin_required
def admin_add_service():
    try:
        service = Service(
            name=request.form.get('name'),
            description=request.form.get('description'),
            icon=request.form.get('icon'),
            benefits=request.form.get('benefits')
        )
        db.session.add(service)
        db.session.commit()
        flash('Service added successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding service: {str(e)}', 'danger')
    
    return redirect(url_for('admin_services'))

@app.route('/admin/services/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_service(id):
    service = Service.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            service.name = request.form.get('name')
            service.description = request.form.get('description')
            service.icon = request.form.get('icon')
            service.benefits = request.form.get('benefits')
            db.session.commit()
            flash('Service updated successfully!', 'success')
            return redirect(url_for('admin_dashboard') + '#services')
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating service: {str(e)}', 'danger')
    
    return render_template('admin/edit_service.html', service=service)

@app.route('/admin/services/delete/<int:id>')
@admin_required
def admin_delete_service(id):
    try:
        service = Service.query.get_or_404(id)
        db.session.delete(service)
        db.session.commit()
        flash('Service deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting service: {str(e)}', 'danger')
    
    return redirect(url_for('admin_services'))

# ============================================
# MATERIALS MANAGEMENT
# ============================================

@app.route('/admin/materials')
@admin_required
def admin_materials():
    return redirect(url_for('admin_dashboard') + '#materials')

@app.route('/admin/materials/add', methods=['POST'])
@admin_required
def admin_add_material():
    try:
        uploaded_filename = None
        if 'material_file' in request.files:
            file = request.files['material_file']
            if file and file.filename and allowed_file(file.filename, 'image'):
                filename = secure_filename(file.filename)
                from time import time
                filename = f"{int(time())}_{filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'images', 'materials', 'types', filename)
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                file.save(filepath)
                uploaded_filename = filename

        images_val = uploaded_filename or request.form.get('images', '').strip()
        if not images_val:
            images_list = request.form.getlist('images')
            images_val = ','.join([x.strip() for x in images_list if x.strip()])
        material = Material(
            name=request.form.get('name'),
            type=request.form.get('type') or 'Marble',
            origin=request.form.get('origin'),
            characteristics=request.form.get('characteristics'),
            images=images_val,
            finishes=request.form.get('finishes'),
            best_use_cases=request.form.get('best_use_cases'),
            durability=request.form.get('durability'),
            price_range=request.form.get('price_range'),
            maintenance=request.form.get('maintenance'),
            description=request.form.get('description')
        )
        db.session.add(material)
        db.session.commit()
        flash('Material added successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding material: {str(e)}', 'danger')
    
    return redirect(url_for('admin_materials'))

@app.route('/admin/materials/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_material(id):
    material = Material.query.get_or_404(id)
    material_images = parse_json(material.images)
    
    if request.method == 'POST':
        try:
            material.name = request.form.get('name')
            material.type = request.form.get('type')
            material.origin = request.form.get('origin')
            material.characteristics = request.form.get('characteristics')
            
            # Direct file upload takes precedence
            if 'material_file' in request.files:
                file = request.files['material_file']
                if file and file.filename and allowed_file(file.filename, 'image'):
                    filename = secure_filename(file.filename)
                    from time import time
                    filename = f"{int(time())}_{filename}"
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'images', 'materials', 'types', filename)
                    os.makedirs(os.path.dirname(filepath), exist_ok=True)
                    file.save(filepath)
                    material.images = filename
                elif 'images' in request.form:
                    material.images = request.form.get('images', '').strip()
            elif 'images' in request.form:
                material.images = request.form.get('images', '').strip()

            material.finishes = request.form.get('finishes')
            material.best_use_cases = request.form.get('best_use_cases')
            material.durability = request.form.get('durability')
            material.price_range = request.form.get('price_range')
            material.maintenance = request.form.get('maintenance')
            material.description = request.form.get('description')
            db.session.commit()
            flash('Material updated successfully!', 'success')
            return redirect(url_for('admin_materials'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating material: {str(e)}', 'danger')
    
    return render_template('admin/edit_material.html', material=material, material_images=material_images)

@app.route('/admin/materials/delete/<int:id>')
@admin_required
def admin_delete_material(id):
    try:
        material = Material.query.get_or_404(id)
        db.session.delete(material)
        db.session.commit()
        flash('Material deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting material: {str(e)}', 'danger')
    
    return redirect(url_for('admin_materials'))

# ============================================
# CONTACT LEADS MANAGEMENT
# ============================================

@app.route('/admin/contacts')
@admin_required
def admin_contacts():
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/contacts/update-status/<int:id>', methods=['POST'])
@admin_required
def admin_update_contact_status(id):
    try:
        lead = ContactLead.query.get_or_404(id)
        lead.status = request.form.get('status')
        db.session.commit()
        flash('Contact status updated successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating status: {str(e)}', 'danger')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/contacts/delete/<int:id>')
@admin_required
def admin_delete_contact(id):
    try:
        lead = ContactLead.query.get_or_404(id)
        db.session.delete(lead)
        db.session.commit()
        flash('Contact deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting contact: {str(e)}', 'danger')
    
    return redirect(url_for('admin_dashboard'))

# ============================================
# ABOUT PAGE CONTENT MANAGEMENT
# ============================================

@app.route('/admin/about')
@admin_required
def admin_about():
    return redirect(url_for('admin_dashboard') + '#about')

@app.route('/admin/about/update', methods=['POST'])
@admin_required
def admin_update_about():
    try:
        about_description = request.form.get('about_description', '').strip()
        about_specialization = request.form.get('about_specialization', '').strip()
        projects_completed = request.form.get('projects_completed', '60').strip()
        residential_projects = request.form.get('residential_projects', '40').strip()
        commercial_projects = request.form.get('commercial_projects', '20').strip()
        years_experience = request.form.get('years_experience', '20+').strip()
        serving_text = request.form.get('serving_text', '').strip()
        
        # Check for photo upload
        if 'about_image' in request.files:
            file = request.files['about_image']
            if file and file.filename and allowed_file(file.filename, 'image'):
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'images', 'about', 'ashok-sharma.jpg')
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                file.save(filepath)

        set_setting('about_description', about_description, 'About page main description')
        set_setting('about_specialization', about_specialization, 'About page specialization text')
        set_setting('projects_completed', projects_completed, 'Total projects completed count')
        set_setting('residential_projects', residential_projects, 'Residential projects count')
        set_setting('commercial_projects', commercial_projects, 'Commercial projects count')
        set_setting('years_experience', years_experience, 'Years of experience')
        set_setting('serving_text', serving_text, 'Serving text for about page')
        
        flash('About page content and photo updated successfully!', 'success')
    except Exception as e:
        flash(f'Error updating about page: {str(e)}', 'danger')
    
    return redirect(url_for('admin_dashboard') + '#about')

# ============================================
# SETTINGS MANAGEMENT
# ============================================

@app.route('/admin/settings/update', methods=['POST'])
@admin_required
def admin_update_settings():
    try:
        telegram_bot_token = request.form.get('telegram_bot_token', '').strip()
        telegram_chat_id = request.form.get('telegram_chat_id', '').strip()
        
        set_setting('telegram_bot_token', telegram_bot_token, 'Telegram Bot Token from @BotFather')
        set_setting('telegram_chat_id', telegram_chat_id, 'Telegram Chat ID (individual or group)')
        
        flash('Settings updated successfully!', 'success')
    except Exception as e:
        flash(f'Error updating settings: {str(e)}', 'danger')
    
    return redirect(url_for('admin_dashboard') + '#settings')

@app.route('/admin/settings/test-telegram', methods=['POST'])
@admin_required
def admin_test_telegram():
    try:
        test_message = """
🧪 <b>Test Message</b>

✅ Your Telegram bot is configured correctly!

This is a test message from your website admin panel. If you received this, your Telegram integration is working perfectly.

⏰ <b>Time:</b> """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if send_telegram_message(test_message):
            return jsonify({'success': True, 'message': 'Test message sent successfully! Check your Telegram.'})
        else:
            return jsonify({'success': False, 'message': 'Failed to send test message. Please check your bot token and chat ID.'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

# API Routes
@app.route('/api/projects')
def api_projects():
    projects = Project.query.all()
    return jsonify([{
        'id': p.id,
        'title': p.title,
        'category': p.category,
        'location': p.location,
        'images': safe_json_loads(p.images, [])
    } for p in projects])

@app.route('/api/filter')
def api_filter():
    category = request.args.get('category', 'all')
    query = Project.query
    if category != 'all':
        query = query.filter(Project.category.contains(category))
    projects = query.all()
    return jsonify([{
        'id': p.id,
        'title': p.title,
        'category': p.category
    } for p in projects])

@app.route('/sitemap.xml')
def sitemap():
    """Generate sitemap.xml for SEO"""
    from flask import Response
    from datetime import datetime
    
    base_url = request.url_root.rstrip('/')
    
    # Get all dynamic URLs
    projects = Project.query.all()
    blog_posts = BlogPost.query.filter(BlogPost.published_date <= datetime.now().date()).all()
    
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>']
    sitemap.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    
    # Static pages
    static_pages = [
        ('', '1.0', 'daily'),
        ('/portfolio', '0.9', 'weekly'),
        ('/services', '0.9', 'monthly'),
        ('/materials', '0.9', 'monthly'),
        ('/about', '0.8', 'monthly'),
        ('/contact', '0.8', 'monthly'),
        ('/testimonials', '0.8', 'weekly'),
        ('/blog', '0.9', 'weekly'),
        ('/faq', '0.8', 'monthly'),
    ]
    
    for url, priority, changefreq in static_pages:
        sitemap.append(f'  <url>')
        sitemap.append(f'    <loc>{base_url}{url}</loc>')
        sitemap.append(f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>')
        sitemap.append(f'    <changefreq>{changefreq}</changefreq>')
        sitemap.append(f'    <priority>{priority}</priority>')
        sitemap.append(f'  </url>')
    
    # Project pages
    for project in projects:
        sitemap.append(f'  <url>')
        sitemap.append(f'    <loc>{base_url}{url_for("project_detail", project_id=project.id)}</loc>')
        sitemap.append(f'    <lastmod>{project.updated_at.strftime("%Y-%m-%d") if project.updated_at else datetime.now().strftime("%Y-%m-%d")}</lastmod>')
        sitemap.append(f'    <changefreq>monthly</changefreq>')
        sitemap.append(f'    <priority>0.8</priority>')
        sitemap.append(f'  </url>')
    
    # Blog posts
    for post in blog_posts:
        sitemap.append(f'  <url>')
        sitemap.append(f'    <loc>{base_url}{url_for("blog_post", post_id=post.id)}</loc>')
        sitemap.append(f'    <lastmod>{post.updated_at.strftime("%Y-%m-%d") if post.updated_at else (post.published_date.strftime("%Y-%m-%d") if post.published_date else datetime.now().strftime("%Y-%m-%d"))}</lastmod>')
        sitemap.append(f'    <changefreq>monthly</changefreq>')
        sitemap.append(f'    <priority>0.7</priority>')
        sitemap.append(f'  </url>')
    
    sitemap.append('</urlset>')
    
    return Response('\n'.join(sitemap), mimetype='application/xml')

@app.route('/robots.txt')
def robots():
    """Generate robots.txt for SEO"""
    from flask import Response
    robots_txt = f"""User-agent: *
Allow: /
Disallow: /admin/
Disallow: /api/

Sitemap: {request.url_root.rstrip('/')}/sitemap.xml
"""
    return Response(robots_txt, mimetype='text/plain')

# WebSocket Event Handlers
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    emit('connected', {'message': 'Connected to server'})
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print('Client disconnected')

@socketio.on('join_room')
def handle_join_room(data):
    """Join a room for notifications"""
    room = data.get('room', 'general')
    join_room(room)
    emit('joined_room', {'room': room, 'message': f'Joined {room} room'})

@socketio.on('leave_room')
def handle_leave_room(data):
    """Leave a room"""
    room = data.get('room', 'general')
    leave_room(room)
    emit('left_room', {'room': room})

@socketio.on('send_message')
def handle_message(data):
    """Handle chat messages"""
    message = data.get('message', '')
    username = data.get('username', 'Guest')
    room = data.get('room', 'general')
    
    # Broadcast message to room
    emit('new_message', {
        'username': username,
        'message': message,
        'timestamp': datetime.now().strftime('%H:%M:%S')
    }, room=room, broadcast=True)

@socketio.on('contact_form_submit')
def handle_contact_form(data):
    """Handle real-time contact form submission"""
    name = (data.get('name') or '').strip()
    email = (data.get('email') or '').strip()
    phone = (data.get('phone') or '').strip()
    project_type = data.get('project_type', '')
    location = data.get('location', '')
    budget_range = data.get('budget_range', '')
    message = (data.get('message') or '').strip()
    
    if not name or not email or not phone or not message:
        emit('form_submitted', {
            'success': False,
            'message': 'Please fill all required fields.'
        })
        return

    # Save to database
    try:
        lead = ContactLead(
            name=name,
            email=email,
            phone=phone,
            project_type=project_type,
            location=location,
            budget_range=budget_range,
            message=message,
            status='new'
        )
        db.session.add(lead)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error saving socket contact lead: {e}")

    # Send Telegram notification
    telegram_message = f"""
🔔 <b>New Contact Form Submission</b>

👤 <b>Name:</b> {name}
📧 <b>Email:</b> {email}
📱 <b>Phone:</b> {phone}
🏗️ <b>Project Type:</b> {project_type or 'Not specified'}
📍 <b>Location:</b> {location or 'Not specified'}
💰 <b>Budget Range:</b> {budget_range or 'Not specified'}

💬 <b>Message:</b>
{message}

⏰ <b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """
    send_telegram_message(telegram_message)

    # Send email notification if configured
    try:
        if app.config.get('MAIL_USERNAME'):
            msg = Message(
                subject=f'New Contact Form Submission - {name}',
                sender=app.config['MAIL_USERNAME'],
                recipients=[app.config['MAIL_USERNAME']],
                body=f"New lead from website:\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nProject Type: {project_type}\nLocation: {location}\nBudget: {budget_range}\n\nMessage:\n{message}"
            )
            mail.send(msg)
    except Exception as e:
        print(f"Socket lead email error: {e}")

    # Emit notification to admin room
    socketio.emit('new_lead', {
        'name': name,
        'email': email,
        'phone': phone,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }, room='admin', broadcast=True)
    
    # Send confirmation to client
    emit('form_submitted', {
        'success': True,
        'message': 'Thank you! Your message has been received. We will contact you soon!'
    })

@socketio.on('typing')
def handle_typing(data):
    """Handle typing indicator"""
    username = data.get('username', 'Guest')
    room = data.get('room', 'general')
    is_typing = data.get('typing', False)
    
    emit('user_typing', {
        'username': username,
        'typing': is_typing
    }, room=room, broadcast=True, include_self=False)

@socketio.on('request_quote')
def handle_quote_request(data):
    """Handle real-time quote requests"""
    project_type = data.get('project_type', 'Not specified')
    location = data.get('location', 'Not specified')
    name = (data.get('name') or 'Website Visitor').strip()
    email = (data.get('email') or '').strip()
    phone = (data.get('phone') or '').strip()
    message = data.get('message', f'Quote request for {project_type} in {location}')

    # Save to ContactLead in database
    try:
        lead = ContactLead(
            name=name,
            email=email or 'N/A',
            phone=phone or 'N/A',
            project_type=project_type,
            location=location,
            budget_range='Quote Request',
            message=message,
            status='new'
        )
        db.session.add(lead)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error saving socket quote lead: {e}")

    # Send Telegram notification for quote request
    telegram_message = f"""
🔔 <b>New Quote Request</b>

👤 <b>Name:</b> {name}
📧 <b>Email:</b> {email or 'Not specified'}
📱 <b>Phone:</b> {phone or 'Not specified'}
🏗️ <b>Project Type:</b> {project_type}
📍 <b>Location:</b> {location}

⏰ <b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """
    send_telegram_message(telegram_message)
    
    # Emit to admin
    socketio.emit('new_quote_request', {
        'project_type': project_type,
        'location': location,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }, room='admin', broadcast=True)
    
    emit('quote_requested', {
        'success': True,
        'message': 'Quote request received. Our team will contact you shortly.'
    })

@socketio.on('project_view')
def handle_project_view(data):
    """Track project views in real-time"""
    project_id = data.get('project_id')
    if project_id:
        emit('project_viewed', {
            'project_id': project_id,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }, room='admin', broadcast=True)

@socketio.on('notification_subscribe')
def handle_notification_subscribe(data):
    """Subscribe to notifications"""
    user_id = data.get('user_id', 'anonymous')
    join_room(f'user_{user_id}')
    emit('subscribed', {'message': 'Subscribed to notifications'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    print("\n" + "="*60)
    print("🚀 Balaji Marble Arts Website is Running!")
    print("="*60)
    print(f"\n📍 Access your website at:")
    print(f"   • http://localhost:5000")
    print(f"   • http://127.0.0.1:5000")
    print(f"\n💡 Press CTRL+C to stop the server")
    print("="*60 + "\n")
    
    # Run on localhost (127.0.0.1) to show local URLs in WSGI message
    socketio.run(app, debug=True, host='127.0.0.1', port=5000, allow_unsafe_werkzeug=True)

