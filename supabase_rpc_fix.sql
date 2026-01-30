-- ============================================================================
-- HTS Dashboard - Supabase RPC Function Fix
-- ============================================================================
-- This script creates/recreates the match_hts_chunks function with the correct
-- parameter order to work with the Supabase Python client.
--
-- CRITICAL: The Supabase Python client passes parameters in ALPHABETICAL order.
-- Therefore, the function signature MUST have parameters alphabetically ordered:
--   1. match_count (comes before 'q' alphabetically)
--   2. query_embedding (comes after 'm' alphabetically)
--
-- Run this in your Supabase SQL Editor to ensure the function exists with
-- the correct signature.
-- ============================================================================

-- Enable pgvector extension if not already enabled
CREATE EXTENSION IF NOT EXISTS vector;

-- Drop existing function if it exists (to recreate with correct signature)
DROP FUNCTION IF EXISTS public.match_hts_chunks(vector, int);
DROP FUNCTION IF EXISTS public.match_hts_chunks(int, vector);

-- Optional: Drop and recreate index to ensure it's clean (run separately if needed)
-- DROP INDEX IF EXISTS hts_knowledge_chunks_embedding_idx;

-- Create the function with ALPHABETICALLY ORDERED parameters
-- This matches how the Supabase Python client will call it
CREATE OR REPLACE FUNCTION public.match_hts_chunks(
  match_count int,           -- First parameter (alphabetically)
  query_embedding vector(1536) -- Second parameter (adjust dimension if needed)
)
RETURNS TABLE (
  id bigint,
  hts_code text,
  title text,
  normalized_text text,
  embedding vector(1536),
  similarity float
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    hts_knowledge_chunks.id,
    hts_knowledge_chunks.hts_code,
    hts_knowledge_chunks.title,
    hts_knowledge_chunks.normalized_text,
    hts_knowledge_chunks.embedding,
    1 - (hts_knowledge_chunks.embedding <=> query_embedding) AS similarity
  FROM hts_knowledge_chunks
  ORDER BY hts_knowledge_chunks.embedding <=> query_embedding
  LIMIT match_count;
END;
$$;

-- Grant execute permissions to authenticated and anon users
GRANT EXECUTE ON FUNCTION public.match_hts_chunks(int, vector) TO authenticated;
GRANT EXECUTE ON FUNCTION public.match_hts_chunks(int, vector) TO anon;

-- ============================================================================
-- Verification Queries
-- ============================================================================

-- 1. Verify the function exists with correct signature
SELECT 
  p.proname AS function_name,
  pg_get_function_arguments(p.oid) AS parameters,
  pg_get_function_result(p.oid) AS return_type
FROM pg_proc p
JOIN pg_namespace n ON p.pronamespace = n.oid
WHERE n.nspname = 'public' 
  AND p.proname = 'match_hts_chunks';

-- 2. Test the function with a dummy vector (adjust dimension as needed)
-- This should return results if you have data in hts_knowledge_chunks
-- SELECT * FROM public.match_hts_chunks(
--   5,  -- match_count
--   (SELECT embedding FROM hts_knowledge_chunks WHERE embedding IS NOT NULL LIMIT 1)
-- );

-- 3. Cleanup & Re-indexing (RUN THESE IF REBUILDING FROM SCRATCH)
-- a. Clear stale embeddings if starting a full re-embed
-- UPDATE hts_knowledge_chunks SET embedding = NULL;

-- b. Create HNSW index for fast similarity search
-- CREATE INDEX hts_knowledge_chunks_embedding_idx ON hts_knowledge_chunks 
-- USING hnsw (embedding vector_cosine_ops)
-- WITH (m = 16, ef_construction = 64);

-- ============================================================================
-- Notes
-- ============================================================================
-- 
-- If you're using a different embedding dimension (e.g., 3072 for text-embedding-3-large),
-- update both occurrences of vector(1536) to vector(YOUR_DIMENSION).
--
-- Common OpenAI embedding dimensions:
-- - text-embedding-ada-002: 1536
-- - text-embedding-3-small: 1536
-- - text-embedding-3-large: 3072
--
-- Make sure your EMBEDDING_DIM environment variable matches the dimension here.
-- ============================================================================
