from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.report_api import router as report_router
from app.api.chat_api import router as chat_router

app = FastAPI(title="AI Report Generator", version="1.0")

# CORS configuration
origins = ["http://localhost:3000", "http://127.0.0.1:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(report_router, prefix="/api")
app.include_router(chat_router, prefix="/api")


@app.get("/")
def health():
    return {"status": "running"}
