from flask import Flask, render_template, request, redirect, url_for, session
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Path where articles are stored
ARTICLES_DIR = "articles"

# Hardcoded admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password"

if not os.path.exists(ARTICLES_DIR):
    os.makedirs(ARTICLES_DIR)

# Load all articles
def load_articles():
    articles = []
    for filename in os.listdir(ARTICLES_DIR):
        if filename.endswith('.json'):
            with open(os.path.join(ARTICLES_DIR, filename), 'r') as file:
                articles.append(json.load(file))
    articles.sort(key=lambda x: x['date'], reverse=True)
    return articles

# Load a single article by filename
def load_article(filename):
    filepath = os.path.join(ARTICLES_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            return json.load(file)
    return None

# Helper function to save article
def save_article(title, content, date):
    article = {
        "title": title,
        "content": content,
        "date": date
    }
    
    filename = f"{date.replace('-', '')}_{title.replace(' ', '_').lower()}.json"
    
    with open(os.path.join(ARTICLES_DIR, filename), 'w') as file:
        json.dump(article, file, indent=4)

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials'), 401
    return render_template('login.html')

# Admin logout
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))

# Admin dashboard
@app.route('/admin/dashboard')
def admin_dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    articles = load_articles()
    return render_template('dashboard.html', articles=articles)

# Add article page
@app.route('/admin/add', methods=['GET', 'POST'])
def add_article():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        date = datetime.now().strftime('%Y-%m-%d')

        save_article(title, content, date)
        return redirect(url_for('admin_dashboard'))
    
    return render_template('add_article.html')

# Edit article page
@app.route('/admin/edit/<filename>', methods=['GET', 'POST'])
def edit_article(filename):
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    article_data = load_article(filename)
    if not article_data:
        return 'Article not found', 404

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        date = article_data['date']  # Keep the original date
        
        old_file_path = os.path.join(ARTICLES_DIR, filename)
        if os.path.exists(old_file_path):
            os.remove(old_file_path)

        save_article(title, content, date)
        
        return redirect(url_for('admin_dashboard'))
    
    return render_template('edit_article.html', article=article_data)

# Delete article
@app.route('/admin/delete/<filename>')
def delete_article(filename):
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    file_path = os.path.join(ARTICLES_DIR, filename)
    if os.path.exists(file_path):
        os.remove(file_path)

    return redirect(url_for('admin_dashboard'))

# Route for the home page
@app.route('/')
def home():
    articles = load_articles()
    return render_template('home.html', articles=articles)

# Route for an article page
@app.route('/article/<filename>')
def article(filename):
    article_data = load_article(filename)
    if not article_data:
        return 'Article not found', 404

    return render_template('article.html', article=article_data)

if __name__ == '__main__':
    app.run(debug=True)
