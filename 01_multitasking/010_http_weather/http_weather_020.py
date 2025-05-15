import httpx
import asyncio
from dotenv import load_dotenv
import os
import time  # Import the time module

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")  # Load API key from .env
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

async def fetch_weather(city):
    """Fetch weather data for a given city."""
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "imperial"  # Use imperial units (Fahrenheit)
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            print(f"Weather in {city}: {data['weather'][0]['description']}, {data['main']['temp']}°F")
        else:
            print(f"Failed to fetch weather for {city}: {response.status_code}")

async def main():
    cities = ["New York", "London", "Tokyo", "Sydney", "Paris", "Berlin", "Mumbai", "Beijing", "Cairo", "São Paulo", "Moscow", "Los Angeles", "Cape Town", "Bangkok", "Dearborn, Michigan", "Richmond, Virginia"]
    
    start_time = time.time()  # Record the start time

    # Create a list of tasks for all cities
    tasks = []
    for city in cities:
        tasks.append(fetch_weather(city))
    
    # Run all tasks concurrently
    await asyncio.gather(*tasks)

    end_time = time.time()  # Record the end time

    print(f"\nTime taken to fetch weather for all cities: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())
