"""Script to generate realistic sample social media data for SocialPulse."""

import csv
import random
from datetime import datetime, timedelta

# Seed for reproducibility
random.seed(42)

platforms_config = {
    "Instagram": {
        "types": ["Reel", "Carousel", "Image", "Story"],
        "reach_range": (3000, 75000),
        "like_ratio": (0.04, 0.12),
        "comment_ratio": (0.003, 0.015),
        "share_ratio": (0.005, 0.035),
    },
    "Facebook": {
        "types": ["Post", "Video", "Image", "Link"],
        "reach_range": (1500, 45000),
        "like_ratio": (0.02, 0.08),
        "comment_ratio": (0.002, 0.012),
        "share_ratio": (0.003, 0.020),
    },
    "YouTube": {
        "types": ["Video", "Shorts", "Community"],
        "reach_range": (5000, 180000),
        "like_ratio": (0.03, 0.10),
        "comment_ratio": (0.004, 0.020),
        "share_ratio": (0.002, 0.015),
    },
}

sample_captions = [
    "10 Must-Know Python Tricks for Beginners 🚀 #coding #python",
    "How I Built a Full Stack Web App in 48 Hours 💻🔥",
    "Campus Placement Guide: Top DSA Questions You Must Practice 📚",
    "Streamlit vs Dash: Which one should you learn first? 🤔",
    "Behind the Scenes of our College Tech Fest 2026 🎉✨",
    "Machine Learning Roadmap for College Students 🤖📈",
    "Day in the Life of a Computer Science Student ☕💻",
    "Top 5 Free APIs Every Developer Needs to Build Cool Projects 🌐",
    "How to Write Clean and Maintainable Code: Senior Dev Advice ✨",
    "Hackathon Winning Strategy: From Idea to Working MVP in 24h 🏆",
    "Why Python is Still the King of Data Science in 2026 👑",
    "Git and GitHub Cheat Sheet for Beginners 🐙⚡",
    "Building an AI Agent from Scratch in Python 🧠",
    "Resume Tips That Actually Get You Software Engineering Interviews 📄",
    "Understanding Big O Notation with Simple Real-Life Examples ⏱️",
    "Best VS Code Extensions for High Productivity in 2026 ⚡",
    "Project Showcase: SocialPulse Social Media Analytics Tool 📊",
    "Web Dev Trends to Watch Out For This Year 🚀",
    "5 Mistakes I Made as a First-Year Engineering Student 🤦‍♂️",
    "Quick Guide to SQL Queries: Group By, Joins, and Indexes 🗄️",
    "Docker Basics in 5 Minutes: Containers Explained Simply 🐳",
    "College Vlog: Semester Exam Preparation & Caffeine Rush ☕📖",
    "Cybersecurity 101: How to Keep Your Web Apps Safe 🛡️",
    "Building REST APIs with FastAPI vs Flask: Benchmark Test ⚡",
    "Top Open Source Projects Open for Student Contributions 🌟",
]

start_date = datetime(2026, 5, 1)
total_days = 180

records = []
for i in range(1, 261):
    post_id = f"POST_{i:03d}"
    platform = random.choice(["Instagram", "Facebook", "YouTube"])
    cfg = platforms_config[platform]
    
    post_type = random.choice(cfg["types"])
    days_offset = random.randint(0, total_days)
    post_date = (start_date + timedelta(days=days_offset)).strftime("%Y-%m-%d")
    
    reach = random.randint(*cfg["reach_range"])
    
    # Calculate realistic engagement based on reach
    likes = int(reach * random.uniform(*cfg["like_ratio"]))
    comments = int(reach * random.uniform(*cfg["comment_ratio"]))
    shares = int(reach * random.uniform(*cfg["share_ratio"]))
    
    # Ensure minimum counts
    likes = max(1, likes)
    comments = max(0, comments)
    shares = max(0, shares)
    
    caption = random.choice(sample_captions)
    
    records.append({
        "post_id": post_id,
        "platform": platform,
        "post_date": post_date,
        "post_type": post_type,
        "caption": caption,
        "likes": likes,
        "comments": comments,
        "shares": shares,
        "reach_or_views": reach,
    })

# Sort chronologically
records.sort(key=lambda x: x["post_date"])

output_path = "/Users/apple/Documents/Projects/SocialPulse/data/sample_social_media.csv"
fieldnames = [
    "post_id", "platform", "post_date", "post_type", 
    "caption", "likes", "comments", "shares", "reach_or_views"
]

with open(output_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(records)

print(f"Successfully generated {len(records)} records in {output_path}")
