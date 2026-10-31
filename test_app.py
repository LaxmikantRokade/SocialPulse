"""Automated unit and integration tests for SocialPulse."""

import io
import unittest
import pandas as pd
from utils.data_loader import load_dataset, validate_and_clean_data
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


class TestSocialPulse(unittest.TestCase):
    def setUp(self):
        self.df = load_dataset()

    def test_sample_dataset_loaded(self):
        self.assertGreaterEqual(len(self.df), 200, "Sample dataset should contain at least 200 rows")
        expected_cols = [
            "post_id", "platform", "post_date", "post_type",
            "caption", "likes", "comments", "shares",
            "reach_or_views", "total_engagement", "engagement_rate"
        ]
        for col in expected_cols:
            self.assertIn(col, self.df.columns)

    def test_platforms_normalized(self):
        platforms = set(self.df["platform"].unique())
        self.assertTrue(platforms.issubset({"Instagram", "Facebook", "YouTube"}))

    def test_no_negative_or_null_values(self):
        self.assertFalse(self.df["likes"].isna().any())
        self.assertFalse(self.df["comments"].isna().any())
        self.assertFalse(self.df["shares"].isna().any())
        self.assertTrue((self.df["likes"] >= 0).all())
        self.assertTrue((self.df["comments"] >= 0).all())
        self.assertTrue((self.df["shares"] >= 0).all())

    def test_zero_division_guard(self):
        zero_reach_csv = io.StringIO(
            "platform,post_date,likes,comments,shares,reach_or_views\n"
            "Instagram,2026-05-01,10,2,1,0\n"
        )
        df_zero = validate_and_clean_data(pd.read_csv(zero_reach_csv))
        self.assertEqual(df_zero.iloc[0]["engagement_rate"], 0.0)

    def test_invalid_csv_handling(self):
        bad_csv = io.StringIO("invalid_col1,invalid_col2\n1,2\n")
        with self.assertRaises(ValueError):
            validate_and_clean_data(pd.read_csv(bad_csv))

    def test_overall_metrics(self):
        metrics = calculate_overall_metrics(self.df)
        self.assertEqual(metrics["total_posts"], len(self.df))
        self.assertGreater(metrics["total_likes"], 0)
        self.assertGreater(metrics["total_comments"], 0)
        self.assertGreater(metrics["total_shares"], 0)
        self.assertGreater(metrics["avg_engagement_rate"], 0.0)

    def test_platform_comparison(self):
        p_df = get_platform_comparison(self.df)
        self.assertEqual(len(p_df), 3)
        self.assertIn("Facebook", p_df["platform"].values)
        self.assertIn("Instagram", p_df["platform"].values)
        self.assertIn("YouTube", p_df["platform"].values)

    def test_top_posts(self):
        top_5 = get_top_posts(self.df, metric="likes", top_n=5)
        self.assertEqual(len(top_5), 5)
        # Check sorting order
        self.assertGreaterEqual(top_5.iloc[0]["likes"], top_5.iloc[1]["likes"])

    def test_timeline_data(self):
        timeline_w = get_timeline_data(self.df, freq="W")
        self.assertFalse(timeline_w.empty)
        self.assertIn("post_date", timeline_w.columns)

    def test_charts_generation(self):
        p_df = get_platform_comparison(self.df)
        t_df = get_timeline_data(self.df, freq="W")
        pt_df = get_post_type_comparison(self.df)

        fig1 = plot_platform_comparison_bars(p_df)
        fig2 = plot_platform_share_donut(p_df)
        fig3 = plot_engagement_rate_comparison(p_df)
        fig4 = plot_timeline_trends(t_df)
        fig5 = plot_post_type_performance(pt_df)
        fig6 = plot_reach_vs_engagement(self.df)

        self.assertIsNotNone(fig1)
        self.assertIsNotNone(fig2)
        self.assertIsNotNone(fig3)
        self.assertIsNotNone(fig4)
        self.assertIsNotNone(fig5)
        self.assertIsNotNone(fig6)


if __name__ == "__main__":
    unittest.main()
