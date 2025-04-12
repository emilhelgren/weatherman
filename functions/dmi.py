
import os
import requests 

from functions.util import get_formatted_date


async def getGlobalRadiationFlux(lat, lon, date):
    API_KEY = os.getenv("FORECAST_EDR_API_KEY")
    datestr = get_formatted_date(date)
    url = f"https://dmigw.govcloud.dk/v1/forecastedr/collections/harmonie_dini_sf/position?parameter-name=global-radiation-flux&datetime={datestr}&crs=crs84&f=GeoJSON&api-key={API_KEY}&coords=POINT({lat} {lon})"
    response = requests.get(url)
    responseJson = response.json()
    data = []
    rawdata = []
    last_value = responseJson["features"][0]["properties"]["global-radiation-flux"]
    for datapoint in responseJson["features"]:
        rawdata.append(datapoint["properties"]["global-radiation-flux"] - last_value)
        data.append({
            "time": datapoint["properties"]["step"],
            "cumulated": datapoint["properties"]["global-radiation-flux"],
            "value": datapoint["properties"]["global-radiation-flux"] - last_value
        })
        last_value = datapoint["properties"]["global-radiation-flux"]
    return data, rawdata



async def getDirectSolarExposure(lat, lon, date):
    API_KEY = os.getenv("FORECAST_EDR_API_KEY")
    datestr = get_formatted_date(date)
    url = f"https://dmigw.govcloud.dk/v1/forecastedr/collections/harmonie_dini_sf/position?parameter-name=direct-solar-exposure&datetime={datestr}&crs=crs84&f=GeoJSON&api-key={API_KEY}&coords=POINT({lat} {lon})"
    response = requests.get(url)
    responseJson = response.json()
    data = []
    rawdata = []
    last_value = responseJson["features"][0]["properties"]["direct-solar-exposure"]
    for datapoint in responseJson["features"]:
        rawdata.append(datapoint["properties"]["direct-solar-exposure"] - last_value)
        data.append({
            "time": datapoint["properties"]["step"],
            "cumulated": datapoint["properties"]["direct-solar-exposure"],
            "value": datapoint["properties"]["direct-solar-exposure"] - last_value
        })
        last_value = datapoint["properties"]["direct-solar-exposure"]
    return data, rawdata
