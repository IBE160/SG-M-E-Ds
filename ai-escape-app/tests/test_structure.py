import os

# Define the root directory of the project
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
AI_ESCAPE_APP_DIR = os.path.join(PROJECT_ROOT, "ai-escape-app")


def test_project_root_exists():
    assert os.path.isdir(PROJECT_ROOT)


def test_ai_escape_app_directory_exists():
    assert os.path.isdir(AI_ESCAPE_APP_DIR)


def test_venv_directory_exists():
    venv_path = os.path.join(PROJECT_ROOT, "venv")
    assert os.path.isdir(venv_path)


def test_essential_app_directories_exist():
    expected_dirs = [
        os.path.join(AI_ESCAPE_APP_DIR, "static"),
        os.path.join(AI_ESCAPE_APP_DIR, "templates"),
        os.path.join(AI_ESCAPE_APP_DIR, "instance"),
        os.path.join(AI_ESCAPE_APP_DIR, "services"),
        os.path.join(AI_ESCAPE_APP_DIR, "tests"),
    ]
    for d in expected_dirs:
        assert os.path.isdir(d), f"Missing directory: {d}"


def test_essential_app_files_exist():
    expected_files = [
        os.path.join(AI_ESCAPE_APP_DIR, "app.py"),
        os.path.join(AI_ESCAPE_APP_DIR, "config.py"),
        os.path.join(AI_ESCAPE_APP_DIR, ".env"),
        os.path.join(AI_ESCAPE_APP_DIR, "requirements.txt"),
        os.path.join(AI_ESCAPE_APP_DIR, ".flaskenv"),
    ]
    for f in expected_files:
        assert os.path.isfile(f), f"Missing file: {f}"
