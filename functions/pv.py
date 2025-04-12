from datetime import datetime
import numpy as np
import pandas as pd
import pvlib
from pvlib.location import Location

def estimate_pv_output(
    direct_exposure_j: np.ndarray,
    date: datetime,
    latitude: float,
    longitude: float,
    tilt: float,
    azimuth: float,
    cloud_cover: np.ndarray | None = None,
    pv_efficiency: float = 0.18,
    albedo: float = 0.2
) -> np.ndarray:
    """
    Estimate hourly PV output (Wh/m²) based on hourly direct solar exposure and panel orientation.

    Parameters:
        direct_exposure_j (np.ndarray): Array of 24 hourly values in J/m².
        date (datetime): Date object for the forecast.
        latitude (float): Latitude of the PV system.
        longitude (float): Longitude of the PV system.
        tilt (float): Tilt angle of the PV panel in degrees.
        azimuth (float): Azimuth angle of the PV panel in degrees (180 = South).
        cloud_cover (np.ndarray | None): Optional array of 24 hourly cloud cover values (0–1 or 0–100).
        pv_efficiency (float): PV system efficiency (default = 0.18).
        albedo (float): Ground reflectivity (default = 0.2).

    Returns:
        np.ndarray: 24 hourly estimated PV outputs in Wh/m².
    """
    # 1. Convert direct exposure from J/m² to W/m² (assuming 1-hour intervals)
    dni = direct_exposure_j / 3600  # W/m² per hour

    # 2. Generate hourly timestamps
    times = pd.date_range(
        start=pd.Timestamp(date).replace(hour=0, minute=0, second=0),
        periods=24, freq='H', tz='UTC'
    )
    location = Location(latitude, longitude)
    times_local = times.tz_convert(location.tz)

    # 3. Solar position
    solar_position = location.get_solarposition(times_local)

    # 4. Estimate GHI roughly
    zenith_rad = np.radians(solar_position['zenith'])
    cos_zenith = np.cos(zenith_rad)
    cos_zenith[cos_zenith < 0] = 0
    ghi = dni * cos_zenith

    # 5. Estimate DHI using cloud cover if available
    if cloud_cover is not None:
        # Normalize cloud cover to [0, 1]
        cloud_fraction = np.clip(cloud_cover / (100 if cloud_cover.max() > 1 else 1), 0, 1)
        # Use an empirical formula: more clouds = more DHI (up to a point)
        # A basic assumption: clear sky = 10% of DNI; overcast = 100%
        dhi = dni * (0.1 + 0.9 * cloud_fraction)
    else:
        # Default assumption: DHI is 10% of DNI (clear-sky)
        dhi = dni * 0.1

    # 6. POA irradiance (W/m²)
    total_irradiance = pvlib.irradiance.get_total_irradiance(
        surface_tilt=tilt,
        surface_azimuth=azimuth,
        dni=dni,
        ghi=ghi,
        dhi=dhi,
        solar_zenith=solar_position['zenith'],
        solar_azimuth=solar_position['azimuth'],
        albedo=albedo
    )

    poa_irradiance = total_irradiance['poa_global'].fillna(0)

    # 7. Estimate hourly energy output (Wh/m²)
    hourly_pv_output = poa_irradiance * pv_efficiency  # W/m²
    hourly_energy_wh = hourly_pv_output  # 1-hour intervals: W = Wh

    return hourly_energy_wh.values
