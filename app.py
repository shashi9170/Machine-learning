from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import json
import requests
import re


load_dotenv()

app = FastAPI()

const allowedOrigins = [
  'http://localhost:5173',
  'http://localhost:5174',
  'http://localhost:3000',
  'https://hack-on-sustainable-shopping-experi.vercel.app',
  'https://hack-on-sustainable-git-9d5060-sachin-singhs-projects-a8578191.vercel.app',
  'https://hack-on-sustainable-shopping-experience-bhr7csnmr.vercel.app'
];

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowedOrigins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MaterialRequest(BaseModel):
    description: str

@app.get("/")
async def home():
    return {"message": "Welcome to the Material Analysis API"}

@app.post("/analyze-material/")
async def analyze_material(data: MaterialRequest):
    headers = {
        "Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}",
        "Content-Type": "application/json",
        "X-Title": "EcoMaterialScanner"       
    }

    payload = {
        "model": "deepseek/deepseek-chat",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an environmental assistant. Based on the material composition provided, "
                    "respond ONLY in a valid JSON object with the following fields:\n\n"
                    "{\n"
                    '  "biodegradable": true or false,\n'
                    '  "degrades_in": "string",\n'
                    '  "disposal": "string",\n'
                    '  "eco_tip": "string"\n'
                    "}\n\n"
                    "Return ONLY the JSON. Do not include markdown, explanation, or anything else."
                )
            },
            {
                "role": "user",
                "content": data.description
            }
        ]
    }

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload)
        )

        if response.status_code != 200:
            return {"success": False, "error": f"OpenRouter error: {response.text}"}

        raw = response.json()
        content = raw["choices"][0]["message"]["content"]

        try:
            result = json.loads(content)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", content, re.DOTALL)
            if not match:
                return {"success": False, "error": "Model did not return any JSON object"}
            result = json.loads(match.group(0))

        return {"success": True, "data": result}

    except Exception as e:
        return {"success": False, "error": str(e)}
