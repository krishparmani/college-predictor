from flask import Flask

from application.routes.recommendation import recommendation_bp

app = Flask(__name__)

app.register_blueprint(recommendation_bp)


@app.route("/")
def home():
    return "MHT CET Predictor Backend is Running 🚀"

@app.route("/health")
def health():

    return {
        "status": "healthy",
        "message": "MHT CET Predictor API is running."
    }


if __name__ == "__main__":
    app.run(debug=True)