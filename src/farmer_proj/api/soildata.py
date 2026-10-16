import os
import requests
from farmer_proj.api.geocoding import get_coordinates

def get_soil_info(lat:float, lon:float):
    url =f"https://rest.isric.org/soilgrids/v2.0/properties/query?lat={lat}&lon={lon}&property=phh2o&property=clay&property=sand&depth=0-5cm&value=mean"

    print("Sending request...")

    response = requests.get(url,  timeout=30)

    print("Status code:", response.status_code)
    
    data = response.json()

    if data :
        print(data)
    else:
        raise ValueError("could not fetch soil data")



get_soil_info(52.3676,4.9041)