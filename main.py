import sys
import geoplot as gplt
import geopandas as gpd
import geoplot.crs as gcrs
import imageio
from shapely.geometry import Point
import pandas as pd
import pathlib
import matplotlib.pyplot as plt
import mapclassify as mc
import numpy as np

BOROUGH_BOUNDARIES = "data/BoroughBoundaries/BoroughBoundaries.shp"

if __name__ == "__main__":
    fileName = sys.argv[1]

    # GDF of NYC Borough Boundaries
    nyc_gdf = gpd.read_file(BOROUGH_BOUNDARIES)

    # GDF of NYC Schools
    schools = pd.read_csv("data/PublicSchoolLocations2019-2020.csv")
    schools = schools[schools["Status_descriptions"] == "Open"]
    school_points = gpd.GeoDataFrame(schools, geometry=gpd.GeoSeries.from_xy(schools['LONGITUDE'], schools['LATITUDE']), crs=4326)
    school_points = school_points[~school_points.geometry.is_empty]
    
    # GDF of 1320 ft around NYC Schools
    school_radii = school_points.copy().to_crs(crs=3857) # Project to a coordinate system that uses meters
    school_radii['geometry'] = school_radii['geometry'].buffer(402.336)
    school_radii = school_radii.to_crs(crs=4326)
    
    # Restrict to land boundaries of the boroughs.
    coveredAreas = nyc_gdf.to_crs(crs=4326).overlay(school_radii.dissolve())
    
    # Create an interactive map with folium.
    m = coveredAreas.explore(
            highlight = False,
            max_bounds = True,
            style_kwds = {"stroke": False, "fillColor": "pink"},
            tiles="CartoDB positron",
            tooltip=False)
    
    m.save(fileName)
