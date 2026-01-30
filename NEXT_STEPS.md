# ✅ Git Push Successful - Next Steps

Your code has been successfully pushed to GitHub! Now follow these steps to complete the deployment:

## 🔴 CRITICAL STEP 1: Run SQL Script in Supabase

**This is the most important step** - without this, the RPC function doesn't exist and Streamlit will still fail.

1. Open your **Supabase Dashboard**
2. Go to **SQL Editor** (left sidebar)
3. Click **New Query**
4. Copy the entire contents of `supabase_rpc_fix.sql` from your project
5. Paste it into the SQL Editor
6. Click **Run** or press `Cmd+Enter`
7. Verify you see "Success" message

**What this does:** Creates the `match_hts_chunks` function with the correct parameter order: `(match_count int, query_embedding vector)`

---

## 📝 STEP 2: Update Streamlit Cloud Secrets

1. Go to your **Streamlit Cloud Dashboard**
2. Click on your **hts-dashboard** app
3. Click **Settings** (⚙️) → **Secrets**
4. Add/update these values in TOML format:

```toml
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_SERVICE_ROLE_KEY = "your-service-role-key-here"
SUPABASE_TABLE = "hts_knowledge_chunks"
SUPABASE_MATCH_RPC = "match_hts_chunks"

OPENAI_API_KEY = "sk-your-key-here"
EMBEDDING_MODEL = "text-embedding-ada-002"
EMBEDDING_DIM = "1536"
```

5. Click **Save**

---

## 🔄 STEP 3: Reboot Streamlit App

1. In Streamlit Cloud dashboard, click the **⋮** menu (three dots)
2. Click **Reboot app**
3. Wait for the app to redeploy (usually 1-2 minutes)
4. Monitor the deployment logs for any errors

---

## ✅ STEP 4: Test the Fix

1. Once the app is running, navigate to **Classification AI** page
2. Enter a test query: `"plastic bottle for drinking water"`
3. Click **Classify**
4. **Expected result:** You should see HTS codes like:
   - 3923.30 - Carboys, bottles, flasks and similar articles
   - 3924.10 - Tableware and kitchenware

If you see results, **the fix worked!** 🎉

---

## 🔍 If It Still Fails

1. **Check Streamlit Cloud logs** for the exact error message
2. **Verify the SQL script ran successfully** in Supabase:
   ```sql
   SELECT proname, pg_get_function_arguments(oid) 
   FROM pg_proc 
   WHERE proname = 'match_hts_chunks';
   ```
   Should return: `match_hts_chunks(match_count integer, query_embedding vector)`

3. **Verify secrets are set correctly** in Streamlit Cloud (especially `SUPABASE_MATCH_RPC`)

4. **Run diagnostic tool locally** to ensure everything works:
   ```bash
   python diagnostic_tool.py
   ```

---

## 📊 Summary

✅ Code pushed to GitHub  
⏳ SQL script needs to be run in Supabase (CRITICAL)  
⏳ Streamlit Cloud secrets need to be updated  
⏳ App needs to be rebooted  
⏳ Test Classification AI page  

**Start with the SQL script - that's the key to fixing the "function not found" error!**
