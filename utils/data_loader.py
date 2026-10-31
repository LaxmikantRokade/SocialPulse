"""Data loading, cleaning, and validation module for SocialPulse."""

import os
import pandas as pd


REQUIRED_COLUMNS = [
    "platform",
    "post_date",
    "likes",
    "comments",
    "shares",
]

COLUMN_SYNONYMS = {
    "platform": ["platform", "channel", "social_media", "network"],
    "post_date": ["post_date", "date", "published_at", "publish_date", "created_at"],
    "post_type": ["post_type", "type", "content_type", "format", "media_type"],
    "caption": ["caption", "post_title", "title", "text", "description", "content"],
    "likes": ["likes", "like_count", "favorite_count", "reactions"],
    "comments": ["comments", "comment_count", "replies"],
    "shares": ["shares", "share_count", "retweets", "reposts"],
    "reach_or_views": [
        "reach_or_views",
        "reach",
        "views",
        "impressions",
        "view_count",
        "impression_count",
    ],
    "post_id": ["post_id", "id", "id_str"],
}


def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Map variations of column names to standard SocialPulse column names."""
    # Lowercase & strip column headers
    df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]

    rename_map = {}
    for standard_col, variations in COLUMN_SYNONYMS.items():
        if standard_col in df.columns:
            continue
        for v in variations:
            if v in df.columns:
                rename_map[v] = standard_col
                break

    if rename_map:
        df = df.rename(columns=rename_map)

    return df


def _standardize_platform(val: str) -> str:
    """Normalize platform casing to brand standard (Instagram, Facebook, YouTube)."""
    val_str = str(val).strip()
    val_lower = val_str.lower()
    if "insta" in val_lower:
        return "Instagram"
    elif "face" in val_lower or val_lower == "fb":
        return "Facebook"
    elif "you" in val_lower or val_lower == "yt":
        return "YouTube"
    return val_str.title()


def validate_and_clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Validate required columns, cast types, clean missing values, and calculate engagement rate."""
    if df.empty:
        raise ValueError("The uploaded CSV file contains no data rows.")

    df = normalize_column_names(df)

    # Check for core required columns
    missing_required = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing_required:
        raise ValueError(
            f"Missing required columns in CSV: {', '.join(missing_required)}. "
            "Please ensure your file has platform, post_date, likes, comments, and shares."
        )

    # Fill default optional columns if absent
    if "post_id" not in df.columns:
        df["post_id"] = [f"POST_{i+1:03d}" for i in range(len(df))]

    if "post_type" not in df.columns:
        df["post_type"] = "Post"

    if "caption" not in df.columns:
        df["caption"] = "Social Media Post"

    if "reach_or_views" not in df.columns:
        # Fallback estimation if reach is absent
        df["reach_or_views"] = (
            pd.to_numeric(df["likes"], errors="coerce").fillna(0)
            + pd.to_numeric(df["comments"], errors="coerce").fillna(0)
            + pd.to_numeric(df["shares"], errors="coerce").fillna(0)
        ) * 10

    # Clean text columns
    df["platform"] = df["platform"].apply(_standardize_platform)
    df["post_type"] = df["post_type"].astype(str).str.strip().str.title()
    df["caption"] = df["caption"].fillna("No Caption").astype(str)

    # Clean numeric columns with safe casting and zero fill
    numeric_cols = ["likes", "comments", "shares", "reach_or_views"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
        # Avoid negative numbers
        df[col] = df[col].apply(lambda x: max(0, int(round(x))))

    # Clean date column
    df["post_date"] = pd.to_datetime(df["post_date"], errors="coerce")
    # Drop records where date could not be parsed at all
    df = df.dropna(subset=["post_date"])
    if df.empty:
        raise ValueError("Could not parse any valid dates from the 'post_date' column.")

    # Calculate Total Engagement: Likes + Comments + Shares
    df["total_engagement"] = df["likes"] + df["comments"] + df["shares"]

    # Safe Engagement Rate (%) = (Total Engagement / Reach) * 100
    # Avoid division by zero
    def safe_engagement_rate(row):
        reach = row["reach_or_views"]
        if reach > 0:
            rate = (row["total_engagement"] / reach) * 100.0
            return round(rate, 2)
        return 0.0

    df["engagement_rate"] = df.apply(safe_engagement_rate, axis=1)

    # Sort chronologically by date
    df = df.sort_values(by="post_date", ascending=True).reset_index(drop=True)

    return df


def load_dataset(file_source=None) -> pd.DataFrame:
    """
    Load dataset from an uploaded file object or fallback to sample CSV.
    """
    if file_source is not None:
        try:
            df = pd.read_csv(file_source)
        except Exception as e:
            raise ValueError(f"Failed to read CSV file: {str(e)}")
    else:
        sample_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "data",
            "sample_social_media.csv",
        )
        if not os.path.exists(sample_path):
            raise FileNotFoundError(f"Sample dataset not found at {sample_path}")
        df = pd.read_csv(sample_path)

    return validate_and_clean_data(df)
