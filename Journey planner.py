from geopy.geocoders import Nominatim #geolocate query
from geopy.distance import geodesic #measure distance
from gmplot import gmplot
import requests, json
from itertools import permutations


def mark_location(destination):
    # to store the list of latitude and longitude for each city
    for i in range (0,len(destination)):
        dest = geolocator.geocode(destination[i])  # .geocode
        cityList.append((dest.latitude, dest.longitude))
        cityDict[destination[i]] = cityList[i]

def plot_location(kl):
    #mark locations (GMPlot)
    gmap = gmplot.GoogleMapPlotter(kl.latitude, kl.longitude,3)
    gmap.apikey = ""
    city_lats, city_lons = zip(*cityList) #* to unpack cityList
    #scatter plots
    gmap.scatter(city_lats, city_lons, '#3B0B39', size=40, marker=False)
    gmap.draw("map_for_ben.html")

# Measuring distances
#Method 1: Python Geocoding Toolbox

def measure_distance(start,destination):
    for i in destination:
        dest = geolocator.geocode(i) #.geocode
        print(dest.address)
        print(dest.latitude, dest.longitude)

        # Measuring distance
        current_location = (start.latitude, start.longitude)
        destination_location = (dest.latitude, dest.longitude)
        print(geodesic(current_location, destination_location).kilometers)


#Method 2: Google Distance Matrix API
def land_transport(source,dest_name):
#    source = destination[0]
#    dest_name="Bangkok, Thailand"
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&'
    r = requests.get(url + 'origins= ' + source +
                         '&destinations= ' + dest_name +
                        '&avoid=tolls&departure_time=now&mode=driving&key=APIkey')
    # mode - drving(default), walking, cycling ...
    # units - metrics (default)
    # avoid - tolls, highway (biases the result to more favorable routes)
    x = r.json()
    y = x.get('rows')
    z = y[0].get('elements')
    ans = z[0].get('duration')
    print("---------------------------------------------------")
    print("Duration if drive to Thailand: ")
    print("Extra option : avoid tolls")
    print(ans.get('text')+'\n')


#Plan shortest route
#permutation
#sum all shortest route
def permutation(lists):
    dest_list = list(permutations(lists))
    return dest_list

#city dict
def shortest_route(dest_list):
    index = 0
    min = 9999999999
    total_dist = [0] * len(dest_list)
    for k in range(0,len(dest_list)) :
        dest_list[k] = list(dest_list[k])   #convert frm tuple to list
        dest_list[k].insert(0,destination[0])
        for i in range (0, len(dest_list[k])-1):
            total_dist[k] += geodesic(cityDict.get(dest_list[k][i]), cityDict.get(dest_list[k][i+1])).kilometers
        if(total_dist[k]<min):
            min = total_dist[k]
            index = k
    print("Total distance is :")
    print(total_dist[index])
    return index


#driver code
if __name__ == "__main__":
    # 1. Mark Locations
    # Create a list - consisting of tuples
    cityList = []
    cityDict = {}
    destination = ['KLIA, Kuala Lumpur,Malaysia', 'Jakarta,Indonesia', 'Bangkok,Thailand', 'Taipei,Taiwan', 'Hong Kong',
                   'Tokyo,Japan', 'Beijing,China', 'Seoul,Korea']
    geolocator = Nominatim(user_agent="my app")
    mark_location(destination)
    kl = geolocator.geocode(destination[0])
    plot_location(kl)

    # 2. Measuring distances
    #Method 1: Python Geocoding Toolbox
    print("\nDestination from KLIA to:")
    measure_distance(kl, destination[1:])

    #Method 2: Google distance matrix API
    print("Alternative to travel by land:")
    #land_transport('KLIA, Kuala Lumpur,Malaysia','Bangkok,Thailand')

    # 3. Find shortest path
    dest_list = permutation(destination[1:])
    index = shortest_route(dest_list)
    print("The shortest route is: ")
    print(dest_list[index])





