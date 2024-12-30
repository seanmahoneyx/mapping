import folium
import pandas as pd

# Load data and store in lists
data = pd.read_csv("Volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])

def color_producer(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000<= elevation < 3000:
        return 'orange'
    else:
        return 'red'


#HTML styling variable for popups that provides a Google link for selected volcano
html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

map = folium.Map(location=[38.58, -99.09], zoom_start=5, tiles="Cartodb Positron")
fgv = folium.FeatureGroup(name="Volcanoes")

for lt, ln, el in zip(lat, lon, elev):
    fgv.add_child(folium.CircleMarker(location=[lt, ln], radius = 6, popup=str(el)+" m", fill_color=color_producer(el),
                                     color ='grey', fill_opacity = 0.7))

fgp = folium.FeatureGroup(name="Population")
geojson_data = open('world.json', 'r', encoding='utf-8-sig').read()
fgp.add_child(folium.GeoJson(data=geojson_data, style_function=lambda x: {'fillColor':'green'
                            if x['properties']['POP2005'] < 10000000 else
                            'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())

map.save("Map1.html")