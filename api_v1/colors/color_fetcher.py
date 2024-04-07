import httpx
from fastapi import HTTPException

API_URL = "https://www.thecolorapi.com/id"


async def fetch_color_title(hex_color: str) -> str:
    async with httpx.AsyncClient() as client:
        params = {"hex": hex_color, "format": "json"}
        response = await client.get(API_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        title = data.get("name", {}).get("value")
        if title:
            return title
        else:
            raise HTTPException(
                status_code=400, detail="Failed to fetch color title from API"
            )
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail="Failed to fetch color title from API",
        )
