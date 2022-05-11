import pandas as pd
import geopandas as gpd
import random
from shapely.geometry import Point

def get_random_point_in_polygon(poly):
    minx, miny, maxx, maxy = poly.bounds.iloc[0]
    while True:
        p = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
        if poly.contains(p).iloc[0]:
            return p

filename_microdata = 'data/guernsey_microdata.csv'
microdata = pd.read_csv(filename_microdata)
microdata['Block'] = microdata['Block'].astype(str)
microdata['lat'] = None
microdata['lon'] = None

filename_gdf = 'data/tl_2020_39059_tabblock10.shp'
gdf = gpd.read_file(filename_gdf)

for index, row in microdata.iterrows():
    blockid = row["Block"]
    poly = gdf[gdf["GEOID10"] == blockid].geometry
    minx, miny, maxx, maxy = poly.bounds.iloc[0]
    point_in_poly = get_random_point_in_polygon(poly)
    microdata.at[index, "lon"] = point_in_poly.x
    microdata.at[index, "lat"] = point_in_poly.y
microdata.to_csv("data/guernsey_data.csv", index=False)