from datetime import datetime
from PIL import Image
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils import load_data, save_data
from flask import current_app
from flask import flash
import os

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('.login'))
    data = load_data()
    tasks = data['users'][session['username']]['tasks']
    return render_template('index.html', tasks=tasks)


# Set upload folder path
UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/upload_avatar', methods=['POST'])
def upload_avatar():
    if 'email' not in session:
        flash("You must be logged in to upload an avatar.", "danger")
        return redirect(url_for('main.login'))  # or wherever your login page is

    if 'avatar' not in request.files:
        flash('No file selected.', 'danger')
        return redirect(url_for('main.profile'))

    file = request.files['avatar']
    if file.filename == '':
        flash('No file selected.', 'warning')
        return redirect(url_for('main.profile'))

    if file and allowed_file(file.filename):
        # safe fallback if email has special characters
        safe_email = session['email'].replace('@', '_at_').replace('.', '_')
        ext = file.filename.rsplit('.', 1)[1].lower()
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        unique_name = f"{safe_email}_{timestamp}.{ext}"

        # Resize and save
        img = Image.open(file)
        img = img.convert("RGB")
        img = img.resize((150, 150))
        save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_name)
        img.save(save_path)

        # Update in JSON database
        users = load_data()['users']
        avatar = session['username']
        if avatar not in users:
            users[avatar] = {'avatar': None, 'email': session.get('email', ''), 'password': '', 'tasks': []}
        
        if avatar in users:
            old_avatar = users[avatar].get('avatar')
            if old_avatar:
                old_path = os.path.join(current_app.config['UPLOAD_FOLDER'], old_avatar)
                if os.path.exists(old_path):
                    os.remove(old_path)
            users[avatar]['avatar'] = unique_name
            save_data({'users': users})

        session['avatar'] = unique_name
        flash('Avatar uploaded successfully.', 'success')
        return redirect(url_for('main.profile'))

    else:
        flash('Invalid file type. Only JPG and PNG allowed.', 'danger')
        return redirect(url_for('main.profile'))


@main.route('/remove_avatar', methods=['POST'])
def remove_avatar():
    email = session.get('email')
    if not email:
        flash("Login required", "warning")
        return redirect(url_for('main.login'))

    users = load_data()['users']
    avatar = users.get('avatar')
    if avatar:
        avatar_path = os.path.join(current_app.config['UPLOAD_FOLDER'], avatar)
        if os.path.exists(avatar_path):
            os.remove(avatar_path)
        users['avatar'] = None
        save_data({'users': users})
        session.pop('avatar', None)
        flash('Avatar removed.', 'info')
    else:
        flash('No avatar to remove.', 'warning')

    return redirect(url_for('main.profile'))


@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_data()['users']
        if username in users and check_password_hash(users[username]['password'], password):
            session['email'] = users[username].get('email')
            session['avatar'] = users[username].get('avatar')
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('.index'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        users = load_data()['users']
        if username in users:
            flash('Username already exists', 'danger')
        else:
            users[username] = {'password': generate_password_hash(password), 'email': email, 'avatar': None, 'tasks': []}
            save_data({'users': users})
            flash('Sign up successful! You can now log in.', 'success')
            return redirect(url_for('.login'))
    return render_template('signup.html')


@main.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('.login'))  # Or your login route
    return render_template('profile.html', user=session['username'])


@main.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'info')
    return redirect(url_for('main.login'))

@main.route('/add', methods=['POST'])
def add():
    data = load_data()
    username = session['username']
    task_text = request.json.get('task')
    if task_text:
        task = {'content': task_text, 'completed': False, 'editing': False}
        data['users'][username]['tasks'].append(task)
        save_data(data)
    return '', 204

@main.route('/complete/<int:task_id>')
def complete(task_id):
    data = load_data()
    task = data['users'][session['username']]['tasks'][task_id]
    task['completed'] = not task['completed']
    save_data(data)
    return '', 204

@main.route('/delete/<int:task_id>')
def delete(task_id):
    data = load_data()
    data['users'][session['username']]['tasks'].pop(task_id)
    save_data(data)
    return '', 204

@main.route('/start_edit/<int:task_id>')
def start_edit(task_id):
    data = load_data()
    for i, t in enumerate(data['users'][session['username']]['tasks']):
        t['editing'] = (i == task_id)
    save_data(data)
    return '', 204

@main.route('/edit/<int:task_id>', methods=['POST'])
def edit(task_id):
    data = load_data()
    new_text = request.json.get('new_text')
    task = data['users'][session['username']]['tasks'][task_id]
    task['content'] = new_text
    task['editing'] = False
    save_data(data)
    return '', 204
