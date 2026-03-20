from groq import Groq
import os

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def generate_llm_data(prompt):

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    return completion.choices[0].message.content
