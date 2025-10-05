from fastapi import Header, HTTPException

API_KEY = "demo-secret-key"

async def api_key_guard(x_api_key: str | None = Header(default=None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
