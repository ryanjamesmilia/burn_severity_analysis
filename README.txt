###################################################################################################################

This repository includes 3 python scripts. The first script prints a burn severity map based on 
Sentinel-2 imagery. The second script masks water from the analysis. The third script calculates
the area (Ha) of burn severity levels.

###################################################################################################################

This project was created by Ryan Milia as part of the Geospatial Data Analytics Program at the 
Centre of Geographic Sciences, Nova Scotia Community College, Lawrencetown, Nova Scotia. It is 
intended for educational purposes only. All content is unedited and unverified. © 2024 COGS

###################################################################################################################

Landsat 2 imagery was downloaded using the STAC catalog using python (pystac). Nova Scotia 
county and water data was downloaded from the Nova Scotia Geographic Data Directory. Normalized 
Burn Ratio (NBR) calculations were taken from the United Nations website.

###################################################################################################################

Instructions:
	1. Download data from this link: "https://github.com/ryanjamesmilia/burn_severity_analysis/releases/tag/v1"
	2. Update file paths as required.
	3. Run all scripts in numerical order.

###################################################################################################################

Data:
	1. 1-burn_severity.py: python script printing a burn severity map.
	2. 2-masking_water.py: python script masking water areas from the burn severity map.
	3. 3-area_calculation.py: python script calculating areas within each burn severity level.
	4. burn_severity_analysis.docx: report presenting burn severity map and graphs.
------------------------------------------------------------------------------------------------------------------
