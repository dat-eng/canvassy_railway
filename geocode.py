import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time

# --------------------------------------------------
# Load CSV
# --------------------------------------------------

df = pd.read_csv(
    "data.csv",
    dtype=str,
    keep_default_na=False
)

print(f"Original rows: {len(df)}")

# --------------------------------------------------
# Build Full Address
# --------------------------------------------------

df["full_address"] = (
    df["Address"]
    + ", "
    + df["City"]
    + ", "
    + df["State"]
)

# --------------------------------------------------
# Geolocator
# --------------------------------------------------

geolocator = Nominatim(
    user_agent="canvassy_app",
    timeout=10
)

# --------------------------------------------------
# Geocode Function
# --------------------------------------------------

def geocode_address(addr):

    for attempt in range(3):

        try:

            location = geolocator.geocode(addr)

            if location:
                return (
                    location.latitude,
                    location.longitude
                )

        except GeocoderTimedOut:
            print(f"Timeout retry: {addr}")

        except Exception as e:
            print(f"Error: {addr}")
            print(e)

        time.sleep(2)

    return ("", "")

# --------------------------------------------------
# Geocode Loop
# --------------------------------------------------

latitudes = []
longitudes = []

for i, addr in enumerate(df["full_address"]):

    print(f"{i+1}/{len(df)} : {addr}")

    lat, lon = geocode_address(addr)

    latitudes.append(lat)
    longitudes.append(lon)

    time.sleep(1)

# --------------------------------------------------
# Save Coordinates
# --------------------------------------------------

df["Latitude"] = latitudes
df["Longitude"] = longitudes

# --------------------------------------------------
# Cleanup
# --------------------------------------------------

df = df.drop(columns=["full_address"])

# --------------------------------------------------
# Save Final CSV
# --------------------------------------------------

df.to_csv(
    "data_final.csv",
    index=False
)

print(f"Final rows: {len(df)}")
print("Done")