#!/usr/bin/env python3

import argparse
import json
import math
import os
import re
import requests

API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')
if not API_KEY:
    raise ValueError("Please set the environment variable GOOGLE_MAPS_API_KEY with your Google Maps API key.")

def get_location_coordinates(location):
    """
    Fetches latitude and longitude for a given location using Google's Geocode API.

    :param location: Location name or address
    :return: tuple containing latitude and longitude
    """
    endpoint = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        'address': location,
        'key': API_KEY
    }

    response = requests.get(endpoint, params=params).json()

    if response['status'] != 'OK':
        raise ValueError(f"Could not fetch coordinates for the location provided. Response: {json.dumps(response, indent=4)}")

    latlng = response['results'][0]['geometry']['location']
    return latlng['lat'], latlng['lng']


def is_coordinate(input_str):
    """
    Checks if the input string is a valid coordinate format.

    :param input_str: A string to validate
    :return: True if the string is a coordinate format, False otherwise
    """
    pattern = r'^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$'
    return bool(re.match(pattern, input_str))


def haversine_distance(coord1, coord2):
    """
    Calculate the Haversine distance between two points on the earth.

    :param coord1: tuple of float (latitude, longitude)
    :param coord2: tuple of float (latitude, longitude)
    :return: distance in meters
    """
    # Aprox radius of Earth in meters
    R = 6371008.8

    lat1 = math.radians(coord1[0])
    lon1 = math.radians(coord1[1])
    lat2 = math.radians(coord2[0])
    lon2 = math.radians(coord2[1])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def get_nearby_restaurants(location, distance, min_rating=None, max_price=None, search=None, max_results=25, get_eta=False, eta_threshold=0):
    """
    Fetches nearby restaurants based on the provided criteria.

    :param location: Location name, address, or coordinates
    :param distance: Search radius in meters
    :param min_rating: Filter by minimum rating (optional)
    :param max_price: Filter by maximum price level (optional)
    :param search: Keyword to search for in restaurant names or descriptions (optional)
    :param max_results: Maximum number of results to return (default is 25)
    :param get_eta: Boolean indicating whether to get ETA by car (default is False)
    :param eta_threshold: Threshold in meters beyond which to get the ETA (default is 0)
    :return: List of dictionaries containing restaurant details
    """
    if is_coordinate(location):
        lat, lng = map(float, location.split(","))
    else:
        lat, lng = get_location_coordinates(location)

    endpoint = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        'location': f"{lat},{lng}",
        'radius': distance,
        'type': 'restaurant',
        'key': API_KEY
    }
    if search:
        params['keyword'] = search

    res = requests.get(endpoint, params=params).json()
    if res['status'] != 'OK':
        return []

    restaurant_details = []
    for result in res['results']:
        if len(restaurant_details) == max_results:
            break

        details_endpoint = "https://maps.googleapis.com/maps/api/place/details/json"
        details_params = {
            'place_id': result['place_id'],
            'fields': 'name,rating,user_ratings_total,price_level,types,opening_hours,formatted_address,formatted_phone_number,website,editorial_summary',
            'key': API_KEY
        }
        details_res = requests.get(details_endpoint, params=details_params).json()
        details = details_res['result']

        if min_rating and float(details.get('rating', 0)) < min_rating:
            continue
        if max_price and details.get('price_level', 5) > max_price:
            continue

        destination_lat, destination_lng = result['geometry']['location']['lat'], result['geometry']['location']['lng']
        straight_distance = haversine_distance((lat, lng), (destination_lat, destination_lng))
        rounded_distance = round(straight_distance / 10) * 10

        driving_eta = None
        if get_eta and (not eta_threshold or straight_distance > eta_threshold):
            driving_eta = get_driving_eta((lat, lng), (destination_lat, destination_lng))

        restaurant = {
            'Name': details['name'],
            'Rating': details.get('rating', "N/A"),
            'Number of Ratings': details.get('user_ratings_total', "N/A"),
            'Price Level': '$' * details.get('price_level', 0),
            'Address': details.get('formatted_address', "N/A"),
            'Phone Number': details.get('formatted_phone_number', "N/A"),
            'Website': details.get('website', "N/A"),
            'Summary': details.get('editorial_summary', "N/A"),
            'Driving ETA': driving_eta,
            'Haversine Distance': rounded_distance
        }
        restaurant_details.append(restaurant)

    return restaurant_details


def get_driving_eta(origin, destination):
    """
    Fetches driving ETA between two locations using Google's Directions API.

    :param origin: Tuple of source latitude and longitude
    :param destination: Tuple of destination latitude and longitude
    :return: Estimated driving time as a string or None if not available
    """
    origin_str = "{},{}".format(*origin)
    destination_str = "{},{}".format(*destination)

    directions_endpoint = "https://maps.googleapis.com/maps/api/directions/json"
    directions_params = {
        'origin': origin_str,
        'destination': destination_str,
        'mode': 'driving',
        'key': API_KEY
    }
    eta_res = requests.get(directions_endpoint, params=directions_params).json()

    if eta_res['status'] != 'OK' or not eta_res.get('routes'):
        return None

    return eta_res['routes'][0]['legs'][0]['duration']['text']


def main():
    """
    Command-line interface for fetching nearby restaurant details based on provided criteria.
    """
    parser = argparse.ArgumentParser(description='Get nearby restaurants based on location.')
    parser.add_argument('location', type=str, help='A location name, address, or coordinates.')
    parser.add_argument('--distance', type=int, default=20000, help='Search radius in meters.')
    parser.add_argument('--get-eta', action='store_true', help='Get ETA by car to the location.')
    parser.add_argument('--eta-threshold', type=int, help='Only get ETA for locations over this distance in meters.')
    parser.add_argument('--min-rating', type=float, help='Filter results by a minimum rating.')
    parser.add_argument('--max-price', type=int, help='Filter results by a maximum price level. 1 is cheapest and 4 is most expensive.')
    parser.add_argument('--search', type=str, help='Search keyword to filter results by restaurant names or descriptions.')
    parser.add_argument('--max-results', type=int, default=25, help='Maximum number of results to return.')

    args = parser.parse_args()

    restaurants = get_nearby_restaurants(
        location=args.location,
        distance=args.distance,
        min_rating=args.min_rating,
        max_price=args.max_price,
        search=args.search,
        max_results=args.max_results,
        get_eta=args.get_eta,
        eta_threshold=args.eta_threshold
        )

    print(json.dumps(restaurants, indent=4))


if __name__ == '__main__':
    main()
