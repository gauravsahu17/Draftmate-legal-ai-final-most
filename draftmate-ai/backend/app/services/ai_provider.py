import httpx
from ..config import settings
class AIUnavailable(Exception): pass
async def generate(system: str, prompt: str) -> str:
    if not settings.ai_api_key: raise AIUnavailable("AI provider is not configured. Add AI_API_KEY to backend/.env to enable generation.")
    try:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(settings.ai_base_url.rstrip("/") + "/chat/completions", headers={"Authorization": f"Bearer {settings.ai_api_key}", "Content-Type": "application/json"}, json={"model": settings.ai_model, "messages": [{"role":"system","content":system},{"role":"user","content":prompt}]})
        if response.status_code == 429: raise AIUnavailable("AI provider rate limit reached. Please retry later.")
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except AIUnavailable: raise
    except httpx.TimeoutException as exc: raise AIUnavailable("AI provider timed out. Please retry.") from exc
    except (httpx.HTTPError, KeyError, IndexError, ValueError) as exc: raise AIUnavailable("AI provider request failed. Check settings and provider availability.") from exc
