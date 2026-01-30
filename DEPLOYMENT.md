# Streamlit Cloud Deployment Guide

## 🎯 Quick Fix Summary

The RPC error was caused by **parameter ordering**. The Supabase Python client passes parameters in **alphabetical order**, not the order you define them. Your Postgres function must match this alphabetical ordering.

### What Changed

1. **[search.py](file:///Users/gauravsalvi/Downloads/hts_dashboard/utils/search.py)**: Reordered parameters and added error handling
2. **[supabase_rpc_fix.sql](file:///Users/gauravsalvi/Downloads/hts_dashboard/supabase_rpc_fix.sql)**: SQL script to create/verify RPC function
3. **[diagnostic_tool.py](file:///Users/gauravsalvi/Downloads/hts_dashboard/diagnostic_tool.py)**: Pre-deployment testing tool
4. **[requirements.txt](file:///Users/gauravsalvi/Downloads/hts_dashboard/requirements.txt)**: Pinned versions for consistency

---

## 📋 Pre-Deployment Checklist

### Step 1: Fix Supabase RPC Function

1. Open your **Supabase SQL Editor**
2. Copy and paste the entire contents of `supabase_rpc_fix.sql`
3. Run the script
4. Verify the output shows the function was created successfully

**Critical:** The function signature must be:
```sql
match_hts_chunks(match_count int, query_embedding vector)
```

Note the **alphabetical order**: `match_count` comes before `query_embedding`.

### Step 2: Verify Embedding Dimensions

Check your embedding model and dimension:

| Model | Dimension |
|-------|-----------|
| `text-embedding-ada-002` | 1536 |
| `text-embedding-3-small` | 1536 |
| `text-embedding-3-large` | 3072 |

If using `text-embedding-3-large`, update the SQL script to use `vector(3072)` instead of `vector(1536)`.

### Step 3: Test Locally

Run the diagnostic tool to verify everything works:

```bash
python diagnostic_tool.py
```

This will test:
- ✅ Environment variables
- ✅ Supabase connection
- ✅ OpenAI embeddings
- ✅ RPC function call

**All tests must pass** before deploying to Streamlit Cloud.

### Step 4: Update Environment Variables

Ensure your `.env` file (or Streamlit Cloud secrets) contains:

```env
# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
SUPABASE_TABLE=hts_knowledge_chunks
SUPABASE_MATCH_RPC=match_hts_chunks

# OpenAI
OPENAI_API_KEY=sk-...
EMBEDDING_MODEL=text-embedding-ada-002
EMBEDDING_DIM=1536
```

> [!IMPORTANT]
> The `SUPABASE_MATCH_RPC` value must match your actual function name in Supabase.

---

## 🚀 Streamlit Cloud Deployment

### Step 1: Push Code to GitHub

```bash
git add .
git commit -m "Fix RPC parameter ordering for Streamlit Cloud"
git push origin main
```

### Step 2: Configure Streamlit Cloud Secrets

1. Go to your app on **Streamlit Cloud**
2. Click **Settings** → **Secrets**
3. Add all environment variables in TOML format:

```toml
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_SERVICE_ROLE_KEY = "your-service-role-key"
SUPABASE_TABLE = "hts_knowledge_chunks"
SUPABASE_MATCH_RPC = "match_hts_chunks"

OPENAI_API_KEY = "sk-..."
EMBEDDING_MODEL = "text-embedding-ada-002"
EMBEDDING_DIM = "1536"
```

> [!WARNING]
> Use **TOML format** for Streamlit Cloud secrets, not `.env` format. Note the quotes around values.

### Step 3: Deploy

1. Click **Reboot app** to force a fresh deployment
2. Monitor the deployment logs for any errors
3. Once deployed, test the Classification AI page

---

## 🔍 Troubleshooting

### Error: "Could not find the function"

**Cause:** RPC function doesn't exist or has wrong signature

**Fix:**
1. Run `supabase_rpc_fix.sql` in Supabase SQL Editor
2. Verify function exists:
   ```sql
   SELECT proname, pg_get_function_arguments(oid) 
   FROM pg_proc 
   WHERE proname = 'match_hts_chunks';
   ```
3. Ensure parameters are in alphabetical order

### Error: "Dimension mismatch"

**Cause:** Embedding dimension doesn't match vector column

**Fix:**
1. Check your `EMBEDDING_MODEL` and `EMBEDDING_DIM`
2. Update SQL function to match (e.g., `vector(3072)` for 3-large)
3. Regenerate embeddings if you changed models

### Error: "Connection timeout"

**Cause:** Network issues or Supabase connection pooling

**Fix:**
1. Verify `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY`
2. Check Supabase project is not paused
3. The retry logic in `search.py` should handle transient errors

### No Results Returned

**Cause:** Empty table or embeddings not generated

**Fix:**
1. Verify `hts_knowledge_chunks` table has data:
   ```sql
   SELECT COUNT(*) FROM hts_knowledge_chunks;
   ```
2. Check that embeddings exist:
   ```sql
   SELECT COUNT(*) FROM hts_knowledge_chunks WHERE embedding IS NOT NULL;
   ```

---

## 🧪 Testing After Deployment

1. **Navigate to Classification AI page**
2. **Enter a test query**: "plastic bottle for drinking water"
3. **Click Classify**
4. **Verify results appear** with HTS codes and descriptions

If successful, you should see relevant HTS codes like:
- 3923.30 - Carboys, bottles, flasks and similar articles
- 3924.10 - Tableware and kitchenware

---

## 📊 What the Fix Does

### Before (Broken)
```python
# Python code sends:
{"query_embedding": vector, "match_count": 5}

# Supabase client calls (alphabetically):
match_chunks(match_count=5, query_embedding=vector)

# But Postgres function expects:
match_chunks(query_embedding vector, match_count int)  ❌
```

### After (Fixed)
```python
# Python code sends:
{"match_count": 5, "query_embedding": vector}

# Supabase client calls (alphabetically):
match_hts_chunks(match_count=5, query_embedding=vector)

# Postgres function signature:
match_hts_chunks(match_count int, query_embedding vector)  ✅
```

The key insight: **Supabase Python client always passes parameters alphabetically**, regardless of how you define them in the dictionary.

---

## 🎉 Success Criteria

- ✅ Diagnostic tool passes all tests locally
- ✅ RPC function exists in Supabase with correct signature
- ✅ All environment variables set in Streamlit Cloud
- ✅ App deploys without errors
- ✅ Classification AI returns HTS code results

---

## 📞 Need Help?

If you still encounter issues after following this guide:

1. **Check Streamlit Cloud logs** for detailed error messages
2. **Run diagnostic tool locally** to isolate the issue
3. **Verify RPC function** in Supabase SQL Editor
4. **Compare environment variables** between local and cloud

The most common issue is forgetting to run the SQL script or having mismatched environment variables between local and cloud.
