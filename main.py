from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
import asyncio
import parser
import logging

app = FastAPI(
    title="Weather parser",
    root_path='/weather_api',
    version="1.0",
    docs_url=None,
    openapi_url=None,
    redoc_url=None
)


@app.exception_handler(Exception)
async def handle_exception(request, exc):
    logging.exception(exc)
    return JSONResponse(status_code=500, content={"message": "Internal Server Error"})


async def fetch_and_parse_data():
    weather_fetcher = parser.WeatherDataFetcher()
    await weather_fetcher.fetch_data()
    weather_fetcher.parse_data()
    return weather_fetcher

@app.get("/")
async def get_weather():
    fetcher = await fetch_and_parse_data()

    temperature = fetcher.get_temperature()
    temp_status = fetcher.get_temperature_status()
    wind = fetcher.get_wind()
    air_pressure = fetcher.get_air_pressure()
    return {
        "temperature": temperature,
        "temp_status": temp_status,
        "wind": wind,
        "air_pressure": air_pressure,
    }


@app.get("/temperature")
async def get_temperature() -> dict[str, str]:
    fetcher = await fetch_and_parse_data()
    return {"temperature": fetcher.get_temperature()}

@app.get("/temp_status")
async def get_temp_status() -> dict[str, str]:
    fetcher = await fetch_and_parse_data()
    return {"temp_status": fetcher.get_temperature_status()}

@app.get("/wind")
async def get_wind() -> dict[str, str]:
    fetcher = await fetch_and_parse_data()
    return {"wind": fetcher.get_wind()}

@app.get("/air_pressure")
async def get_air_pressure() -> dict[str, str]:
    fetcher = await fetch_and_parse_data()
    return {"air_pressure": fetcher.get_air_pressure()}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_level="debug",
        reload=True,
    )
