from datetime import datetime
import json
from fastapi import FastAPI
import redis
import numpy as np

from dotenv import load_dotenv

from functions.aws import upload_file_to_bucket
from functions.cache import Cache
from functions.dmi import getDirectSolarExposure, getGlobalRadiationFlux
from functions.opencage import address_to_coords
from functions.plotting import hourly_pv_plot
from functions.pv import estimate_pv_output
from functions.util import print_column_graph

load_dotenv()

app = FastAPI()
cache = Cache()

@app.get("/forecast/coors")
async def get_forecast(lat: float=12.561, lon: float=55.715, date: str="2025-03-13"):
    try:
        directSolarExposure = await getDirectSolarExposure(lat, lon, date)
        return {"directSolarExposure": directSolarExposure, "lat": lat, "lon": lon, "date": date}
    except Exception as e:
        return {"error": str(e)}

@app.get("/forecast/address")
async def get_forecast(address: str, datestr: str="2025-03-13", tilt: float=35, orientation: str=["south", "west", "east"], kwp: float=1.0):
    try:
        # Get date from datestr
        date = datetime.strptime(datestr, '%Y-%m-%d')

        # Get coords from address
        cached_item = cache.get(address)
        if cached_item:
            print("Using cached coords for address", address)
            coords = eval(cached_item)
        else:
            print("Fetching coords for address", address)
            coords = await address_to_coords(address)
            cache.setex(address, 120, str(coords))
        lat = coords["lat"]
        lon = coords["lng"]

        data, rawData = await getDirectSolarExposure(lat, lon, date)

        orientation_angle = 180 if orientation == "south" else 90 if orientation == "east" else 270 if orientation == "west" else 0
        # Convert rawData to np array and multiply by conversion and kwp
        production_forecast = estimate_pv_output(np.array(rawData), date, lat, lon, tilt, orientation_angle) * kwp
        print(production_forecast)
        print(type(production_forecast))
        print_column_graph(list(production_forecast))
        file_path, title = hourly_pv_plot(production_forecast, "PV Production Forecast", "Production (Wh)", "Hour", "pv_production_forecast")
        # Upload pdf file to S3
        with open(file_path, "rb") as f:
            file_contents = f.read()
        upload_file_to_bucket("weatherman-bucket", f"{title}_{lat}_{lon}_{datestr}.pdf", file_contents)
        json_data = json.dumps(data, indent=2)
        upload_file_to_bucket("weatherman-bucket", f"{title}_{lat}_{lon}_{datestr}.json", json_data)

        # Cache 
        return {"forecast": list(production_forecast),
                "total": sum(production_forecast),
                "lat": lat, 
                "lon": lon, 
                "address": address, 
                "date": date,
                "pdf_url": f"https://weatherman-bucket.s3.eu-north-1.amazonaws.com/{str.replace(title, ' ', '+')}_{lat}_{lon}_{datestr}.pdf",
                "json_url": f"https://weatherman-bucket.s3.eu-north-1.amazonaws.com/{str.replace(title, ' ', '+')}_{lat}_{lon}_{datestr}.json"
                }
    except Exception as e:
        return {"error in endpoint": str(e)}
    


@app.get("/coords")
async def get_coords(address: str):
    try:
        print("address", address)
        cached_item = cache.get(address)
        if cached_item:
            return {"address": address, "coords": eval(cached_item), "cached": True}
        coords = await address_to_coords(address)
        cache.setex(address, 120, str(coords))
        return {"address": address, "coords": coords, "cached": False}
    except Exception as e:
        return {"error": str(e)}