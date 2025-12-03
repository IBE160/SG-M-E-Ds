import os
import pytest

@pytest.fixture
def project_root():
    # Assuming tests are run from the ai-escape-app directory
    return os.path.dirname(os.path.abspath(__file__)) + "/../"

def test_project_directories_exist(project_root):
    expected_directories = [
        "static",
        "templates",
        "instance",
        "services",
        "tests",
        ".github/workflows"
    ]
    for directory in expected_directories:
        path = os.path.join(project_root, directory)
        assert os.path.isdir(path), f"Directory '{directory}' does not exist."

def test_project_files_exist(project_root):
    expected_files = [
        "app.py",
        "config.py",
        "models.py",
        "routes.py",
        "requirements.txt",
        ".env",
        ".flaskenv",
        "README.md",
        ".github/workflows/ci.yml"
    ]
    for file in expected_files:
        path = os.path.join(project_root, file)
        assert os.path.isfile(path), f"File '{file}' does not exist."

def test_readme_content_exists(project_root):
    readme_path = os.path.join(project_root, "README.md")
    assert os.path.isfile(readme_path), "README.md does not exist."
    with open(readme_path, "r") as f:
        content = f.read()
        assert "# AI Escape App" in content
        assert "A Python Flask application for an AI-driven escape room game." in content

def test_requirements_txt_content_exists(project_root):
    requirements_path = os.path.join(project_root, "requirements.txt")
    assert os.path.isfile(requirements_path), "requirements.txt does not exist."
    with open(requirements_path, "r") as f:
        content = f.read()
        assert "Flask" in content
        assert "python-dotenv" in content
        assert "gunicorn" in content
