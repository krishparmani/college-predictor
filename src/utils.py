VALID_YEARS = [
    "2023-2024",
    "2024-2025",
    "2025-2026"
]


def validate_input(
    percentile,
    category,
    branch,
    academic_year,
    valid_categories,
    valid_branches
):
    if percentile < 0 or percentile > 100:
        raise ValueError(
            "Percentile must be between 0 and 100."
        )

    if not isinstance(category, str) or not category.strip():
        raise ValueError(
            "Category is required."
        )

    if not isinstance(branch, str) or not branch.strip():
        raise ValueError(
            "Branch is required."
        )

    if academic_year is not None and academic_year not in valid_academic_years:
        raise ValueError(
            f"Academic year must be one of {valid_academic_years}"
        )

    if category not in valid_categories:
        raise ValueError(
            f"Invalid category: {category}"
        )

    if branch not in valid_branches:
        raise ValueError(
            f"Invalid branch: {branch}"
        )