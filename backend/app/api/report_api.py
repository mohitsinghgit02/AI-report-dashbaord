from fastapi import APIRouter, HTTPException
import json
import re
from app.services.data_loader import load_csv
from app.services.pandas_analyzer import analyze_data
from app.services.prompt_builder import build_prompt
from app.services.groq_service import generate_html_dashboard
from app.services.html_validator import sanitize_html

router = APIRouter()


@router.get("/report")
def generate_report(file: str, lang: str = "en"):

    df = load_csv(file)

    pandas_analysis = analyze_data(df)

    if "error" in pandas_analysis:
        return pandas_analysis

    prompt = build_prompt(pandas_analysis, lang)

    ai_response = generate_html_dashboard(prompt)

    ai_json = parse_llm_response(ai_response)

    final_dashboard = merge_dashboard(pandas_analysis, ai_json)

    return final_dashboard


def parse_llm_response(response):
    """
    Parse LLM JSON response safely.
    Accepts str, bytes, or dict.
    Returns dict or None.
    """

    print("Raw LLM response:", response)
    # Already a dict → return as-is
    if isinstance(response, dict):
        return response

    # If bytes → decode
    if isinstance(response, bytes):
        response = response.decode("utf-8")

    # Must be string now
    if not isinstance(response, str):
        print("Error: response must be str, bytes, or dict.")
        return None

    # Remove ```json or ``` wrapping
    cleaned = re.sub(r"^```json\s*|```$", "", response.strip(), flags=re.MULTILINE)

    # Remove trailing commas before closing braces/brackets
    cleaned = re.sub(r",(\s*[\]}])", r"\1", cleaned)

    # Validate it looks like JSON
    if not cleaned.startswith("{") and not cleaned.startswith("["):
        print("Error: JSON does not start with { or [")
        print("Raw response:", response)
        return None

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        print("JSON Decode Error:", e)
        print("Cleaned response:", cleaned)
        return None


def merge_dashboard(pandas_data, ai_data):

    return {
        "title": "AI Generated Data Dashboard",
        "overview": pandas_data["overview"],
        "kpis": pandas_data["kpis"][:3],
        "charts": pandas_data["charts"],
        "summary": ai_data.get("summary"),
        "insights": ai_data.get("insights"),
        "predictions": ai_data.get("predictions"),
    }
