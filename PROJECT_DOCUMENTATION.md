# HTS Intelligence Dashboard - Project Documentation

## 📋 Table of Contents
1. [Project Overview & Business Idea](#-project-overview)
2. [Technical Architecture](#-technical-architecture)
3. [Features & Page Descriptions](#-features)
4. [Problems Faced & Solutions](#-problems-faced)
5. [Development Progress & Fixes](#-development-progress)
6. [Future Scope](#-future-scope)

---

## 🚀 Project Overview
The **HTS Intelligence Dashboard** is an AI-powered platform designed to revolutionize how businesses and individuals interact with the **Harmonized Tariff Schedule (HTS)**. 

### The Problem
Classifying products for international trade is notoriously complex. The HTS contains over 30,000 codes, and finding the correct one requires deep expertise. Errors in classification lead to incorrect duty payments, legal penalties, and shipping delays.

### The Business Idea
Using **Semantic Search** and **LLMs (Large Language Models)**, this dashboard allows users to find HTS codes using plain English descriptions instead of memorizing technical jargon. It bridges the gap between complex legal text and everyday product names (e.g., matching "plastic water bottles" to the correct technical heading 3923).

---

## 🏗 Technical Architecture
- **Frontend**: [Streamlit](https://streamlit.io/) (Python-based interactive web framework).
- **Database**: [Supabase](https://supabase.com/) (PostgreSQL with `pgvector` extension).
- **AI/Embeddings**: [OpenAI](https://openai.com/) (`text-embedding-3-small` for 1536-dimension vectors).
- **Search Engine**: Vector similarity search using **Cosine Distance** on HNSW indexes.

---

## 🔍 Features & Page Descriptions

### 1. HTS Search
Perform semantic searches across the entire HTS database.
- **How it works**: Your query is converted into a vector and matched against the database.
- **Capability**: Understands synonyms and context (e.g., "bicycles" matches "cycles, not motorized").

### 2. Classification AI
A high-level assistant for complex product descriptions.
- **Use Case**: Paste a full product specification, and the AI suggests the most likely HTS codes with confidence levels and reasoning.

### 3. Hierarchy Browser
Explore the "Tree of HTS".
- **Functionality**: Navigate from broad Chapters (01-99) down to specific 10-digit codes. Essential for seeing "parent" legal notes.

### 4. Analytics Dashboard
Track usage and data health.
- **Metrics**: Total records (35,571), average search speed, and classification patterns.

### 5. Settings & Config
Configure API keys and UI preferences.
- **Fixed**: This page now features high-quality premium HTML rendering for a glassmorphism aesthetic.

### 6. Chunk Browser (Debug Tool)
Advanced view of the underlying knowledge base.
- **Functionality**: Allows developers to see exactly what text is being used for each embedding chunk.

---

## 🛠 Problems Faced & Solutions

### 1. The "Horses vs. Trousers" Mismatch (Critical)
**Problem**: Searching for "live horses" returned "trousers and breeches."
**Cause**: The embeddings in the database were corrupted or mismatched with the text data due to previous fragmented imports.
**Solution**: We performed a **full, clean rebuild**. We deleted all 35,000 rows and re-imported them directly from the `hts_2026_basic_edition_json.json` source, ensuring 1:1 alignment between text and 1536-dim vectors.

### 2. Supabase RPC Alphabetical Bug
**Problem**: The app couldn't find the `match_hts_chunks` function.
**Cause**: The Supabase Python client passes parameters to Postgres in **alphabetical order** (`match_count` before `query_embedding`), but the function was defined differently.
**Solution**: Redefined the SQL function signature to accept parameters in alphabetical order.

### 3. Search Timeouts
**Problem**: Small queries would crash with a "Statement Timeout."
**Cause**: Sequential scanning of 35,000+ high-dimensional vectors is computationally expensive.
**Solution**: Recommended and implemented a custom **HNSW (Hierarchical Navigable Small World)** index in Supabase to enable sub-second similarity searches.

---

## ✅ Development Progress & Fixes
- **Data Integrity**: Verified 35,571 HTS records are now 100% correctly embedded.
- **UI/UX**: Implemented a Premium Dark Mode with Glassmorphism effects.
- **Logic**: Standardized all search calls to use the `match_hts_chunks` RPC.
- **Environment**: Fixed `.env` path issues to ensure Streamlit Cloud compatibility.

---

## 🔮 Future Scope
- **Real-time Duty Calculation**: Integrate with official APIs to provide live duty rates.
- **Document OCR**: Allow users to upload invoices and auto-extract HTS codes.
- **Chatbot Integration**: A dedicated AI agent that can explain legal footnotes and exclusions.
