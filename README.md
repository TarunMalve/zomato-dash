# 🍽️ Zomato Analytics Dashboard

A production-ready, full-stack data analytics dashboard built with **Python**, **Streamlit**, and **Plotly** — providing restaurant owners and market analysts with actionable insights into Bangalore's dining landscape using the Zomato dataset.

---

## 📸 Dashboard Overview

The dashboard includes:
- **Executive Summary KPIs** – Total restaurants, votes, avg votes, median cost
- **Market Segmentation** – Service analysis (online order × book table) and restaurant type distribution
- **Performance & Rating Analytics** – Cuisine leaderboard, correlation heatmap, and location performance
- **Deep Dive Explorations** – Cost distribution histogram and votes vs. rating scatter plot
- **Sidebar Filters** – Filter by location, dining type, and online order availability

---

## ✨ Features

- 🔴 Zomato-branded theme (`#E23744`)
- 📊 Interactive Plotly charts (bar, scatter, histogram, heatmap)
- 🔍 Dynamic sidebar filtering (location, type, online order)
- 💡 KPI metric cards for quick executive summaries
- 📁 Automatic fallback to sample data if `zomato.csv` is not found
- ⚡ `@st.cache_data` for fast repeated loads

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.9+ | Core language |
| Streamlit | Web app framework |
| Plotly Express | Interactive charts |
| Pandas | Data wrangling |
| NumPy | Numerical operations |

---

## 🚀 Setup & Run

```bash
# 1. Clone the repository
git clone https://github.com/TarunMalve/zomato-dash.git
cd zomato-dash

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the dashboard
streamlit run app.py
```

The app will automatically use `data/sample_zomato.csv` if `data/zomato.csv` is not present.

To use your own data, place your Zomato CSV at `data/zomato.csv`.

---

## 📋 Data Format

The CSV file (`zomato.csv` or `sample_zomato.csv`) must contain the following columns:

| Column | Type / Example |
|---|---|
| `address` | String |
| `name` | String (restaurant name) |
| `online_order` | `"Yes"` / `"No"` |
| `book_table` | `"Yes"` / `"No"` |
| `votes` | Integer (e.g., 450) |
| `location` | String (e.g., `"Indiranagar"`) |
| `cuisines` | Comma-separated string (e.g., `"North Indian, Chinese"`) |
| `approx_cost(for two people)` | Numeric or string with commas (e.g., `800`, `"1,100"`) |
| `listed_in(type)` | Categorical (e.g., `"Dining"`, `"Cafes"`, `"Delivery"`) |
| `listed_in(city)` | String (city area/hub name) |
| `rest_type` | String (e.g., `"Casual Dining"`, `"Quick Bites"`) |
| `Phone` | String |
| `rate` | String like `"4.2/5"`, may contain `"NEW"`, `"-"`, or NaN |

---

## 📁 Project Structure

```
zomato-dash/
├── .streamlit/
│   └── config.toml        # Streamlit theme & server config
├── data/
│   └── sample_zomato.csv  # Sample dataset (55 rows)
├── utils/
│   ├── __init__.py
│   └── data_loader.py     # Data loading & cleaning utilities
├── app.py                 # Main Streamlit dashboard
├── requirements.txt       # Python dependencies
└── README.md
```

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.