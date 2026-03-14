import google.generativeai as genai
from typing import List
from app.core.config import GEMINI_API_KEY
from app.embeddings import search_similar_chunks

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

def general_chat(message: str) -> str:
    """Normal LLM conversation."""
    try:
        response = model.generate_content(message)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def rag_chat(message: str, website_id: str) -> dict:
    """RAG pipeline - website content se jawab do."""

    chunks = search_similar_chunks(website_id, message, top_k=5)

    print(f"Retrieved {len(chunks)} chunks for query: '{message}'")

    if not chunks:
        print("No chunks found - using general LLM")
        answer = general_chat(message)
        return {
            "response": answer,
            "sources": [],
            "mode": "general_fallback"
        }
        
    context_parts = []
    sources = []
    for i, chunk in enumerate(chunks, 1):
        context_parts.append(f"[Section {i}]:\n{chunk['text']}")
        if chunk["source"] not in sources:
            sources.append(chunk["source"])

    context = "\n\n".join(context_parts)

    prompt = f"""You are a helpful AI assistant for a business website. 
A user is asking a question about the website content.

Use the following retrieved content to answer the question accurately and helpfully.
If the exact information is not in the context, use what IS available to give the best possible answer.
Always be helpful and professional.

Retrieved Website Content:
{context}

User Question: {message}

Instructions:
- Answer based on the retrieved content above
- Be specific and detailed
- If content is partially relevant, still provide a helpful answer
- Do not say "I cannot find" unless the content is completely unrelated

Answer:"""

    try:
        response = model.generate_content(prompt)
        answer = response.text
        print(f"Answer generated ({len(answer)} chars)")
    except Exception as e:
        answer = f"Error generating response: {str(e)}"

    return {
        "response": answer,
        "sources": sources,
    }
