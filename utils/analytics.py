"""Analytics and metric computation utilities for SocialPulse."""

import pandas as pd


def calculate_overall_metrics(df: pd.DataFrame) -> dict:
    """Calculate high-level summary KPIs."""
    if df.empty:
        return {
            "total_posts": 0,
            "total_likes": 0,
            "total_comments": 0,
            "total_shares": 0,
            "total_reach": 0,
            "total_engagement": 0,
            "avg_engagement_rate": 0.0,
            "avg_likes_per_post": 0.0,
            "avg_comments_per_post": 0.0,
            "avg_shares_per_post": 0.0,
        }

    total_posts = int(len(df))
    total_likes = int(df["likes"].sum())
    total_comments = int(df["comments"].sum())
    total_shares = int(df["shares"].sum())
    total_reach = int(df["reach_or_views"].sum())
    total_engagement = int(df["total_engagement"].sum())

    # Overall Engagement Rate = (Total Engagements / Total Reach) * 100
    overall_engagement_rate = (
        (total_engagement / total_reach * 100.0) if total_reach > 0 else 0.0
    )

    avg_likes = total_likes / total_posts if total_posts > 0 else 0.0
    avg_comments = total_comments / total_posts if total_posts > 0 else 0.0
    avg_shares = total_shares / total_posts if total_posts > 0 else 0.0

    return {
        "total_posts": total_posts,
        "total_likes": total_likes,
        "total_comments": total_comments,
        "total_shares": total_shares,
        "total_reach": total_reach,
        "total_engagement": total_engagement,
        "avg_engagement_rate": round(overall_engagement_rate, 2),
        "avg_likes_per_post": round(avg_likes, 1),
        "avg_comments_per_post": round(avg_comments, 1),
        "avg_shares_per_post": round(avg_shares, 1),
    }


def get_platform_comparison(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate metrics grouped by social media platform."""
    if df.empty:
        return pd.DataFrame()

    platform_summary = (
        df.groupby("platform")
        .agg(
            posts=("post_id", "count"),
            likes=("likes", "sum"),
            comments=("comments", "sum"),
            shares=("shares", "sum"),
            reach=("reach_or_views", "sum"),
            total_engagement=("total_engagement", "sum"),
            avg_engagement_rate=("engagement_rate", "mean"),
        )
        .reset_index()
    )

    # Calculate platform-level overall engagement rate: sum(engagements)/sum(reach)*100
    platform_summary["overall_engagement_rate"] = platform_summary.apply(
        lambda r: round((r["total_engagement"] / r["reach"] * 100.0), 2)
        if r["reach"] > 0
        else 0.0,
        axis=1,
    )
    platform_summary["avg_engagement_rate"] = platform_summary[
        "avg_engagement_rate"
    ].round(2)

    return platform_summary


def get_post_type_comparison(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate metrics grouped by post type (e.g. Reel, Video, Carousel, Image)."""
    if df.empty:
        return pd.DataFrame()

    post_type_summary = (
        df.groupby("post_type")
        .agg(
            posts=("post_id", "count"),
            likes=("likes", "sum"),
            comments=("comments", "sum"),
            shares=("shares", "sum"),
            reach=("reach_or_views", "sum"),
            avg_engagement_rate=("engagement_rate", "mean"),
        )
        .reset_index()
    )

    post_type_summary["avg_engagement_rate"] = post_type_summary[
        "avg_engagement_rate"
    ].round(2)
    return post_type_summary.sort_values(by="posts", ascending=False)


def get_top_posts(
    df: pd.DataFrame, metric: str = "engagement_rate", top_n: int = 5
) -> pd.DataFrame:
    """Return top performing posts sorted by specified metric."""
    if df.empty:
        return pd.DataFrame()

    valid_metrics = [
        "engagement_rate",
        "likes",
        "comments",
        "shares",
        "reach_or_views",
        "total_engagement",
    ]
    if metric not in valid_metrics:
        metric = "engagement_rate"

    sorted_df = df.sort_values(by=metric, ascending=False).head(top_n)
    return sorted_df.reset_index(drop=True)


def get_timeline_data(df: pd.DataFrame, freq: str = "W") -> pd.DataFrame:
    """Group engagement metrics over time by Day or Week."""
    if df.empty:
        return pd.DataFrame()

    temp_df = df.copy()
    temp_df["post_date"] = pd.to_datetime(temp_df["post_date"])
    temp_df = temp_df.set_index("post_date")

    # Resample
    timeline = (
        temp_df.resample(freq)
        .agg(
            posts=("post_id", "count"),
            likes=("likes", "sum"),
            comments=("comments", "sum"),
            shares=("shares", "sum"),
            reach=("reach_or_views", "sum"),
            total_engagement=("total_engagement", "sum"),
        )
        .reset_index()
    )

    # Safe rate over time
    timeline["engagement_rate"] = timeline.apply(
        lambda r: round((r["total_engagement"] / r["reach"] * 100.0), 2)
        if r["reach"] > 0
        else 0.0,
        axis=1,
    )

    return timeline
