def build_prompt(summary, lang):

    # language code mapping
    lang_map = {
        "en": "English",
        "hi": "Hindi",
        "gu": "Gujarati",
        "mr": "Marathi",
        "bn": "Bengali",
        "ta": "Tamil",
        "te": "Telugu",
        "kn": "Kannada",
        "ml": "Malayalam",
        "pa": "Punjabi",
    }

    language = lang_map.get(lang, "English")

    prompt = f"""
You are a senior business data analyst.

Generate business insights from the dataset analysis.

Rules:
- Return ONLY valid JSON
- Write all text in {language}
- Do NOT generate charts
- Do NOT change any numeric values
- Focus on clear insights and future predictions
- Keep the response concise

Return JSON format:

{{
  "summary": "",
  "insights": [
    {{"text": ""}},
    {{"text": ""}},
    {{"text": ""}}
  ],
  "predictions": [
    {{"text": ""}},
    {{"text": ""}}
  ]
}}

Dataset Analysis:
{summary}
"""

    return prompt
