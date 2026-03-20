import os
import logging

from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS

from routes.analyze import analyze_bp


# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def create_app() -> Flask:
    load_dotenv()

    app = Flask(__name__)
    
    # Enable Flask logging
    app.logger.setLevel(logging.DEBUG)

    # Restrict CORS to configured frontend origin in production,
    # and allow all localhost ports in development for flexibility
    allowed_origin = os.getenv("FRONTEND_ORIGIN", "*")
    flask_env = os.getenv("FLASK_ENV", "development")
    
    if flask_env == "development":
        # In development, allow all localhost variants for flexibility
        cors_resources = {r"/api/*": {
            "origins": [
                allowed_origin,
                "http://localhost:3000",
                "http://localhost:3001",
                "http://localhost:5173",
                "http://localhost:5174",
                "http://localhost:5175",
                "http://localhost:5176",
                "http://localhost:5177",
                "http://127.0.0.1:3000",
                "http://127.0.0.1:3001",
                "http://127.0.0.1:5173",
                "http://127.0.0.1:5174",
                "http://127.0.0.1:5175",
                "http://127.0.0.1:5176",
                "http://127.0.0.1:5177",
            ],
            "methods": ["GET", "POST", "OPTIONS", "PUT", "DELETE"],
            "allow_headers": ["Content-Type", "Authorization"]
        }}
    else:
        # In production, only allow configured frontend origin
        cors_resources = {r"/api/*": {"origins": allowed_origin}}
    
    CORS(app, resources=cors_resources)

    app.register_blueprint(analyze_bp, url_prefix="/api")

    @app.get("/api/health")
    def health_check():
        logger.info("Health check endpoint called")
        return jsonify({"status": "healthy", "message": "NewsGuard API is running"})

    return app


app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    debug = os.getenv("FLASK_ENV", "development") == "development"
    logger.info(f"Starting Flask app on port {port} with debug={debug}")
    app.run(host="0.0.0.0", port=port, debug=debug)
