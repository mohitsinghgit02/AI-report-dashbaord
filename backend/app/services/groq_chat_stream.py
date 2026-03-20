from groq import Groq
import os
import json

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def stream_chat(question, pandas_analysis):
    """
    Streams LLM response token-by-token for the chat UI.
    The model is instructed to return well formatted Markdown.
    """

    # Convert dataset summary to JSON string
    context = json.dumps(pandas_analysis)

    # Small prompt to keep token usage low
    prompt = f"""
Dataset summary:
{context}

User question:
{question}

Instructions:
- Answer in SIMPLE LANGUAGE so that commmon man can understand.
- Answer using dataset information ONLY.
- Format response in clean Markdown.
- Use headings (## or ###) to structure the answer.
- Use bullet points for insights.
- Use Markdown tables for numeric comparisons.
- Highlight important values using **bold**.
- Use emojis/icons when useful (📊 📈 💡).
"""

    stream = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful data analyst that produces clear Markdown formatted answers.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        stream=True,
    )

    # Stream tokens back to frontend
    for chunk in stream:

        if not chunk.choices:
            continue

        delta = chunk.choices[0].delta

        if delta.content:
            yield delta.content
