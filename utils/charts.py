"""Interactive Plotly chart generation module for SocialPulse."""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Brand and accent colors
PLATFORM_COLORS = {
    "Instagram": "#E1306C",
    "Facebook": "#1877F2",
    "YouTube": "#FF0000",
}

THEME_LAYOUT = dict(
    font=dict(family="sans-serif", size=12, color="#2D3436"),
    margin=dict(l=40, r=40, t=50, b=40),
    plot_bgcolor="rgba(248, 249, 250, 0.5)",
    paper_bgcolor="rgba(0,0,0,0)",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
    ),
)


def plot_platform_comparison_bars(platform_df: pd.DataFrame) -> go.Figure:
    """Grouped bar chart comparing Total Likes, Comments, and Shares across platforms."""
    fig = go.Figure()

    if platform_df.empty:
        return fig

    fig.add_trace(
        go.Bar(
            name="Likes",
            x=platform_df["platform"],
            y=platform_df["likes"],
            marker_color="#6C5CE7",
            text=platform_df["likes"].apply(lambda x: f"{x:,}"),
            textposition="auto",
        )
    )
    fig.add_trace(
        go.Bar(
            name="Comments",
            x=platform_df["platform"],
            y=platform_df["comments"],
            marker_color="#00CEC9",
            text=platform_df["comments"].apply(lambda x: f"{x:,}"),
            textposition="auto",
        )
    )
    fig.add_trace(
        go.Bar(
            name="Shares",
            x=platform_df["platform"],
            y=platform_df["shares"],
            marker_color="#FD79A8",
            text=platform_df["shares"].apply(lambda x: f"{x:,}"),
            textposition="auto",
        )
    )

    fig.update_layout(
        title="<b>Total Interactions by Platform</b>",
        barmode="group",
        yaxis_title="Total Count",
        xaxis_title="",
        **THEME_LAYOUT,
    )
    return fig


def plot_platform_share_donut(platform_df: pd.DataFrame, metric: str = "total_engagement") -> go.Figure:
    """Donut chart showing platform share for a given metric."""
    if platform_df.empty or metric not in platform_df.columns:
        return go.Figure()

    metric_labels = {
        "total_engagement": "Total Engagement",
        "likes": "Likes Share",
        "reach": "Audience Reach",
        "posts": "Content Volume (Posts)",
    }
    label = metric_labels.get(metric, metric.replace("_", " ").title())

    colors = [PLATFORM_COLORS.get(p, "#636E72") for p in platform_df["platform"]]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=platform_df["platform"],
                values=platform_df[metric],
                hole=0.55,
                marker=dict(colors=colors),
                textinfo="label+percent",
                hoverinfo="label+value+percent",
            )
        ]
    )

    fig.update_layout(
        title=f"<b>Platform Share: {label}</b>",
        showlegend=True,
        **THEME_LAYOUT,
    )
    return fig


def plot_engagement_rate_comparison(platform_df: pd.DataFrame) -> go.Figure:
    """Bar chart comparing average engagement rate per platform."""
    if platform_df.empty:
        return go.Figure()

    colors = [PLATFORM_COLORS.get(p, "#6C5CE7") for p in platform_df["platform"]]

    fig = go.Figure(
        data=[
            go.Bar(
                x=platform_df["platform"],
                y=platform_df["overall_engagement_rate"],
                marker_color=colors,
                text=platform_df["overall_engagement_rate"].apply(lambda x: f"{x:.2f}%"),
                textposition="outside",
            )
        ]
    )

    fig.update_layout(
        title="<b>Overall Engagement Rate (%) by Platform</b>",
        yaxis_title="Engagement Rate (%)",
        xaxis_title="",
        **THEME_LAYOUT,
    )
    return fig


def plot_timeline_trends(timeline_df: pd.DataFrame) -> go.Figure:
    """Timeline trend line chart for interactions over time."""
    fig = go.Figure()

    if timeline_df.empty:
        return fig

    fig.add_trace(
        go.Scatter(
            x=timeline_df["post_date"],
            y=timeline_df["likes"],
            mode="lines+markers",
            name="Likes",
            line=dict(color="#6C5CE7", width=2.5),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=timeline_df["post_date"],
            y=timeline_df["comments"],
            mode="lines+markers",
            name="Comments",
            line=dict(color="#00B894", width=2),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=timeline_df["post_date"],
            y=timeline_df["shares"],
            mode="lines+markers",
            name="Shares",
            line=dict(color="#E84393", width=2),
        )
    )

    fig.update_layout(
        title="<b>Engagement Trends Over Time</b>",
        xaxis_title="Date",
        yaxis_title="Count",
        hovermode="x unified",
        **THEME_LAYOUT,
    )
    return fig


def plot_post_type_performance(post_type_df: pd.DataFrame) -> go.Figure:
    """Horizontal bar chart comparing engagement rate across content types."""
    if post_type_df.empty:
        return go.Figure()

    fig = px.bar(
        post_type_df,
        x="avg_engagement_rate",
        y="post_type",
        orientation="h",
        color="avg_engagement_rate",
        color_continuous_scale="Purples",
        text=post_type_df["avg_engagement_rate"].apply(lambda x: f"{x:.2f}%"),
        labels={
            "avg_engagement_rate": "Avg Engagement Rate (%)",
            "post_type": "Post Format",
        },
    )

    fig.update_layout(
        title="<b>Content Format vs. Average Engagement Rate</b>",
        coloraxis_showscale=False,
        yaxis=dict(categoryorder="total ascending"),
        **THEME_LAYOUT,
    )
    fig.update_traces(textposition="outside")
    return fig


def plot_reach_vs_engagement(df: pd.DataFrame) -> go.Figure:
    """Scatter plot: Reach vs. Total Engagement with Platform coloring."""
    if df.empty:
        return go.Figure()

    fig = px.scatter(
        df,
        x="reach_or_views",
        y="total_engagement",
        color="platform",
        color_discrete_map=PLATFORM_COLORS,
        size="engagement_rate",
        hover_data=["post_id", "post_type", "caption", "engagement_rate"],
        labels={
            "reach_or_views": "Reach / Views",
            "total_engagement": "Total Engagements",
            "platform": "Platform",
            "engagement_rate": "Engagement Rate (%)",
        },
    )

    fig.update_layout(
        title="<b>Reach vs. Engagement Scatter Analysis</b>",
        **THEME_LAYOUT,
    )
    return fig
