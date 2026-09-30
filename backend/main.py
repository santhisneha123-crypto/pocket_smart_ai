import json
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

try:
    from google import genai
except ImportError:
    genai = None


PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

app = FastAPI(title="PocketSmart AI")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY and genai else None


class PlannerRequest(BaseModel):
    planner: str
    budget: float
    details: dict


@app.get("/")
def home():
    return FileResponse(PROJECT_ROOT / "frontend" / "index.html")


@app.post("/recommend")
def recommend(request: PlannerRequest):
    if client is None:
        return demo_recommendations(request.planner, request.budget)

    prompt = f"""
You are PocketSmart AI, a smart budget planning and recommendation assistant.

Planner: {request.planner}
Budget: ₹{request.budget}
User Requirements: {json.dumps(request.details)}

Create recommendations suitable for the user's requirements. Stay within the
budget, divide it logically, recommend useful products or services, mention
popular platforms, and briefly explain each recommendation.

Return only JSON in this format:
{{
  "budget": {request.budget},
  "allocation": {{"Category 1": 0, "Category 2": 0}},
  "recommendations": [{
    "name": "Product Name",
    "category": "Category",
    "price": 0,
    "platform": "Platform",
    "reason": "Reason"
  }]
}}
"""

    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt,
        )
        text = response.text.strip().removeprefix("```json").removesuffix("```").strip()
        return json.loads(text)
    except Exception as error:
        return {"error": f"AI recommendation failed: {error}"}


def demo_recommendations(planner: str, budget: float):
    if planner == "Home Interior":
        allocation = {
            "Furniture": round(budget * 0.40),
            "Lighting": round(budget * 0.20),
            "Decor": round(budget * 0.20),
            "Fans & Accessories": round(budget * 0.20),
        }
        recommendations = [
            {"name": "Modern LED Ceiling Light", "category": "Lighting", "price": 1200, "platform": "Amazon", "reason": "Affordable lighting option for a modern room."},
            {"name": "Ceiling Fan", "category": "Electrical", "price": 2500, "platform": "Flipkart", "reason": "Useful and budget-friendly cooling solution."},
            {"name": "Compact Dining Table", "category": "Furniture", "price": 8500, "platform": "IKEA", "reason": "Suitable for compact dining spaces."},
        ]
    elif planner == "Party Planner":
        allocation = {
            "Catering": round(budget * 0.50),
            "Decoration": round(budget * 0.25),
            "Entertainment": round(budget * 0.15),
            "Other": round(budget * 0.10),
        }
        recommendations = [
            {"name": "Party Food Package", "category": "Catering", "price": 5000, "platform": "Swiggy", "reason": "Suitable for a small party."},
            {"name": "Birthday Decoration Package", "category": "Decoration", "price": 2500, "platform": "Local Vendor", "reason": "Simple decoration within a limited budget."},
            {"name": "Hotel Room", "category": "Accommodation", "price": 3000, "platform": "OYO", "reason": "Can be used when accommodation is required."},
        ]
    else:
        allocation = {
            "Necklace": round(budget * 0.40),
            "Earrings": round(budget * 0.25),
            "Bangles": round(budget * 0.20),
            "Accessories": round(budget * 0.15),
        }
        recommendations = [
            {"name": "Elegant Necklace", "category": "Necklace", "price": 2500, "platform": "Amazon", "reason": "Simple design suitable for special occasions."},
            {"name": "Matching Earrings", "category": "Earrings", "price": 1200, "platform": "Flipkart", "reason": "Can be paired with an elegant outfit."},
            {"name": "Traditional Bangles", "category": "Bangles", "price": 900, "platform": "Amazon", "reason": "Suitable for traditional occasions."},
        ]

    return {"budget": budget, "allocation": allocation, "recommendations": recommendations}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
