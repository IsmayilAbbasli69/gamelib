# 🎮 AI-Powered Gamer Matchmaking & Teammate Recommendation System

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?style=for-the-badge&logo=python&logoColor=white)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Scikit--Learn-orange.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Hackathon](https://img.shields.io/badge/Hackathon-Project-success.svg?style=for-the-badge)

An AI-driven recommendation engine that analyzes players' **Steam gameplay hours**, **preferred in-game roles**, and **genre interests** to match them with the most compatible teammates in real time.

---

## 💡 The Problem & Our Solution
Traditional matchmaking systems in online gaming rely strictly on player ranks (Rank/MMR). This narrow approach often leads to toxic lobbies, clashing playstyles, and role conflicts (e.g., getting matched into a team where everyone wants to play the same role).

**Our Solution:** An intelligent matchmaking engine that evaluates actual player behavior and historical data (Steam hours). It calculates mathematical profile proximity to build well-balanced, high-compatibility teams containing complementary roles.

---

## 🧠 Machine Learning Architecture

The system processes raw gaming metrics into actionable match recommendations through a 3-stage pipeline:

1. **Data Source (`data_source.py`):** A curated synthetic dataset containing 150 unique player profiles, tracking individual playtime across 8 popular titles (*CS2, Dota 2, Witcher 3, Cyberpunk 2077, Elden Ring, GTA V, Baldur's Gate 3, Left 4 Dead 2*) alongside their strategic team roles.
2. **Feature Engineering & Scaling (`data_preprocessing.py`):** To prevent extreme playhour discrepancies (e.g., 2,000 hours in one game vs. 5 hours in another) from distorting the model, features are normalized utilizing `sklearn.preprocessing.MinMaxScaler` to bind values strictly between $0$ and $1$.
3. **Mathematical Vector Modeling (`model.py`):** The engine maps players into a multi-dimensional vector space and utilizes **Cosine Similarity** to compute exact geometric proximity and taste alignment. Formula:
   $$\text{Similarity}(A, B) = \frac{A \cdot B}{\|A\| \|B\|}$$

---

## 📁 Repository Structure

```text
├── data_source.py         # Synthetic database of 150 unique player profiles
├── data_preprocessing.py  # Data ingestion, feature extraction, and MinMaxScaler implementation
├── model.py               # Main ML engine utilizing Cosine Similarity for matchmaking
├── requirements.txt       # Project dependencies and environment packages
└── README.md              # Project documentation (This file)
