# 🛡️ HTS Intelligence Platform
### *Modern Trade Compliance Powered by Industrial AI*

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://hts-intelligence.streamlit.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

The **HTS Intelligence Platform** is a state-of-the-art solution designed to simplify the complex world of the **Harmonized Tariff Schedule (HTS)**. By combining **Semantic Search**, **Vector Databases**, and **Large Language Models (LLMs)**, we bridge the gap between technical customs jargon and everyday product descriptions.

---

## 🚀 The Vision

Classifying products for international trade is a manual, error-prone process involving over **30,000 unique codes**. A single mistake can lead to heavy penalties, shipping delays, and lost revenue.

Our platform empowers trade professionals to:
- 🔍 **Search Semantically**: Find codes using plain English (e.g., "plastic water bottles") instead of technical terms.
- 🧠 **Classify with AI**: Leverage LLMs to analyze complex product specs and receive regulatory reasoning.
- 🌲 **Explore Hierarchy**: Navigate the HTS tree from broad chapters down to 10-digit specific codes.
- ⚡ **Reduce Risk**: Ensure compliance with high-confidence, AI-validated classification logic.

---

## ✨ Key Features

| Feature | Description |
| :--- | :--- |
| **HTS Search** | Sub-second semantic search across 35,000+ records using OpenAI embeddings. |
| **Classification AI** | Deep-dive assistant that explains *why* a code was chosen based on HTS rulings. |
| **Hierarchy Browser** | Interactive navigation of the "Tree of HTS" to understand parent/child legal notes. |
| **Analytics Dashboard** | Real-time monitoring of dataset health, search patterns, and system performance. |
| **Premium UI** | A sleek, glassmorphism-inspired dark mode designed for professional environments. |

---

## 🏗️ Technical Architecture

- **Frontend**: [Streamlit](https://streamlit.io/) (Python-based interactive framework)
- **Database**: [Supabase](https://supabase.com/) (PostgreSQL + `pgvector` for vector storage)
- **AI/Embeddings**: [OpenAI](https://openai.com/) (`text-embedding-3-small`)
- **Indexing**: Custom **HNSW** (Hierarchical Navigable Small World) for ultra-fast similarity search.

---

## 🛠️ Getting Started

### 1️⃣ Prerequisites
- Python 3.9+
- A Supabase Project (with `pgvector` enabled)
- An OpenAI API Key

### 2️⃣ Local Installation
```bash
# Clone the repository
git clone https://github.com/your-repo/hts-dashboard.git
cd hts-dashboard

# Install dependencies
pip install -r requirements.txt

# Set up environment variables (.env)
cp .hts_dashboard/.env.example .env 
# (Update .env with your Supabase and OpenAI keys)
```

### 3️⃣ Database Setup
1. Open your **Supabase SQL Editor**.
2. Run the contents of `supabase_rpc_fix.sql` to create the `match_hts_chunks` function.
3. (Optional) Run `rebuild_embeddings.py` to populate your database from the source JSON.

### 4️⃣ Run the App
```bash
streamlit run app.py
```

---

## 📦 Project Structure

- `app.py`: Main entry point and landing page.
- `pages/`: Individual dashboard pages (Search, AI, Analytics).
- `utils/`: Core logic for database connections, search, and UI components.
- `diagnostic_tool.py`: Pre-deployment health check script.
- `requirements.txt`: Pinned dependencies for stability.

---

## 📄 Documentation & Resources

- [Pre-Deployment Checklist](DEPLOYMENT.md)
- [Project Documentation (Deep Dive)](PROJECT_DOCUMENTATION.md)
- [Quick Start: RPC Fix Guide](QUICKSTART.md)

---

## 🤝 Contributing & Support

We welcome contributions! Please see our `CONTRIBUTING.md` (coming soon) for details. For issues, please open a GitHub Issue or reach out to the trade compliance team.

---

**Built with ❤️ for Global Trade Professionals.**
