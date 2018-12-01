import folium
from folium.plugins import MarkerCluster
import geopandas as gpd
import pandas as pd
import psycopg2

# create map object
map = folium.Map([20.5937, 78.9629],
                 zoom_start=4,
                 tiles='cartodbpositron')

connection = psycopg2.connect(database="india", user="postgres", password="toorroot")

states = gpd.read_postgis('select * from gadm36_ind_1', connection)
consumers = pd.read_csv('consumers.csv')
retailers = pd.read_csv('retailers.csv')


def popup_generator(data, i):
    iocl = "IOCL / AOD : " + str(data['IOCL/AOD'][i])
    hpcl = "HPCL : " + str(data['HPCL'][i])
    bpcl = "BPCL : " + str(data['BPCL'][i])
    total = "TOTAL : " + str(data[' TOTAL'][i])
    total_as_on = "TOTAL (As on 1.4.2011) : " + str(data[' TOTAL (As on 1.4.2011)'][i])
    return iocl + '  |  ' + hpcl + '  |  ' + bpcl + '  |  ' + total + '  |  ' + total_as_on


# folium.Marker(
#     location=(),
#     popup='Add popup text here.',
#     icon=folium.Icon(color='green', icon='ok-sign'),
# ).add_to(map)


consumers = consumers.sort_values('State / UT', axis=0)
consumers = consumers.reset_index(drop=True)
retailers = retailers.sort_values('State / UT', axis=0)
retailers = retailers.reset_index(drop=True)
c_i = 0
states_i = 0
while c_i < consumers.shape[0]:
    if states['name_1'][states_i] != 'Telangana':
        print(states['name_1'][states_i], states['geom'][states_i].centroid.y,
              states['geom'][states_i].centroid.x)
        folium.Marker(
            location=(states['geom'][states_i].centroid.y, states['geom'][states_i].centroid.x),
            popup='Consumers :- ' +
            popup_generator(consumers, c_i) + ' '*20 + 'Retailers :-' +
            popup_generator(retailers, c_i),
            tooltip=states['name_1'][states_i],
            icon=folium.Icon(color='green', icon='info-sign')).add_to(map)
        c_i += 1
        states_i += 1
    else:
        states_i += 1


states_json = states.to_crs(epsg='4326').to_json()
folium.GeoJson(states_json).add_to(map, name='state')
folium.LayerControl().add_to(map)

# save file
map.save('test.html')
