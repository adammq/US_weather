# for url:
import urllib
# for html:
import requests
import bs4
# for proper location name, latitude, longitude:
from geopy.geocoders import Nominatim

# getting temperature from National Weather Service
weather_url = "https://forecast.weather.gov/"
geolocator = Nominatim(user_agent="weather app")

# checking the integrity of the location passed in
invalid_location = True
while (invalid_location):
	location = input("CITY, ST: ")

# use CITY, ST to fetch data
# Location is a list storing location string, latitude, and longitude
	Location = geolocator.geocode(location)
	if (str(Location) == "None"):
		print("\n***LOCATION NOT FOUND***\n")
	else:
		invalid_location = False


# fit latitude and longitude to format required in NWS url form
# local weather pages on NWS website all employ this same url form, only
# varying the latitude and longitude to two decimal places in the url
lat = round(Location.latitude, 2)
lon = round(Location.longitude, 2)
city_link = "MapClick.php?textField1=" + str(lat) + "&textField2=" + str(lon) + "#.XFXwSs9Kh24"

# creates total url
url = urllib.parse.urljoin(weather_url, city_link)

# fetching the html
response = requests.get(url)
html = response.text
soup = bs4.BeautifulSoup(html, "html.parser")

# searching for relevant information
tempf = soup.find(id="current_conditions-summary").find(class_="myforecast-current-lrg")
tempc = soup.find(id="current_conditions-summary").find(class_="myforecast-current-sm")
weather = soup.find(id="current_conditions_detail").find_all('tr')

# printing location as well as relevant temperature and weather metrics
print("\n" + str(Location) + ":")

# desired number of underscores to span location text
width = len(Location[0])+1
print("-"*width)
print("\nTemperature\n" + tempf.text + " (" + tempc.text + ")\n\n")

# it is necessary to create and cycle through a multidimensional array
# in order to extract desired data
w = []
for i in range(0, len(weather)):
	w.append(weather[i].find_all('td'))
for i in range(0, len(w)):
	for j in range(0, len(w[i])):
		print(w[i][j].text)
	print("\n")