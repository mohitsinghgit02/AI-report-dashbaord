from fastapi import APIRouter, HTTPException
import json
import re
import pandas as pd
from app.services.groq_service import generate_llm_data
from app.services.s3_loader import download_s3_file
from app.services.report_registry import REPORT_REGISTRY

router = APIRouter()


@router.get("/reports/{report_type}")
def generate_report(report_type: str, file: str, lang: str = "en"):

    if report_type not in REPORT_REGISTRY:
        raise HTTPException(status_code=400, detail="Invalid report type")

    report_service = REPORT_REGISTRY[report_type]

    local_file = f"/tmp/{file.split('/')[-1]}"

    download_s3_file(file, local_file)

    df = pd.read_csv(local_file)

    pandas_analysis = report_service.analyze(df)

    prompt = report_service.build_prompt(pandas_analysis, lang)

    ai_response = generate_llm_data(prompt)

    ai_json = parse_llm_response(ai_response)

    final_dashboard = merge_dashboard(pandas_analysis, ai_json)

    return final_dashboard


def parse_llm_response(response):

    if isinstance(response, dict):
        return response

    if isinstance(response, bytes):
        response = response.decode("utf-8")

    cleaned = re.sub(r"^```json\s*|```$", "", response.strip(), flags=re.MULTILINE)
    cleaned = re.sub(r",(\s*[\]}])", r"\1", cleaned)

    try:
        return json.loads(cleaned)
    except Exception:
        return {}


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
