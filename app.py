"""SocialPulse – Social Media Data Analytics Dashboard
A modern, lightweight Python analytics application built with Streamlit, Pandas, and Plotly.
Deployable on Streamlit Community Cloud.
"""

import os
import streamlit as st
import pandas as pd

from utils.data_loader import load_dataset
from utils.analytics import (
    calculate_overall_metrics,
    get_platform_comparison,
    get_post_type_comparison,
    get_top_posts,
    get_timeline_data,
)
from utils.charts import (
    plot_platform_comparison_bars,
    plot_platform_share_donut,
    plot_engagement_rate_comparison,
    plot_timeline_trends,
    plot_post_type_performance,
    plot_reach_vs_engagement,
)

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="SocialPulse – Social Media Analytics",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- MODERN STYLING (CSS) ---
st.markdown(
    """
    <style>
    /* Metric card styling */
    div[data-testid="stMetric"] {
        background-color: #F8F9FA;
        border: 1px solid #E9ECEF;
        padding: 14px 18px;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    div[data-testid="stMetric"]:hover {
        border-color: #6C5CE7;
        box-shadow: 0 4px 12px rgba(108, 92, 231, 0.1);
        transition: all 0.2s ease-in-out;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        color: #636E72 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.7rem !important;
        font-weight: 700 !important;
        color: #2D3436 !important;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 18px;
        border-radius: 8px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #F0EDFD !important;
        color: #6C5CE7 !important;
    }

    /* Badges */
    .badge {
        display: inline-block;
        padding: 4px 10px;
        font-size: 0.8rem;
        font-weight: 600;
        border-radius: 6px;
        margin-right: 6px;
    }
    .badge-ig { background-color: #FCE4EC; color: #C2185B; }
    .badge-fb { background-color: #E3F2FD; color: #1565C0; }
    .badge-yt { background-color: #FFEBEE; color: #C62828; }
    .badge-default { background-color: #EDE7F6; color: #512DA8; }
    </style>
    """,
    unsafe_allow_html=True,
)


def get_platform_badge(platform: str) -> str:
    """Return an HTML badge for a platform."""
    p_lower = str(platform).lower()
    if "insta" in p_lower:
        return f'<span class="badge badge-ig">📸 {platform}</span>'
    elif "face" in p_lower:
        return f'<span class="badge badge-fb">👥 {platform}</span>'
    elif "you" in p_lower:
        return f'<span class="badge badge-yt">▶️ {platform}</span>'
    return f'<span class="badge badge-default">🌐 {platform}</span>'


# --- SIDEBAR: DATA SOURCE & FILTERS ---
with st.sidebar:
    st.markdown("## ⚡ **SocialPulse**")
    st.caption("Social Media Performance & Analytics Engine")
    st.markdown("---")

    st.subheader("📂 Data Source")
    data_source = st.radio(
        "Select Dataset:",
        options=["Sample Dataset", "Upload CSV File"],
        index=0,
        help="Use the pre-packaged 250+ row demo dataset or upload your own CSV file.",
    )

    uploaded_file = None
    if data_source == "Upload CSV File":
        uploaded_file = st.file_uploader(
            "Upload Social Media CSV",
            type=["csv"],
            help="Expected columns: platform, post_date, likes, comments, shares, reach_or_views, post_type, caption",
        )

    # Allow downloading the sample dataset template
    sample_csv_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "data", "sample_social_media.csv"
    )
    if os.path.exists(sample_csv_path):
        with open(sample_csv_path, "rb") as f:
            st.download_button(
                label="📥 Download Sample CSV Template",
                data=f.read(),
                file_name="socialpulse_sample_data.csv",
                mime="text/csv",
                help="Download sample CSV to inspect schema or edit your own data.",
            )

    st.markdown("---")


# --- DATA LOADING ---
try:
    if data_source == "Upload CSV File" and uploaded_file is not None:
        raw_df = load_dataset(uploaded_file)
        active_source_label = f"Uploaded File: `{uploaded_file.name}`"
    else:
        raw_df = load_dataset(None)
        active_source_label = "Pre-loaded Sample Dataset"
except Exception as e:
    st.error(f"⚠️ Error loading dataset: {str(e)}")
    st.info(
        "💡 Tip: Ensure your CSV has columns like `platform`, `post_date`, `likes`, `comments`, `shares`, and `reach_or_views`."
    )
    st.stop()


# --- SIDEBAR FILTERS ---
with st.sidebar:
    st.subheader("🔍 Filter Data")

    # Date range filter
    min_date = raw_df["post_date"].min().date()
    max_date = raw_df["post_date"].max().date()

    selected_date_range = st.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    # Platform filter
    all_platforms = sorted(raw_df["platform"].unique().tolist())
    selected_platforms = st.multiselect(
        "Select Platforms",
        options=all_platforms,
        default=all_platforms,
    )

    # Post type filter
    all_post_types = sorted(raw_df["post_type"].unique().tolist())
    selected_post_types = st.multiselect(
        "Select Post Formats",
        options=all_post_types,
        default=all_post_types,
    )

    st.markdown("---")
    st.caption("💡 SocialPulse Analytics v1.0 | Streamlit Mini Project")


# --- APPLY FILTERS ---
filtered_df = raw_df.copy()

# Filter by platforms
if selected_platforms:
    filtered_df = filtered_df[filtered_df["platform"].isin(selected_platforms)]
else:
    filtered_df = filtered_df.iloc[0:0]

# Filter by post types
if selected_post_types:
    filtered_df = filtered_df[filtered_df["post_type"].isin(selected_post_types)]
else:
    filtered_df = filtered_df.iloc[0:0]

# Filter by date range safely
if isinstance(selected_date_range, (tuple, list)) and len(selected_date_range) == 2:
    start_d, end_d = selected_date_range
    filtered_df = filtered_df[
        (filtered_df["post_date"].dt.date >= start_d)
        & (filtered_df["post_date"].dt.date <= end_d)
    ]


# --- TOP HEADER & METRIC SUMMARY ---
st.title("⚡ SocialPulse – Social Media Analytics")
st.markdown(
    f"Comprehensive performance analytics and cross-platform benchmarking • **{active_source_label}**"
)

# Empty data guard
if filtered_df.empty:
    st.warning("⚠️ No data matches your active filter selection. Please broaden the sidebar filters.")
    st.stop()

# Overall metrics
overall_metrics = calculate_overall_metrics(filtered_df)

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Posts", f"{overall_metrics['total_posts']:,}")
col2.metric("Total Likes", f"{overall_metrics['total_likes']:,}")
col3.metric("Total Comments", f"{overall_metrics['total_comments']:,}")
col4.metric("Total Shares", f"{overall_metrics['total_shares']:,}")
col5.metric(
    "Avg Engagement Rate",
    f"{overall_metrics['avg_engagement_rate']:.2f}%",
    help="Formula: (Total Likes + Comments + Shares) / Total Reach * 100",
)

# Secondary row of quick metrics
m_col1, m_col2, m_col3, m_col4 = st.columns(4)
with m_col1:
    st.caption(f"👀 **Total Reach / Views:** {overall_metrics['total_reach']:,}")
with m_col2:
    st.caption(f"👍 **Avg Likes / Post:** {overall_metrics['avg_likes_per_post']:,}")
with m_col3:
    st.caption(f"💬 **Avg Comments / Post:** {overall_metrics['avg_comments_per_post']:,}")
with m_col4:
    st.caption(f"🔄 **Avg Shares / Post:** {overall_metrics['avg_shares_per_post']:,}")

st.markdown("---")


# --- DASHBOARD TABS ---
tab_overview, tab_platforms, tab_formats, tab_top_posts, tab_raw_data = st.tabs(
    [
        "📈 Overview & Trends",
        "⚖️ Platform Comparison",
        "📱 Content Format Analysis",
        "🏆 Top-Performing Posts",
        "📋 Data & Export",
    ]
)

# --- TAB 1: OVERVIEW & TRENDS ---
with tab_overview:
    st.subheader("Engagement Trends Over Time")

    trend_col1, trend_col2 = st.columns([1, 4])
    with trend_col1:
        granularity = st.radio(
            "Grouping Frequency:",
            options=["Weekly", "Daily"],
            index=0,
            horizontal=False,
        )
    with trend_col2:
        freq_code = "W" if granularity == "Weekly" else "D"
        timeline_df = get_timeline_data(filtered_df, freq=freq_code)
        fig_timeline = plot_timeline_trends(timeline_df)
        st.plotly_chart(fig_timeline, use_container_width=True)

    st.markdown("---")
    st.subheader("Audience Reach vs. Engagement Correlation")
    st.caption("Bubble size indicates Engagement Rate (%). Hover over individual bubbles for post details.")
    fig_scatter = plot_reach_vs_engagement(filtered_df)
    st.plotly_chart(fig_scatter, use_container_width=True)


# --- TAB 2: PLATFORM COMPARISON ---
with tab_platforms:
    st.subheader("Cross-Platform Benchmarks: Instagram vs Facebook vs YouTube")

    platform_summary_df = get_platform_comparison(filtered_df)

    p_col1, p_col2 = st.columns(2)
    with p_col1:
        fig_bar = plot_platform_comparison_bars(platform_summary_df)
        st.plotly_chart(fig_bar, use_container_width=True)

    with p_col2:
        donut_metric = st.selectbox(
            "Share Distribution Metric:",
            options=["total_engagement", "likes", "reach", "posts"],
            format_func=lambda x: {
                "total_engagement": "Total Engagement (Likes + Comments + Shares)",
                "likes": "Total Likes",
                "reach": "Audience Reach / Views",
                "posts": "Number of Posts Published",
            }.get(x, x),
        )
        fig_donut = plot_platform_share_donut(platform_summary_df, metric=donut_metric)
        st.plotly_chart(fig_donut, use_container_width=True)

    st.markdown("---")

    p_col3, p_col4 = st.columns([1, 1])
    with p_col3:
        fig_rates = plot_engagement_rate_comparison(platform_summary_df)
        st.plotly_chart(fig_rates, use_container_width=True)

    with p_col4:
        st.markdown("#### 📊 **Platform Summary Table**")
        display_platform_df = platform_summary_df.copy()
        display_platform_df.columns = [
            "Platform",
            "Posts",
            "Likes",
            "Comments",
            "Shares",
            "Reach / Views",
            "Total Engagement",
            "Avg Rate (%)",
            "Overall Rate (%)",
        ]
        st.dataframe(
            display_platform_df.style.format(
                {
                    "Posts": "{:,}",
                    "Likes": "{:,}",
                    "Comments": "{:,}",
                    "Shares": "{:,}",
                    "Reach / Views": "{:,}",
                    "Total Engagement": "{:,}",
                    "Avg Rate (%)": "{:.2f}%",
                    "Overall Rate (%)": "{:.2f}%",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )


# --- TAB 3: CONTENT FORMAT ANALYSIS ---
with tab_formats:
    st.subheader("Content Format Performance Analysis")
    st.caption("Identify which post format (Reels, Videos, Carousels, Images) drives higher engagement.")

    post_type_summary = get_post_type_comparison(filtered_df)

    f_col1, f_col2 = st.columns([1, 1])
    with f_col1:
        fig_formats = plot_post_type_performance(post_type_summary)
        st.plotly_chart(fig_formats, use_container_width=True)

    with f_col2:
        st.markdown("#### 💡 **Format Insights**")
        if not post_type_summary.empty:
            best_format = post_type_summary.loc[
                post_type_summary["avg_engagement_rate"].idxmax()
            ]
            st.success(
                f"🌟 **Top Engaging Format:** `{best_format['post_type']}` with an average engagement rate of **{best_format['avg_engagement_rate']:.2f}%**."
            )

        display_type_df = post_type_summary.copy()
        display_type_df.columns = [
            "Post Format",
            "Posts",
            "Likes",
            "Comments",
            "Shares",
            "Reach / Views",
            "Avg Engagement Rate (%)",
        ]
        st.dataframe(
            display_type_df.style.format(
                {
                    "Posts": "{:,}",
                    "Likes": "{:,}",
                    "Comments": "{:,}",
                    "Shares": "{:,}",
                    "Reach / Views": "{:,}",
                    "Avg Engagement Rate (%)": "{:.2f}%",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )


# --- TAB 4: TOP-PERFORMING POSTS ---
with tab_top_posts:
    st.subheader("Top-Performing Posts Leaderboard")

    top_col1, top_col2 = st.columns([2, 1])
    with top_col1:
        metric_choice = st.selectbox(
            "Rank Posts By:",
            options=[
                ("engagement_rate", "Engagement Rate (%)"),
                ("likes", "Total Likes"),
                ("comments", "Total Comments"),
                ("shares", "Total Shares"),
                ("reach_or_views", "Reach / Views"),
            ],
            format_func=lambda x: x[1],
        )[0]
    with top_col2:
        top_n = st.slider("Number of Posts to Display:", min_value=3, max_value=20, value=5)

    top_posts_df = get_top_posts(filtered_df, metric=metric_choice, top_n=top_n)

    # Display Top 3 posts as cards
    st.markdown("#### 🌟 Top Highlights")
    highlight_cols = st.columns(min(3, len(top_posts_df)))
    for idx, (col, post) in enumerate(zip(highlight_cols, top_posts_df.iloc[:3].to_dict(orient="records"))):
        with col:
            rank_emoji = ["🥇", "🥈", "🥉"][idx]
            st.markdown(
                f"""
                <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 10px; padding: 14px; box-shadow: 0 2px 6px rgba(0,0,0,0.03);">
                    <div style="font-size: 1.1rem; font-weight: 700;">{rank_emoji} Rank #{idx+1}</div>
                    <div style="margin: 6px 0;">{get_platform_badge(post['platform'])} <span style="font-size: 0.85rem; color: #718096;">{post['post_type']} • {post['post_date'].strftime('%b %d, %Y')}</span></div>
                    <p style="font-size: 0.95rem; font-weight: 500; min-height: 48px; color: #2D3748;">"{post['caption']}"</p>
                    <hr style="margin: 8px 0; border: none; border-top: 1px solid #EDF2F7;"/>
                    <div style="display: flex; justify-content: space-between; font-size: 0.85rem;">
                        <span>❤️ <b>{post['likes']:,}</b></span>
                        <span>💬 <b>{post['comments']:,}</b></span>
                        <span>🔄 <b>{post['shares']:,}</b></span>
                        <span>⚡ <b>{post['engagement_rate']:.2f}%</b></span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("---")
    st.markdown("#### 📋 Full Leaderboard")

    table_data = top_posts_df[
        [
            "post_id",
            "platform",
            "post_type",
            "post_date",
            "caption",
            "likes",
            "comments",
            "shares",
            "reach_or_views",
            "engagement_rate",
        ]
    ].copy()
    table_data["post_date"] = table_data["post_date"].dt.strftime("%Y-%m-%d")
    table_data.columns = [
        "Post ID",
        "Platform",
        "Format",
        "Date",
        "Caption",
        "Likes",
        "Comments",
        "Shares",
        "Reach / Views",
        "Engagement Rate (%)",
    ]

    st.dataframe(
        table_data.style.format(
            {
                "Likes": "{:,}",
                "Comments": "{:,}",
                "Shares": "{:,}",
                "Reach / Views": "{:,}",
                "Engagement Rate (%)": "{:.2f}%",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )


# --- TAB 5: RAW DATA & EXPORT ---
with tab_raw_data:
    st.subheader("Dataset Explorer & Export")
    st.write(f"Showing **{len(filtered_df):,}** of **{len(raw_df):,}** posts based on your active filters.")

    search_query = st.text_input("🔎 Search by post caption or ID:", placeholder="e.g. Python, Hackathon, POST_042")
    view_df = filtered_df.copy()
    if search_query:
        view_df = view_df[
            view_df["caption"].str.contains(search_query, case=False, na=False)
            | view_df["post_id"].str.contains(search_query, case=False, na=False)
        ]

    st.dataframe(
        view_df[
            [
                "post_id",
                "platform",
                "post_type",
                "post_date",
                "caption",
                "likes",
                "comments",
                "shares",
                "reach_or_views",
                "engagement_rate",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )

    # Download filtered CSV
    csv_bytes = view_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv_bytes,
        file_name="socialpulse_filtered_data.csv",
        mime="text/csv",
    )
