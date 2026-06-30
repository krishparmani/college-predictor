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