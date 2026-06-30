import pandas as pd

from src.logger import logging


class RecommendationEngine:

    def __init__(self, dataframe):

        logging.info("Initializing Recommendation Engine")

        self.df = dataframe.copy()

        logging.info(f"Dataset loaded successfully with {self.df.shape[0]} rows.")

    def filter_branch(self, branch):

        logging.info(f"Filtering dataset for branch: {branch}")

        filtered_df = self.df[
            self.df["branch_name"] == branch
        ].copy()

        logging.info(
            f"Found {filtered_df.shape[0]} records for {branch}"
        )

        return filtered_df
    
    def filter_category(self, dataframe, category):

        logging.info(f"Filtering dataset for category: {category}")

        filtered_df = dataframe[
            dataframe["category"] == category
        ].copy()

        logging.info(
            f"Found {filtered_df.shape[0]} records for {category}"
        )

        return filtered_df

    def filter_year(self, dataframe, academic_year):

        logging.info(
            f"Filtering dataset for academic year: {academic_year}"
        )

        filtered_df = dataframe[
            dataframe["academic_year"] == academic_year
        ].copy()

        logging.info(
            f"Found {filtered_df.shape[0]} records for {academic_year}"
        )

        return filtered_df

    def classify(self, dataframe, percentile):

        logging.info(
            f"Classifying colleges for percentile: {percentile}"
        )

        df = dataframe.copy()

        df["difference"] = percentile - df["percentile"]

        def get_category(diff):

            if diff >= 1:
                return "Safe"

            elif diff >= -0.5:
                return "Target"

            else:
                return "Dream"

        df["chance"] = df["difference"].apply(get_category)

        logging.info("Classification completed.")

        return df

    def recommend(
        self,
        percentile,
        category,
        branch,
        academic_year=None
    ):

        logging.info("Recommendation started.")

        branch_df = self.filter_branch(branch)

        category_df = self.filter_category(
            branch_df,
        category
        )

        if academic_year is None:
            academic_year = self.df["academic_year"].max()

        logging.info(
            f"Using academic year: {academic_year}"
        )

        year_df = self.filter_year(
            category_df,
            academic_year
        )

        classified_df = self.classify(
            year_df,
            percentile
        )

        classified_df = self.remove_duplicates(
            classified_df
        )

        classified_df = self.rank_recommendations(
            classified_df
        )

        classified_df = self.add_confidence_score(
            classified_df
        )

        safe = classified_df[
            classified_df["chance"] == "Safe"
        ]

        target = classified_df[
            classified_df["chance"] == "Target"
        ]

        dream = classified_df[
            classified_df["chance"] == "Dream"
        ]

        top_recommendation = None

        if not safe.empty:
            top_recommendation = safe.iloc[0]

        elif not target.empty:
            top_recommendation = target.iloc[0]

        elif not dream.empty:
            top_recommendation = dream.iloc[0]

        logging.info("Recommendation generation completed.")

        return {
            "topRecommendation": top_recommendation,
            "safe": safe,
            "target": target,
            "dream": dream
        }

    def remove_duplicates(self, df):
        """
        Keep only one row for each College + Branch combination.
        Preference is given to the highest percentile cutoff.
        """

        logging.info("Removing duplicate college recommendations.")

        df = df.sort_values(
            by="percentile",
            ascending=False
        )

        df = df.drop_duplicates(
            subset=["college_code", "branch_code"],
            keep="first"
        )

        logging.info(
            f"Recommendations after duplicate removal: {len(df)}"
        )

        return df

    def rank_recommendations(self, df):
        """
        Rank recommendations based on chance and percentile difference.
        """

        logging.info("Ranking recommendations.")

        chance_priority = {
            "Safe": 1,
            "Target": 2,
            "Dream": 3
        }

        ranked_df = df.copy()

        ranked_df["chance_priority"] = ranked_df["chance"].map(
            chance_priority
        )

        ranked_df = ranked_df.sort_values(
            by=[
                "chance_priority",
                "difference"
            ],
            ascending=[
                True,
                False
            ]
        )

        ranked_df = ranked_df.drop(
            columns=["chance_priority"]
        )

        logging.info("Ranking completed.")

        return ranked_df

    def add_confidence_score(self, df):

        """
        Adds confidence score based on percentile difference.
        """

        logging.info("Calculating confidence score.")

        confidence_df = df.copy()

        def calculate(diff):

            if diff >= 3:
                return 99

            elif diff >= 2:
                return 97

            elif diff >= 1:
                return 92

            elif diff >= 0.5:
                return 85

            elif diff >= 0:
                return 75

            elif diff >= -0.5:
                return 65

            elif diff >= -1:
                return 50

            else:
                return 35

        confidence_df["confidence"] = confidence_df[
            "difference"
        ].apply(calculate)

        logging.info("Confidence score calculated.")

        return confidence_df