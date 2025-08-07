from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import os
import json
from functools import wraps
import config

app = Flask(__name__)
app.secret_key = 'intelligent_career_advisor_key'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

# Create upload directory if it doesn't exist (only if not on Vercel)
if not os.environ.get('VERCEL'):
    os.makedirs('uploads', exist_ok=True)

# Predefined credentials for simple authentication
PREDEFINED_EMAIL = "admin@careeradvisor.com"
PREDEFINED_PASSWORD = "admin123"

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Simple predefined authentication
        if email == PREDEFINED_EMAIL and password == PREDEFINED_PASSWORD:
            session['user_id'] = 1
            session['email'] = email
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password. Use admin@careeradvisor.com / admin123', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/resume_parser', methods=['GET', 'POST'])
@login_required
def resume_parser_page():
    if request.method == 'POST':
        if 'resume' not in request.files:
            flash('No file selected', 'danger')
            return redirect(request.url)
        
        file = request.files['resume']
        if file.filename == '':
            flash('No file selected', 'danger')
            return redirect(request.url)
        
        if file:
            # Process the resume file
            try:
                import resume_parser
                result = resume_parser.parse_resume_file(file)
                return render_template('resume_parser_result.html', result=result)
            except Exception as e:
                flash(f'Error processing resume: {str(e)}', 'danger')
                return redirect(request.url)
    
    return render_template('resume_parser.html')

@app.route('/job_matcher', methods=['GET', 'POST'])
@login_required
def job_matcher_page():
    if request.method == 'POST':
        job_position = request.form.get('job_position', '')
        location = request.form.get('location', '')
        skills = request.form.get('skills', '')
        
        try:
            import job_matcher
            matches = job_matcher.find_job_matches(job_position, location, skills)
            return render_template('job_matcher.html', matches=matches, submitted=True)
        except Exception as e:
            flash(f'Error finding job matches: {str(e)}', 'danger')
    
    return render_template('job_matcher.html')

@app.route('/career_guidance', methods=['GET', 'POST'])
@login_required
def career_guidance_page():
    if request.method == 'POST':
        current_role = request.form.get('current_role', '')
        experience_years = request.form.get('experience_years', '')
        skills = request.form.get('skills', '')
        interests = request.form.get('interests', '')
        
        try:
            import career_guidance
            guidance = career_guidance.get_career_guidance(current_role, experience_years, skills, interests)
            return render_template('career_guidance.html', guidance=guidance, submitted=True)
        except Exception as e:
            flash(f'Error generating career guidance: {str(e)}', 'danger')
    
    return render_template('career_guidance.html')

@app.route('/interview_prep', methods=['GET', 'POST'])
@login_required
def interview_prep_page():
    if request.method == 'POST':
        job_role = request.form.get('job_role', '')
        experience_level = request.form.get('experience_level', '')
        
        try:
            import interview_prep
            questions = interview_prep.get_interview_questions(job_role, experience_level)
            return render_template('interview_prep.html', questions=questions, submitted=True)
        except Exception as e:
            flash(f'Error generating interview questions: {str(e)}', 'danger')
    
    return render_template('interview_prep.html')

@app.route('/interview_chatbot', methods=['GET', 'POST'])
@login_required
def interview_chatbot_page():
    if request.method == 'POST':
        message = request.form.get('message', '')
        job_role = request.form.get('job_role', 'Software Engineer')
        
        try:
            import interview_prep2
            response = interview_prep2.chat_with_interview_bot(message, job_role)
            return render_template('interview_chatbot.html', response=response, message=message)
        except Exception as e:
            flash(f'Error in chatbot: {str(e)}', 'danger')
    
    return render_template('interview_chatbot.html')

# API endpoints for AJAX calls
@app.route('/api/process_resume', methods=['POST'])
@login_required
def process_resume():
    try:
        data = request.get_json()
        resume_text = data.get('resume_text', '')
        
        import resume_parser
        result = resume_parser.parse_resume_text(resume_text)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/find_jobs', methods=['POST'])
@login_required
def find_jobs():
    try:
        data = request.get_json()
        job_position = data.get('job_position', '')
        location = data.get('location', '')
        skills = data.get('skills', '')
        
        import job_matcher
        matches = job_matcher.find_job_matches(job_position, location, skills)
        return jsonify(matches)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/career_guidance', methods=['POST'])
@login_required
def get_guidance():
    try:
        data = request.get_json()
        current_role = data.get('current_role', '')
        experience_years = data.get('experience_years', '')
        skills = data.get('skills', '')
        interests = data.get('interests', '')
        
        import career_guidance
        guidance = career_guidance.get_career_guidance(current_role, experience_years, skills, interests)
        return jsonify(guidance)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/interview_chat', methods=['POST'])
@login_required
def interview_chat():
    try:
        data = request.get_json()
        message = data.get('message', '')
        job_role = data.get('job_role', 'Software Engineer')
        
        import interview_prep2
        response = interview_prep2.chat_with_interview_bot(message, job_role)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 