from flask import Blueprint, request

from src.utils import validate_input

import pandas as pd

from src.components.recommendation_engine import RecommendationEngine
from src.config import MASTER_DATASET_PATH

df = pd.read_csv(MASTER_DATASET_PATH)

VALID_CATEGORIES = sorted(df["category"].unique().tolist())

VALID_BRANCHES = sorted(df["branch_name"].unique().tolist())

engine = RecommendationEngine(df)

recommendation_bp = Blueprint(
    "recommendation",
    __name__
)


@recommendation_bp.route("/recommend", methods=["POST"])
def recommend():

    try:

        data = request.get_json()

        validate_input(
            percentile=data["percentile"],
            category=data["category"],
            branch=data["branch"],
            academic_year=data.get("academic_year"),
            valid_categories=VALID_CATEGORIES,
            valid_branches=VALID_BRANCHES
        )

        result = engine.recommend(
            percentile=data["percentile"],
            category=data["category"],
            branch=data["branch"],
            academic_year=data.get("academic_year")
        )

        return {
            "topRecommendation":
                result["topRecommendation"].to_dict()
                if result["topRecommendation"] is not None
                else None,

            "safe":
                result["safe"].to_dict(orient="records"),

            "target":
                result["target"].to_dict(orient="records"),

            "dream":
                result["dream"].to_dict(orient="records")
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }, 400