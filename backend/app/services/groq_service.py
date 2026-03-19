from groq import Groq
import os

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def generate_html_dashboard(prompt):

    print(f"Generating HTML dashboard with prompt: {prompt}")
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    print(f"Received completion: {completion.choices[0].message.content}")

    return completion.choices[0].message.content
