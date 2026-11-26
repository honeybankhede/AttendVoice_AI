from flask import Flask, jsonify, render_template
from config import Config
from database.db import db, migrate
from backend.health import health_bp

def create_app():
    app = Flask(__name__, template_folder="frontend/templates",
                static_folder="frontend/static")
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Import models so Flask-Migrate can discover their metadata.
    from database import models  # noqa: F401

    app.register_blueprint(health_bp)

    @app.get("/")
    def index():
        return render_template(
    "index.html",
    college=app.config["COLLEGE_NAME"]
)

    @app.errorhandler(404)
    def not_found(_error):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def server_error(_error):
        return jsonify({"error": "Internal server error"}), 500

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=app.config["DEBUG"])
