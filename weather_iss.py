#!/usr/bin/env python3.7
import json
import requests
import pytz
from datetime import datetime

# Declare constants for API calls
WEATHER_API_CALL = "https://api.darksky.net/forecast/fc995cf7fbe0051ca6cd68805dfc5783/"
GEO_API_CALL = "http://open.mapquestapi.com/geocoding/v1/address?key=UhL8161KEFt4CGekeRCeYoBDQSd0t6GF&location="
REVERSE_GEO_API_CALL = "http://www.mapquestapi.com/geocoding/v1/reverse?key=UhL8161KEFt4CGekeRCeYoBDQSd0t6GF&location="
ISS_API_CALL = "https://api.wheretheiss.at/v1/satellites/25544"
COUNTRY_CODE_API_CALL = "https://restcountries.eu/rest/v2/alpha/"


def get_weather(protocol, location):

    # Get latitude and longitude
    coord = get_lat_lng(location)

    # Get all weather data and convert to JSON
    local_weather_api_call = WEATHER_API_CALL + \
        str(coord["lat"]) + "," + str(coord["lng"])
    weather_data = (requests.get(local_weather_api_call)).json()

    # Begin recording the output string into "result"
    result = "\n========================================"

    # If the client wants 3 day forecast, gather data for next 3 days
    if(protocol == "3DAY"):

        # If there is no city name available, output county data instead
        if(len(coord['city']) == 0):
            result += ("\nForcast weather in\t" +
                       coord["country"] + " " + coord["state"])
        else:
            result += ("\nForcast weather in\t" + coord["city"] + ", " +
                       coord["state"])

        # Get JSON data for the daily weather forcast
        daily_forcast_data = weather_data["daily"]["data"]
        daily_forcast = []

        # For all the days in the JSON data, work on a single days worth of data
        for day in daily_forcast_data:
            day_weather = {
                "date": datetime.utcfromtimestamp(int(day["time"])).strftime('%Y-%m-%d'),
                "summary": day["summary"],
                "sunrise": datetime.utcfromtimestamp(int(day["sunriseTime"])-14400).strftime('%H:%M:%S'),
                "sunset": datetime.utcfromtimestamp(int(day["sunsetTime"])-14400).strftime('%H:%M:%S'),
                "precip_prob": str(day["precipProbability"]*100) + " %",
                "high_temp": str(day["temperatureHigh"]) + "F",
                "low_temp": str(day["temperatureLow"]) + "F",
            }
            # Add each day's weather data to an array
            daily_forcast.append(day_weather)

        # Format output string for 3 days worth of weather forecast
        i = 0
        for x in daily_forcast:
            result += "\n----------------------------------------"

            result += "\nDate: " + x["date"]
            result += "\n" + x["summary"] + "\n"
            result += "\nSunrise time\t\t" + x["sunrise"]
            result += "\nSunset time\t\t" + x["sunset"]
            result += "\nPrecip chance\t\t" + \
                x["precip_prob"]
            result += "\nHigh Temp\t\t" + x["high_temp"]
            result += "\nLow Temp\t\t" + x["low_temp"]
            i += 1
            if i == 3:
                break

    # If the client inputs any command other than "3DAY", output the current weather information
    else:

        # If there is no city name available, output county data instead
        if(len(coord['city']) == 0):
            result += ("\nCurrent weather in\t" +
                       coord["country"] + " " + coord["state"])
        else:
            result += ("\nCurrent weather in\t" + coord["city"] + ", " +
                       coord["state"])

        # Get tempurature, humidity, & condition from JSON
        tempurature = weather_data["currently"]["temperature"]
        feels_tempurature = weather_data["currently"]["apparentTemperature"]
        humidity = weather_data["currently"]["humidity"]*100
        conditions = weather_data["currently"]["summary"]

        # Format output string for the current weather
        result += ("\nCurrent temperature\t" + str(tempurature) + "F")
        result += ("\nCurrent feels like\t" + str(feels_tempurature) + "F")
        result += ("\nCurrent humidity\t%.1f%%" % humidity)
        result += ("\nCurrent conditions\t" + str(conditions))

    result += ("\n========================================\n")
    return result


def get_ISS():

    # Retrieves the current location of the ISS (latitutde, longitude coordinates)
    iss_data = (requests.get(ISS_API_CALL)).json()

    # Gathers the location data (city, country)
    iss_lat = float('{:.3f}'.format(iss_data['latitude']))
    iss_lng = float('{:.3f}'.format(iss_data['longitude']))

    local = get_location(iss_lat, iss_lng)

    msg = ("==================================================\n")

    # If the country returns as "XZ" then the ISS is not over a specific country
    if(local['country'] == "XZ"):
        msg = "The ISS is located at " + "lat: " + str(iss_lat) + " lng: " + str(
            iss_lng) + "\t over the ocean"
    else:
        # Get the country name from the two letter country code
        country_code = local['country']
        country_data = (requests.get(
            COUNTRY_CODE_API_CALL+country_code)).json()
        country = country_data["name"]
        msg += "The ISS is located at " + "lat: " + str(iss_lat) + " lng: " + str(
            iss_lng) + "\nOver Country:\t" + str(country)

    msg += ("\n==================================================\n")

    result = {
        'msg': msg,
        'lat': iss_lat,
        'lng': iss_lng
    }

    return result


def get_lat_lng(location):

    # Convert location data into latitude & longitude
    location_api_call = GEO_API_CALL + location
    geo_data = (requests.get(location_api_call)).json()

    locations = geo_data['results'][0]['locations']

    # Find the location that is in the USA
    for local in locations:
        if (local['adminArea1'] == "US"):
            geo_data = local
            break

    city = geo_data['adminArea5']

    # If city is not given, get county
    if (len(city) == 0):
        city = geo_data['adminArea4']

    state = geo_data['adminArea3']
    lat = geo_data['latLng']['lat']
    lng = geo_data['latLng']['lng']
    country = geo_data['adminArea1']

    # Return a dictionary of the lat, lng, city, state
    return {"lat": lat, "lng": lng, "state": state, "city": city, "country": country}


def get_location(lat, lng):

    # Reverse geocode lat and lng into a location
    location_api_call = REVERSE_GEO_API_CALL + str(lat) + ","+str(lng)
    geo_data = (requests.get(location_api_call)).json()

    country = city = geo_data['results'][0]['locations'][0]['adminArea1']

    city = geo_data['results'][0]['locations'][0]['adminArea5']

    # If city is not given, get county
    if (len(city) == 0):
        city = geo_data['results'][0]['locations'][0]['adminArea4']

    # Return city and country code
    return {'city': city, 'country': country}
