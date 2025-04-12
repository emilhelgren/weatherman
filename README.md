This project uses UV [source:https://docs.astral.sh/uv/] as the package manager.


## Setup
- run: uv sync
- Make sure you have access to DMI EDR forecast API, and Opencage API, as well as an AWS S3 bucket, and then set the following environment variables:
* FORECAST_EDR_API_KEY
* OPENCAGE_API_KEY
* AWS_ACCESS_KEY_ID
* AWS_SECRET_ACCESS_KEY
- If you want to use cache, launch a redis client using: docker run -p 6379:6379 -it redis/redis-stack:latest
- run: fastapi dev
- Example of a valid request: 
GET: http://localhost:8000/forecast/address?address=Brorsonsgade%201%2C%201624%20K%C3%B8benhavn%20V&tilt=35&orientation=east&datestr=YYYY-MM-DD
## Concept

### Step 1
Convert a parameter from the forecastedr api into an hourly production forecast for some PV panel in a chosen location for the coming day
- input: GPS location in CRS84, example POINT(12.561 55.715) ✅
- make API call for ~~direct-solar-exposure~~ global-radiation-flux ✅
- disaggregate into hourly values ✅
- convert to production using ~~efficiency, angle?, area ❓~~ some conversion factor ✅

### Step 2
Add address->GPS converter ✅

### Step 3 
Add cache using node-cache ✅
Cache coords for a specific address ✅

### Step 4
Add PV panel parameters such as:
* tilt ✅
* orientation ✅
* scale by Wp ✅
* Time of year mask ✅

### Step 4x (expansion)
Use the old DTU project to account for specific location shadows using height data.
Tune the conversion factor to be something accurate.

### Step 5
Setup a storage bucket on AWS to save plots and data in ✅ 
Fix so unavailable cache doesn't error ✅ 
Create some simple plots and save them in the bucket along with the data ✅ 
Return the URL of the bucket in the response ✅ 

### Step 6
Make some good error handling for invalid requests.

### Step 7
Set up a CRON job on Azure that fetches data every day to basically gather historical forecast data

### Step 8
Fetch production data somewhere as well, so I can setup some data mining on the forecasting features

## Useful parameters:

78. direct-solar-exposure
Direct solar exposure is the time integral of direct solar irradiance. Direct Solar Irradiance is the solar flux per unit area received from the solid angle of the Sun's disc on a surface normal to the sun direction. Not present on first model step.
Joule pr. square metres

84. global-radiation-flux:
Global radiation flux is the total amount of solar radiation that reaches the Earths surface. It is the sum of the direct solar radiation and diffuse solar radiation, which is solar radiation scattered throughout the atmosphere.
https://codes.ecmwf.int/grib/param-db/?id=3117
Watt pr. square metres

