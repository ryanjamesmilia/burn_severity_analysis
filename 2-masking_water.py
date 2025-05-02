"""Masking Water"""

__author__ = "Ryan Milia"

""" Date: March 06, 2025
    Description:
    This module masks water from the Landsat-2 derived burn severity map.
    - Opens the GeoNOVA dataset.
    - Applies a mask to the existing burn severity map.
    - Prints a masked burn severity map.
"""

import rasterio
from rasterio.io import MemoryFile
import rasterio.mask
import shapely.ops
import pyproj
import fiona

# Filters features from the dataset
def filter_features(property: str, value: str, dataset):
    return list(filter(lambda f: f.properties[property] == value, dataset))

# Applies a coordination operation to features
def transform_features(features, from_crs, to_crs):
    transform = pyproj.Transformer.from_crs(from_crs,
                                            to_crs,
                                            always_xy=True).transform
    output_features = []
    for f in features:
        output_features.append(shapely.ops.transform(transform,
                                                     shapely.geometry.shape(f.geometry)))
    return output_features

# Applies a mask to the bands
def apply_mask(band, features, invert=False):
    with MemoryFile() as memfile:
        with rasterio.open(memfile,
                           mode='w',
                           **profile) as temp:
            temp.write(band)
        with rasterio.open(memfile) as temp:
            result, _ = rasterio.mask.mask(temp,
                                           features,
                                           invert=invert,
                                           filled=True)
    return result

if __name__ == '__main__':

    # File paths
    lake_filename = r'C:\Users\ryanj\Desktop\COGS\code\portfolio\burn_severity_analysis\water\WA_POLY_10K.shp'  
    county_filename = r'C:\Users\ryanj\Desktop\COGS\code\portfolio\burn_severity_analysis\county\County_Polygons.shp'
    input_filename = r'C:\Users\ryanj\Desktop\COGS\code\portfolio\burn_severity_analysis\burn_severity.tif'  
    output_filename = r'C:\Users\ryanj\Desktop\COGS\code\portfolio\burn_severity_analysis\masked_burn_severity.tif'

    with rasterio.open(input_filename) as burn_severity:
        # Get the CRS of the image
        burn_severity_crs = burn_severity.crs
        # Get the profile of the burn severity dataset
        profile = burn_severity.profile
        # Open the GeoNOVA county dataset. This dataset will be used to mask out the ocean.
        with fiona.open(county_filename) as county:
            # Filter out Nova Scotia
            shelburne = filter_features('NAME',
                                        'Shelburne',
                                        county)
            mask_county = transform_features(shelburne,
                                             county.crs,
                                             burn_severity_crs)
        # Open the GeoNOVA dataset used to mask the lakes.
        with fiona.open(lake_filename) as lake:
            # Get the geometry for masking
            lakes = filter_features('FEAT_DESC',
                                    'Lake Water polygon',
                                    lake)
            lakes.extend(filter_features('FEAT_DESC',
                                         'Coast River Water polygon',
                                         lake))
            mask_lakes = transform_features(lakes, lake.crs, burn_severity_crs)
        # Mask the burn severity band with the province boundary
        masked = apply_mask(burn_severity.read(), mask_county)
        # Mask the result with the lakes
        masked = apply_mask(masked, mask_lakes, invert=True)

    # Write the mask result to a new file (not overwriting the original)
    with rasterio.open(output_filename,
                       mode='w',
                       **profile) as output:
        output.write(masked)

    print(f"Masked burn severity map saved to {output_filename}")