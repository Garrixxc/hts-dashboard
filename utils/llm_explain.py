"""
HTS Dashboard - LLM-Powered Classification Explanations

This module uses OpenAI to generate human-readable explanations for why
a product matches a particular HTS code.
"""

import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def explain_classification(
    product_description: str,
    hts_code: str,
    hts_title: str,
    context: str = "",
    model: str = "gpt-4o-mini"
) -> str:
    """
    Generate a detailed explanation for why a product matches an HTS code.
    
    Args:
        product_description: The product description provided by the user
        hts_code: The HTS code being explained
        hts_title: The title/description of the HTS code
        context: Additional context from the HTS database (optional)
        model: OpenAI model to use (default: gpt-4o-mini for speed/cost)
    
    Returns:
        Markdown-formatted explanation
    """
    
    prompt = f"""You are an expert in HTS (Harmonized Tariff Schedule) classification for international trade and customs.

A user is trying to classify the following product:
**Product Description:** {product_description}

The semantic search system has suggested this HTS code:
**HTS Code:** {hts_code}
**HTS Title:** {hts_title}

{f'**Additional Context:** {context}' if context else ''}

Please provide a clear, concise explanation (3-4 paragraphs) covering:

1. **Why this classification makes sense**: Explain the key factors that make this HTS code appropriate for the product (material composition, intended use, technical specifications, etc.)

2. **Key matching factors**: Highlight specific words or characteristics from the product description that align with the HTS code requirements

3. **Important considerations**: Mention any HTS notes, exclusions, or edge cases the user should be aware of

4. **Confidence assessment**: Based on the product description, rate how confident you are in this classification (High/Medium/Low) and explain why

5. **Alternative codes to consider** (if applicable): Briefly mention if there are any similar HTS codes that might also be relevant

Format your response in clear markdown with headers. Be specific and practical."""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert HTS classification specialist. Provide clear, actionable explanations."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,  # Lower temperature for more consistent, factual responses
            max_tokens=1000,
        )
        
        explanation = response.choices[0].message.content
        return explanation
        
    except Exception as e:
        return f"""
### ⚠️ Error Generating Explanation

Unable to generate explanation: {str(e)}

Please try again or contact support if the issue persists.
"""


def generate_search_variations(query: str, num_variations: int = 3) -> list[str]:
    """
    Generate alternative search queries to improve recall.
    Used for multi-vector fallback when initial search has low confidence.
    
    Args:
        query: Original search query
        num_variations: Number of alternative queries to generate
    
    Returns:
        List of alternative query strings
    """
    
    prompt = f"""Given this product search query: "{query}"

Generate {num_variations} alternative ways to search for the same product in an HTS database.
Consider:
- Synonyms for materials (e.g., "plastic" → "polymeric material", "resin")
- Alternative use cases
- Technical terminology
- Broader or more specific terms

Return ONLY the alternative queries, one per line, without numbering or explanation."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a search query optimization expert for HTS classification."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=200,
        )
        
        variations = response.choices[0].message.content.strip().split('\n')
        # Clean up the variations
        variations = [v.strip().strip('-').strip() for v in variations if v.strip()]
        
        return variations[:num_variations]
        
    except Exception as e:
        print(f"Error generating search variations: {e}")
        # Fallback: return original query
        return [query]
