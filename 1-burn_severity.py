"""Burn Severity"""

__author__ = "Ryan Milia"

""" Date: March 06, 2025
    Description:
    This module prints a burn severity map based on Sentinel-2 imagery.
    - Downloads Sentinel-2 imagery for the specified time and geography.
    - Resamples SWIR bands from 20m to 10m resolution.
    - Calculates the pre-fire NBR, post-fire NBR, and burn severity. 
    - Prints a burn severity map based on the NBR calculation.
"""
import pystac_client
import planetary_computer
import rasterio
from rasterio.mask import mask
from rasterio.warp import reproject, Resampling
import numpy as np
from shapely.geometry import box
import geopandas as gpd

# Connect to the STAC catalog
catalog = pystac_client.Client.open(
    "https://planetarycomputer.microsoft.com/api/stac/v1",
    modifier=planetary_computer.sign_inplace
)

# Define the date range for the fire
start_date = "2023-05-24T00:00:00Z"
end_date = "2023-07-30T23:59:59Z"

# Search for Sentinel-2 images by ID
search = catalog.search(
    collections=['sentinel-2-l2a'],
    ids=[
        'S2B_MSIL2A_20230518T151659_R025_T19TGJ_20230518T234549',  # Pre-fire
        'S2B_MSIL2A_20230806T151659_R025_T19TGJ_20230806T211758'   # Post-fire
    ]
)

items = search.item_collection()
print(f'{len(items)} items found')

# Define spatial extent (EPSG:32619)
bounds = [767760.0, 4827590.0, 801670.0, 4847040.0] 
geom = box(*bounds)
geo = gpd.GeoDataFrame({'geometry': [geom]}, crs='EPSG:32619')

def process_band(item, band_name, meta):
    """Process the image band, reproject to 10m resolution if needed"""
    # Open the band image (SWIR or NIR)
    with rasterio.open(item.assets[band_name].href) as band_image:
        profile = band_image.profile
        # Get the CRS from the band image (if available)
        src_crs = band_image.crs
        # Create a window from the bounds - a windowed read will be performed just to keep data volumes to a minimum
        band_window = rasterio.windows.from_bounds(*bounds, band_image.transform)
        band_window_transform = rasterio.windows.transform(band_window, band_image.transform)
        
        # Read the data
        band_data = band_image.read(indexes=1, window=band_window).astype(np.float32)
        
        # Check if we need to resample (for SWIR bands at 20m)
        resolution = abs(band_image.transform.a)
        
        if resolution > 10.0:  # If resolution is coarser than 10m (e.g., 20m for SWIR)
            # Create an empty band for the output (upsampled to 10 m)
            band_data_10m = np.empty((int(band_window.height * 2), int(band_window.width * 2)), dtype=band_data.dtype)

            # Adjust the profile for the output image
            profile['transform'] = rasterio.Affine(
                a=10, b=band_window_transform.b, c=band_window_transform.c,
                d=band_window_transform.d, e=-10, f=band_window_transform.f
            )
            profile['width'] = band_window.width * 2
            profile['height'] = band_window.height * 2
            
            # Reproject to the new resolution
            band_data_10m, transform = reproject(
                source=band_data,
                destination=band_data_10m,
                src_transform=band_window_transform,
                dst_transform=profile['transform'],
                resampling=Resampling.nearest,
                src_crs=src_crs,
                dst_crs=band_image.crs
            )
            
            return band_data_10m, profile
        else:
            # For B08 which already has 10m resolution, return as is
            return band_data, profile

# Process both the pre-fire and post-fire SWIR and NIR bands
pre_swir, meta = process_band(items[0], 'B12', None)  # SWIR band (pre-fire)
pre_nir, _ = process_band(items[0], 'B08', meta)  # NIR band (pre-fire)

post_swir, meta = process_band(items[1], 'B12', meta)  # SWIR band (post-fire)
post_nir, _ = process_band(items[1], 'B08', meta)  # NIR band (post-fire)

# Compute NBR
def calculate_nbr(nir, swir):
    """Calculate the Normalized Burn Ratio (NBR)"""
    return (nir - swir) / (nir + swir)

# Calculate pre-fire and post-fire NBR
pre_nbr = calculate_nbr(pre_nir, pre_swir)
post_nbr = calculate_nbr(post_nir, post_swir)

# Compute Burn Severity (ΔNBR)
delta_nbr = pre_nbr - post_nbr

# Define the output path
output_path = r"C:\Users\ryanj\Desktop\COGS\code\portfolio\burn_severity_analysis\burn_severity.tif"

# Update metadata for output
meta.update({
    "dtype": rasterio.float32,
    "count": 1  # Ensure it is a single-band output
})

# Save the burn severity output
with rasterio.open(output_path, "w", **meta) as dest:
    dest.write(delta_nbr.astype(rasterio.float32), 1)

print("Burn severity map saved as 'burn_severity.tif'")