#!/usr/bin/env python3
"""
HTS Dashboard - Supabase RPC Diagnostic Tool

This script tests your Supabase connection and RPC function before deploying
to Streamlit Cloud. Run this locally to verify everything works correctly.

Usage:
    python diagnostic_tool.py
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv(".hts_dashboard/.env")

def check_env_vars():
    """Verify all required environment variables are set."""
    print("=" * 70)
    print("STEP 1: Checking Environment Variables")
    print("=" * 70)
    
    required_vars = [
        "SUPABASE_URL",
        "SUPABASE_SERVICE_ROLE_KEY",
        "OPENAI_API_KEY",
        "EMBEDDING_MODEL",
        "EMBEDDING_DIM",
        "SUPABASE_TABLE"
    ]
    
    optional_vars = ["SUPABASE_MATCH_RPC"]
    
    missing = []
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # Mask sensitive values
            if "KEY" in var or "SECRET" in var:
                display_value = value[:8] + "..." + value[-4:] if len(value) > 12 else "***"
            else:
                display_value = value
            print(f"✅ {var}: {display_value}")
        else:
            print(f"❌ {var}: NOT SET")
            missing.append(var)
    
    for var in optional_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: {value}")
        else:
            print(f"⚠️  {var}: NOT SET (using default)")
    
    if missing:
        print(f"\n❌ Missing required environment variables: {', '.join(missing)}")
        return False
    
    print("\n✅ All required environment variables are set!\n")
    return True


def test_supabase_connection():
    """Test basic Supabase connection."""
    print("=" * 70)
    print("STEP 2: Testing Supabase Connection")
    print("=" * 70)
    
    try:
        from supabase import create_client
        
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        table = os.getenv("SUPABASE_TABLE", "hts_knowledge_chunks")
        
        supabase = create_client(url, key)
        
        # Test table access
        result = supabase.table(table).select("id").limit(1).execute()
        
        if result.data:
            print(f"✅ Successfully connected to Supabase")
            print(f"✅ Table '{table}' is accessible")
            print(f"   Sample record ID: {result.data[0]['id']}")
        else:
            print(f"⚠️  Connected to Supabase but table '{table}' appears empty")
        
        return True
        
    except Exception as e:
        print(f"❌ Supabase connection failed: {e}")
        return False


def test_openai_embeddings():
    """Test OpenAI embedding generation."""
    print("\n" + "=" * 70)
    print("STEP 3: Testing OpenAI Embeddings")
    print("=" * 70)
    
    try:
        from openai import OpenAI
        
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        model = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")
        expected_dim = int(os.getenv("EMBEDDING_DIM", "1536"))
        
        print(f"   Model: {model}")
        print(f"   Expected dimension: {expected_dim}")
        
        # Generate test embedding
        response = client.embeddings.create(
            model=model,
            input="test query for HTS classification"
        )
        
        vector = response.data[0].embedding
        actual_dim = len(vector)
        
        print(f"✅ Successfully generated embedding")
        print(f"   Actual dimension: {actual_dim}")
        
        if actual_dim == expected_dim:
            print(f"✅ Dimension matches expected value!")
        else:
            print(f"❌ Dimension mismatch! Expected {expected_dim}, got {actual_dim}")
            print(f"   Update your EMBEDDING_DIM environment variable to {actual_dim}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ OpenAI embedding generation failed: {e}")
        return False


def test_rpc_function():
    """Test the Supabase RPC function."""
    print("\n" + "=" * 70)
    print("STEP 4: Testing Supabase RPC Function")
    print("=" * 70)
    
    try:
        from supabase import create_client
        from openai import OpenAI
        
        # Initialize clients
        supabase = create_client(
            os.getenv("SUPABASE_URL"),
            os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        )
        
        openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Generate test embedding
        model = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")
        response = openai_client.embeddings.create(
            model=model,
            input="plastic bottle for water"
        )
        vector = response.data[0].embedding
        
        # Test RPC call
        rpc_name = os.getenv("SUPABASE_MATCH_RPC", "match_hts_chunks")
        print(f"   RPC function: {rpc_name}")
        print(f"   Parameters: match_count=5, query_embedding=vector({len(vector)})")
        
        result = supabase.rpc(
            rpc_name,
            {
                "match_count": 5,
                "query_embedding": vector,
            }
        ).execute()
        
        if result.data:
            print(f"✅ RPC function call successful!")
            print(f"   Returned {len(result.data)} results")
            
            # Display first result
            if len(result.data) > 0:
                first = result.data[0]
                print(f"\n   Sample result:")
                print(f"   - HTS Code: {first.get('hts_code', 'N/A')}")
                print(f"   - Title: {first.get('title', 'N/A')[:60]}...")
                if 'similarity' in first:
                    print(f"   - Similarity: {first['similarity']:.4f}")
        else:
            print(f"⚠️  RPC function returned no results")
            print(f"   This might mean your table is empty or the function isn't working correctly")
        
        return True
        
    except Exception as e:
        error_msg = str(e).lower()
        print(f"❌ RPC function call failed!")
        print(f"   Error: {e}")
        
        if "could not find the function" in error_msg:
            print(f"\n   🔍 DIAGNOSIS: Function not found in schema cache")
            print(f"   📋 ACTION REQUIRED:")
            print(f"      1. Run supabase_rpc_fix.sql in your Supabase SQL Editor")
            print(f"      2. Verify the function signature matches: (match_count int, query_embedding vector)")
            print(f"      3. Ensure parameters are in ALPHABETICAL order")
        
        return False


def main():
    """Run all diagnostic tests."""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "HTS DASHBOARD DIAGNOSTIC TOOL" + " " * 24 + "║")
    print("╚" + "=" * 68 + "╝")
    print()
    
    results = []
    
    # Run tests
    results.append(("Environment Variables", check_env_vars()))
    
    if results[-1][1]:  # Only continue if env vars are set
        results.append(("Supabase Connection", test_supabase_connection()))
        results.append(("OpenAI Embeddings", test_openai_embeddings()))
        results.append(("RPC Function", test_rpc_function()))
    
    # Summary
    print("\n" + "=" * 70)
    print("DIAGNOSTIC SUMMARY")
    print("=" * 70)
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status}: {test_name}")
        if not passed:
            all_passed = False
    
    print("=" * 70)
    
    if all_passed:
        print("\n🎉 All tests passed! Your setup is ready for Streamlit Cloud deployment.")
        print("\n📋 Next steps:")
        print("   1. Commit and push your code changes")
        print("   2. Update Streamlit Cloud secrets with all environment variables")
        print("   3. Deploy to Streamlit Cloud")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above before deploying.")
        print("\n📋 Common fixes:")
        print("   - Run supabase_rpc_fix.sql in Supabase SQL Editor")
        print("   - Verify all environment variables in .env file")
        print("   - Check Supabase table has data with embeddings")
        return 1


if __name__ == "__main__":
    sys.exit(main())
