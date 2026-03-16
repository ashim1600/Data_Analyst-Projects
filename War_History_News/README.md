# ⚔️ Major War Histories & News — Streamlit App

An interactive dashboard built with **Python** and **Streamlit** that explores major armed conflicts throughout history and provides the latest war-related news.

---

## 🚀 Features

| Section | Description |
|---|---|
| 🏠 **Overview** | Key metrics, war timeline, and casualties bar chart |
| 📚 **War Encyclopedia** | Detailed cards for 12+ major wars with cause, outcome & Wikipedia links |
| 📊 **Statistics** | Casualties by type (pie), wars per region (bar), civilian vs military scatter, duration chart, raw data table |
| 🗺️ **World Map** | Interactive globe with bubble size = casualties, colour = war type |
| 📰 **News** | Curated war news + optional live feed via [NewsAPI](https://newsapi.org) |

---

## 🗂️ Wars Covered

- Napoleonic Wars (1803–1815)
- American Civil War (1861–1865)
- World War I (1914–1918)
- World War II (1939–1945)
- Korean War (1950–1953)
- Vietnam War (1955–1975)
- Gulf War (1990–1991)
- Afghanistan War (2001–2021)
- Iraq War (2003–2011)
- Syrian Civil War (2011–2024)
- Russia–Ukraine War (2022–ongoing)
- Israel–Gaza War (2023–ongoing)

---

## 🛠️ Setup & Run

### 1. Clone the repository

```bash
git clone https://github.com/ashim1600/Data_Analyst-Projects.git
cd Data_Analyst-Projects/War_History_News
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
streamlit run app.py
```

The app will open at **http://localhost:8501** in your browser.

---

## 📡 Live News (Optional)

To enable live war news, obtain a free API key from [https://newsapi.org](https://newsapi.org), then enter it in the **sidebar** of the running app. Without a key, the app shows a curated set of static news articles.

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `streamlit` | Web app framework |
| `pandas` | Data manipulation |
| `plotly` | Interactive charts & maps |
| `requests` | HTTP calls for live news |
| `Pillow` | Image handling |

---

## 📁 Project Structure

```
War_History_News/
├── app.py            # Main Streamlit application
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

---

## ⚠️ Disclaimer

Casualty figures and historical data are **estimates** drawn from academic, governmental, and encyclopaedic sources. This dashboard is intended for **educational purposes only**.
