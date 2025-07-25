from flask import Flask, render_template, request, redirect, session, url_for
from models import db, User  # Moved User and db to models.py
from weed import weed_bp
from plantdisease import plant_disease_bp as plant_bp
from water import cropwater_bp
import bcrypt
import pdfkit

app = Flask(__name__)
app.secret_key = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)  # Initialize db with app

# Create DB
with app.app_context():
    db.create_all()

# Register Blueprints
app.register_blueprint(weed_bp)
app.register_blueprint(plant_bp)
app.register_blueprint(cropwater_bp)

# Routes
@app.route('/')
def intro_page():
    return render_template('intro_index.html')

@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session['email'] = user.email
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid email or password. Please try again or register.")
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return render_template('register.html', error="Email already registered. Please login.")

        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'email' in session:
        user = User.query.filter_by(email=session['email']).first()
        return render_template('dashboard.html', user=user)
    return redirect(url_for('login'))

@app.route('/weed_index')
def weed_index():
    if 'email' in session:
        user = User.query.filter_by(email=session['email']).first()
        return render_template('weed_index.html', user=user)
    return redirect(url_for('login'))

@app.route('/crophealth')
def crophealth():
    if 'email' in session:
        user = User.query.filter_by(email=session['email']).first()
        return render_template('crophealth.html', user=user)
    return redirect(url_for('login'))

@app.route('/water_index')
def water_index():
    if 'email' in session:
        user = User.query.filter_by(email=session['email']).first()
        return render_template('water_index.html', user=user)
    return redirect(url_for('login'))

@app.route('/water_result')
def water_result():
    if 'email' in session:
        user = User.query.filter_by(email=session['email']).first()
        return render_template('water_result.html', user=user)
    return redirect(url_for('login'))

@app.route('/weed_result')
def weed_result():
    if 'email' in session:
        user = User.query.filter_by(email=session['email']).first()
        return render_template('weed_result.html', user=user)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))

@app.context_processor
def inject_user():
    if 'email' in session:
        user = User.query.filter_by(email=session['email']).first()
        return dict(user=user)
    return dict(user=None)


# Start server
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
