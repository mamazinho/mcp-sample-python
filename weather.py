from datetime import datetime, timedelta
from typing import Any

import httpx
from mcp.server.fastmcp import FastMCP

# Constants
API_BASE = "https://api.open-meteo.com/v1/forecast"

mcp = FastMCP("weather")

async def make_weather_request(url: str) -> dict[str, Any] | None:
    """
    Make a request to the OpenMeteo API and return the JSON response.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()

def format_forecast(data: dict[str, Any], city: str) -> str:
    """
    Format weather forecast into a readable string.
    """
    tomorrow_index = 1  # Index 1 represents tomorrow in daily data
    
    temp_max = data["daily"]["temperature_2m_max"][tomorrow_index]
    temp_min = data["daily"]["temperature_2m_min"][tomorrow_index]
    precipitation_prob = data["daily"]["precipitation_probability_mean"][tomorrow_index]
    wind_speed = data["daily"]["windspeed_10m_max"][tomorrow_index]
    
    return f"""
        Previsão para amanhã em {city}:
        Temperatura: Mín: {temp_min}°C, Máx: {temp_max}°C
        Probabilidade de Chuva: {precipitation_prob}%
        Velocidade do Vento: {wind_speed} km/h
    """

@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    url = f"{API_BASE}?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_mean,windspeed_10m_max&timezone=America/Sao_Paulo&start_date={tomorrow}&end_date={tomorrow}"
    
    data = await make_weather_request(url)
    return data
    if not data:
        return "Não foi possível obter a previsão do tempo para esta localização."
        
    return format_forecast(data)

if __name__ == "__main__":
    mcp.run()