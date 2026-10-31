# ⚡ SocialPulse – Social Media Data Analytics Dashboard

**SocialPulse** is a lightweight, responsive, and beginner-friendly Python web application designed for social media performance analytics and cross-platform benchmarking. It empowers creators, marketing teams, and students to analyze interactions across **Instagram**, **Facebook**, and **YouTube**.

Built specifically as a clean college **B.Tech Mini Project**, it emphasizes modular Python architecture, interactive Plotly visualizations, robust error handling, and zero-configuration deployment to **Streamlit Community Cloud**.

---

## 🚀 Key Features

1. **Executive KPI Dashboard**:
   - Total Posts, Total Likes, Total Comments, Total Shares, Total Reach.
   - Overall Average Engagement Rate (%) and per-post metrics.
2. **Formula-Driven Engagement Analysis**:
   - Calculates engagement rates safely avoiding zero-division errors:
     $$\text{Engagement Rate (\%)} = \left(\frac{\text{Likes} + \text{Comments} + \text{Shares}}{\text{Reach or Views}}\right) \times 100$$
3. **Cross-Platform Benchmarking**:
   - Side-by-side comparison between **Instagram**, **Facebook**, and **YouTube**.
   - Grouped interaction bar charts and interactive share donut charts.
4. **Content & Format Analytics**:
   - Performance evaluation across formats (e.g., *Reels vs Carousels vs Videos vs Static Posts*).
5. **Top-Performing Posts Leaderboard**:
   - Filter and rank top posts by Likes, Comments, Shares, or Engagement Rate.
   - Visual card badges for top podium highlights (#1, #2, #3).
6. **Data Upload & Demonstration**:
   - Pre-loaded realistic sample dataset containing **260 records** across multiple months.
   - Sidebar CSV uploader with column normalization and missing data safeguards.
   - One-click template download for demo presentations.
7. **Interactive Sidebar Filters**:
   - Filter dynamically by date range, platforms, and content formats.

---

## 📁 Project Structure

```text
SocialPulse/
│
├── .streamlit/
│   ├── config.toml             # Custom modern UI theme & server settings
│   └── credentials.toml        # Streamlit onboarding configuration
│
├── data/
│   ├── sample_social_media.csv # 260-row realistic sample dataset
│   └── generate_sample_data.py # Script used to generate the sample dataset
│
├── utils/
│   ├── __init__.py
│   ├── data_loader.py          # Data validation, column normalization & cleaning
│   ├── analytics.py            # Summary KPIs & statistical calculations
│   └── charts.py               # Responsive Plotly chart generators
│
├── app.py                      # Main Streamlit web application
├── test_app.py                 # Automated unit and integration test suite
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules
└── README.md                   # Project documentation
```

---

## 🛠️ Tech Stack

- **Language:** Python 3.10+
- **Frontend & App Framework:** [Streamlit](https://streamlit.io/)
- **Data Manipulation:** [Pandas](https://pandas.pydata.org/)
- **Interactive Visualizations:** [Plotly](https://plotly.com/python/)

---

## 💻 Local Setup & Execution Guide

### 1. Clone or Open the Repository
```bash
cd SocialPulse
```

### 2. (Optional but Recommended) Create a Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
streamlit run app.py
```
Open your browser and navigate to `http://localhost:8501`.

---

## 🧪 Running Unit Tests

Run the built-in test suite to verify data loading, platform normalization, zero-division handling, and chart generation:

```bash
python3 test_app.py
```

---

## ☁️ Deployment on Streamlit Community Cloud

This project is structured for 1-click deployment on **Streamlit Community Cloud**:

1. Push this repository to **GitHub**.
2. Go to [share.streamlit.io](https://share.streamlit.io/) and log in with your GitHub account.
3. Click **"New app"**.
4. Select your repository: `SocialPulse`.
5. Set the Main file path to: `app.py`.
6. Click **"Deploy!"**. Streamlit Cloud will install `requirements.txt` and launch the app immediately.

---

## 📊 CSV Schema for Custom Uploads

The dashboard supports custom CSV uploads. The file should contain the following fields (headers are case-insensitive):

| Column | Example | Description |
| :--- | :--- | :--- |
| `platform` | `Instagram` | Platform name (`Instagram`, `Facebook`, `YouTube`) |
| `post_date` | `2026-06-15` | Date of publishing (`YYYY-MM-DD`) |
| `post_type` | `Reel` | Format (`Reel`, `Video`, `Carousel`, `Image`, etc.) |
| `caption` | `10 Python Tips` | Post title or caption |
| `likes` | `1250` | Number of likes |
| `comments` | `85` | Number of comments |
| `shares` | `120` | Number of shares |
| `reach_or_views` | `18500` | Total reach or views count |

---

## 🎓 Academic Submission Highlights (VIVA / Demo Tips)

- **Architecture:** Demonstrates separation of concerns (`utils/data_loader.py` for ETL, `utils/analytics.py` for aggregation, `utils/charts.py` for visualization).
- **Resilience:** Gracefully handles empty files, missing column synonyms (e.g. `impressions` automatically maps to `reach_or_views`), zero reach, and missing text values.
- **Interactivity:** Uses Streamlit caching and Plotly hover-tooltips without requiring backend database servers or external paid APIs.
