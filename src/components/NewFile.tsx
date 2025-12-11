#!/bin/bash

PROJECT_NAME="ai_code_review_backend"
VENV_NAME="venv"
PYTHON_VERSION="python3" # Or python, depending on system configuration

echo "--- Backend Project Initialization Script ---"

# 1. Create project directory
echo "Creating project directory: $PROJECT_NAME"
mkdir -p "$PROJECT_NAME"
cd "$PROJECT_NAME"

# 2. Create virtual environment
echo "Creating virtual environment: $VENV_NAME"
"$PYTHON_VERSION" -m venv "$VENV_NAME"

# 3. Activate virtual environment (for the script's scope)
echo "Activating virtual environment..."
source "$VENV_NAME/bin/activate"

# 4. Install basic dependencies
echo "Installing basic dependencies: Flask, gunicorn, python-dotenv"
pip install Flask gunicorn python-dotenv

# 5. Create a basic Flask application file
echo "Creating a basic 'app.py'...
"
cat << EOF > app.py
from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from AI-Powered Code Review Backend!'

@app.route('/health')
def health_check():
    return {'status': 'ok'}

if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
EOF

# 6. Create requirements.txt
echo "Generating requirements.txt"
pip freeze > requirements.txt

# 7. Create .gitignore file
echo "Creating .gitignore file"
cat << EOF > .gitignore
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
*.egg-info/
.env

# Editor-specific (common)
.vscode/
.idea/
*.sublime-project
*.sublime-workspace

# Logs and databases
*.log
*.sqlite3
*.db

# OS generated files
.DS_Store
Thumbs.db
EOF

# 8. Initialize git repository
echo "Initializing Git repository"
git init

# 9. Make initial commit
echo "Making initial commit"
git add .
git commit -m "feat: Initial backend project setup with Flask and venv"

echo "--- Project initialization complete! ---"
echo "To activate your virtual environment: source $VENV_NAME/bin/activate"
echo "To run the Flask app: flask run"
echo "Or using gunicorn: gunicorn -w 4 'app:app'"
echo "Deactivating virtual environment for current shell session."
deactivate
