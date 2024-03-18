import geopandas as gpd
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import random

np.set_printoptions(precision=2)

# make the results repeatable
np.random.seed(352)

def random_tours(n):
    """Create two random tours with n cities"""
    
    tour = list(range(n))
    np.random.shuffle(tour)

    # pick random index to split
    split = np.random.randint(0, n-1)
    tour1 = tour[:split]
    tour2 = tour[split:]
    

    return(tour)

def get_state_centroids():
    # Read state data

    # load pickled data from states.pkl if it exists
    try:
        states = pd.read_pickle('states.pkl')
        print('Loaded from states.pkl')
    except:        
        states = gpd.read_file('https://www2.census.gov/geo/tiger/GENZ2021/shp/cb_2021_us_state_20m.zip')

        # pickle (save) the data to states.pkl
        states.to_pickle('states.pkl')

    # Filter out Alaska, Hawaii, and territories
    contiguous_usa = states[~states['STUSPS'].isin(['AK', 'HI', 'PR', 'GU', 'VI', 'MP', 'AS', 'DC'])]

    # Calculate centroids
    # /home/stan/repositories/CS7320-AI/ComplexSearch/map.py:46: UserWarning: Geometry is in a geographic CRS. Results from 'centroid' are likely incorrect. Use 'GeoSeries.to_crs()' to re-project geometries to a projected CRS before this operation.
   # centroids = contiguous_usa.geometry.centroid
    # fix:
    contiguous_usa = contiguous_usa.to_crs(epsg=2163)


    centroids = contiguous_usa.geometry.centroid
    contiguous_usa['centroid_lon'] = centroids.x
    contiguous_usa['centroid_lat'] = centroids.y

    # Create tuples (state name, x-coordinate, y-coordinate)
    state_tuples = list(zip(contiguous_usa['NAME'], centroids.x, centroids.y))

    return contiguous_usa, state_tuples

def draw_contiguous_usa_map_with_centroids():
    contiguous_usa, state_tuples = get_state_centroids()

    print(state_tuples)
    print(len(state_tuples))

    # Plotting
    fig, ax = plt.subplots(1, 1, figsize=(15, 10))
    contiguous_usa.plot(ax=ax, color='white', edgecolor='black')

    # Plot centroids
    for state, x, y in state_tuples:
        plt.plot(x, y, marker='o', color='gray', markersize=5)

    plt.title("USA with State Centroids")
    plt.show()

draw_contiguous_usa_map_with_centroids()

