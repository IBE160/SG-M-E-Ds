from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
import os
from routes import bp


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///default.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///:memory:"  # Use an in-memory SQLite for testing
    )


def create_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)

    engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
    Session = sessionmaker(bind=engine)
    session = Session()

    # Create tables if they don't exist
    Base.metadata.create_all(engine)

    # Attach session to app context for easy access
    app.session = session

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/game")
    def game_setup():
        return render_template("index.html")

    app.register_blueprint(bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
