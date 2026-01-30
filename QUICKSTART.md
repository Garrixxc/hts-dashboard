# 🚀 Quick Start - Streamlit Cloud RPC Fix

## The Problem
```
Could not find the function public.match_hts_chunks(match_count, query_embedding)
```

## The Root Cause
Supabase Python client passes RPC parameters in **alphabetical order**, not the order you define them.

## The Fix (3 Steps)

### 1️⃣ Run SQL Script in Supabase
```sql
-- Copy supabase_rpc_fix.sql and run in Supabase SQL Editor
-- This creates the function with correct parameter order
```

### 2️⃣ Test Locally
```bash
python diagnostic_tool.py
```
All tests must pass ✅

### 3️⃣ Deploy to Streamlit Cloud

**Set these secrets in Streamlit Cloud:**
```toml
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_SERVICE_ROLE_KEY = "your-key"
SUPABASE_TABLE = "hts_knowledge_chunks"
SUPABASE_MATCH_RPC = "match_hts_chunks"
OPENAI_API_KEY = "sk-..."
EMBEDDING_MODEL = "text-embedding-ada-002"
EMBEDDING_DIM = "1536"
```

Then **Reboot app** in Streamlit Cloud.

---

## Files Changed

| File | What Changed |
|------|--------------|
| `utils/search.py` | ✅ Fixed parameter ordering + retry logic |
| `supabase_rpc_fix.sql` | ✅ SQL to create/verify RPC function |
| `diagnostic_tool.py` | ✅ Pre-deployment testing tool |
| `requirements.txt` | ✅ Pinned versions |
| `DEPLOYMENT.md` | ✅ Full deployment guide |

---

## Verification

After deployment, test on Classification AI page:
- Input: "plastic bottle for drinking water"
- Expected: HTS codes like 3923.30 returned

---

**Need more details?** See [DEPLOYMENT.md](file:///Users/gauravsalvi/Downloads/hts_dashboard/DEPLOYMENT.md)
