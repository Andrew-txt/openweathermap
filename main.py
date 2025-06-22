from fastapi import FastAPI, HTTPException
import requests
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()
KEY = 'b29fe587deb6be040d1133081ac8ace8'


@app.get("/weather")
async def weather(query: str) -> JSONResponse:
    """
    Asynchronous HTTP-request, get the weather in city.

    Args:
        query: Search string

    Returns:
        JSONResponse with city, temp, pressure and wind speed.

    Raises:
        HTTPException: If request fails or parsing error occurs
    """
    try:
        response = requests.get(
            "http://api.openweathermap.org/data/2.5/weather",
            params={
                "q": query,
                "appid": KEY,
                "units": "metric"
            }
        )

        data = response.json()

        if response.status_code != 200:
            raise HTTPException(status_code=400, detail=data.get("message", "Ошибка API"))

        return JSONResponse(
            {
                "data": {
                    "city": query,
                    "temp": data["main"]["temp"],
                    "pressure": round(data["main"]["pressure"] * 0.750062, 2),
                    "wind_speed": data["wind"]["speed"]
                }
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7682)