# 🌱 Material Analysis API

This is a FastAPI-based backend service that uses **LLM (via OpenRouter/DeepSeek)** to analyze product descriptions and determine their **biodegradability**, **decomposition time**, **disposal methods**, and **eco-friendly tips**.

It is part of a larger project to help users make **sustainable and informed choices** when shopping or disposing of materials.

---

## 🚀 API Endpoint

### `POST /analyze-material/`

**Description**:  
Analyzes a product or material description and returns eco-related insights.

### ✅ Request

```json
POST /analyze-material/
Content-Type: application/json

{
  "description": "A plastic water bottle made from PET with a polyethylene cap."
}
