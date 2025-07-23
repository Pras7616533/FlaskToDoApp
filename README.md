# Flask To-Do App

A simple, modern To-Do List web application built with Flask. Users can register, log in, manage their tasks, and upload a profile avatar.

## Features

- User registration and authentication
- Add, edit, complete, and delete tasks
- Profile page with avatar upload and removal
- Data stored in a JSON file (no database required)
- Responsive UI with Bootstrap 5

## Project Structure

```
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── utils.py
│   ├── static/
│   │   ├── style.css
│   │   ├── default_avatar.png
│   │   └── uploads/
│   └── templates/
│       ├── base.html
│       ├── index.html
│       ├── login.html
│       ├── profile.html
│       └── signup.html
├── data/
│   └── data.json
├── run.py
├── requirements.txt
└── README.md
```

## Setup Instructions

1. **Clone the repository:**
   ```sh
   git clone <repo-url>
   cd FlaskToDoApp
   ```

2. **Create a virtual environment (optional but recommended):**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```sh
   python run.py
   ```

5. **Open your browser and go to:**
   ```
   http://127.0.0.1:5000/
   ```

## Notes

- Uploaded avatars are stored in `app/static/uploads/`.
- All user and task data is stored in `data/data.json`.
- Default secret key is set in [`app/__init__.py`](app/__init__.py); change it for production use.

## Requirements

- Python 3.8+
- See [`requirements.txt`](requirements.txt) for Python packages.