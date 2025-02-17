# Personal Blog Web App

## Overview
This is a simple blog application built with Flask. It allows users to view articles, while admins can manage (add, edit, delete) articles through a secure dashboard.

## Features
- **Home Page**: Displays a list of all articles in descending order by date.
- **Article Pages**: Each article can be viewed in full.
- **Admin Dashboard**: Admins can log in to manage articles (add, edit, delete).
- **Login System**: Admin login with a hardcoded username and password.

## Setup Instructions

### Step 1: Clone the Repository
```
git clone https://github.com/idorombaut/personal-blog-web-app.git
cd personal-blog-web-app
```

### Step 2: Set Up a Virtual Environment
1. **Create a Virtual Environment**
   ```
   python -m venv venv
   ```

2. **Activate the Virtual Environment**
   - **Windows**:
     ```
     .\venv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```
     source venv/bin/activate
     ```

3. **Install Dependencies**
   ```
   pip install Flask
   ```

### Step 3: Run the Application
```
python app.py
```

### Step 4: Access the Admin Panel
- Navigate to `http://127.0.0.1:5000/login` to log in as the admin.
- The hardcoded login credentials are:  
  Username: admin  
  Password: password
