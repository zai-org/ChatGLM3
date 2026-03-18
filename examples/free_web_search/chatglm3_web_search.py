"""
ChatGLM3 + Free Web Search Example (v13.0.0)
Zero-cost, API-key-free real-time web search for ChatGLM3.
"""
from transformers import AutoTokenizer, AutoModel
from free_web_search_ultimate import UltimateSearcher

# Initialize searcher — no API key needed!
searcher = UltimateSearcher()

def search_and_answer(model, tokenizer, question: str) -> str:
    """Search the web and use ChatGLM3 to generate a grounded answer."""
    # Step 1: Search the web
    results = searcher.search(question, engine="duckduckgo", max_results=3)
    context = "\n\n".join([
        f"Source: {r['url']}\n{r['snippet']}"
        for r in results
    ])
    
    # Step 2: Build prompt with search context
    prompt = f"""Based on the following web search results, answer the question.

Search Results:
{context}

Question: {question}
Answer:"""
    
    # Step 3: Generate answer with ChatGLM3
    response, _ = model.chat(tokenizer, prompt, history=[])
    return response

if __name__ == "__main__":
    # Install: pip install free-web-search-ultimate==13.0.0 transformers
    # PyPI: https://pypi.org/project/free-web-search-ultimate/
    print("ChatGLM3 + free-web-search-ultimate demo")
    print("Search: 'Latest AI developments in 2025'")
    results = searcher.search("Latest AI developments in 2025", engine="duckduckgo", max_results=3)
    for r in results:
        print(f"  - {r['title']}: {r['url']}")
