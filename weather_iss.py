#!/usr/bin/env python3.7
import json
import requests
from datetime import datetime

WEATHER_API_CALL = "https://api.darksky.net/forecast/fc995cf7fbe0051ca6cd68805dfc5783/"
GEO_API_CALL = "http://open.mapquestapi.com/geocoding/v1/address?key=UhL8161KEFt4CGekeRCeYoBDQSd0t6GF&location="
REVERSE_GEO_API_CALL = "http://www.mapquestapi.com/geocoding/v1/reverse?key=UhL8161KEFt4CGekeRCeYoBDQSd0t6GF&location="
ISS_API_CALL = "http://api.open-notify.org/iss-pass.json?"  # + "lat=LAT&lon=LON"


def get_weather(location):

    # Get latitude and longitude
    coord = get_lat_lng(location)

    # Get all weather data and convert to JSON
    local_weather_api_call = WEATHER_API_CALL + \
        str(coord["lat"]) + "," + str(coord["lng"])
    weather_data = (requests.get(local_weather_api_call)).json()

    # Get tempurature, humidity, & condition from JSON
    tempurature = weather_data["currently"]["temperature"]
    feels_tempurature = weather_data["currently"]["apparentTemperature"]
    humidity = weather_data["currently"]["humidity"]*100
    conditions = weather_data["currently"]["summary"]

    # Print weather data
    result = "\n----------------------------------------"
    if(len(coord['city']) == 0):
        result += ("\nCurrent weather in\t" + coord["state"])
    else:
        result += ("\nCurrent weather in\t" + coord["city"] + ", " +
                   coord["state"])

    result += ("\nCurrent temperature\t" + str(tempurature) + "F")
    result += ("\nCurrent feels like\t" + str(feels_tempurature) + "F")
    result += ("\nCurrent humidity\t%.1f%%" % humidity)
    result += ("\nCurrent conditions\t" + str(conditions))
    result += ("\n----------------------------------------\n")
    return result


def get_ISS():
    location = input(
        "\nEnter an address, city & state, or ZIP Code for International Space Station data\n>>> ")

    # Get latitude and longitude
    coord = get_lat_lng(location)

    local_iss_api_call = ISS_API_CALL + "lat=" + \
        str(coord["lat"]) + "&lon=" + str(coord["lng"])

    iss_data = (requests.get(local_iss_api_call)).json()

    print(iss_data)

    if(len(coord['city']) == 0):
        print("\nISS over\t" + coord["state"])
    else:
        print("\nISS over\t" + coord["city"] + ", " +
              coord["state"])

    print("----------------------------------------")
    for response in iss_data['response']:
        risetime = response['risetime']
        duration = response['duration']

        print("Risetime\t" + str(datetime.utcfromtimestamp(risetime).strftime('%c')))
        print("Settime\t\t" +
              str(datetime.utcfromtimestamp(risetime+duration).strftime('%c')))
        print("----------------------------------------")
    print("\n")

    return


def get_lat_lng(location):

    # Convert location data into latitude & longitude
    location_api_call = GEO_API_CALL + location
    geo_data = (requests.get(location_api_call)).json()

    locations = geo_data['results'][0]['locations']

    for local in locations:
        if (local['adminArea1'] == "US"):
            geo_data = local
            break

    city = geo_data['adminArea5']
    if (len(city) == 0):
        city = geo_data['adminArea4']

    state = geo_data['adminArea3']
    lat = geo_data['latLng']['lat']
    lng = geo_data['latLng']['lng']

    # Return a dictionary of the lat, lng, city, state
    return {"lat": lat, "lng": lng, "state": state, "city": city}
