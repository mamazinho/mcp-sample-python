from datetime import datetime, timedelta
from typing import Any

import httpx
from mcp.server.fastmcp import FastMCP

# Constants
API_BASE = "https://api.open-meteo.com/v1/forecast"

mcp = FastMCP("weather")

async def _get_forecast_on_meteo(url: str) -> dict[str, Any] | None:
    """
    Make a request to the OpenMeteo API and return the JSON response.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """    
    url = f"{API_BASE}?latitude={latitude}&longitude={longitude}"
    
    return await _get_forecast_on_meteo(url)

if __name__ == "__main__":
    mcp.run()