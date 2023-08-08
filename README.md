# nomad-diner

Deciding where to eat during travels can be a hassle. This script uses Google's APIs to suggest nearby restaurants.

## Features:

- **Location Input:** Accepts addresses or coordinates.
- **Filters:** Set price range, rating, and distance.
- **Search Term:** Filter by cuisine or dish.
- **ETA:** Estimates drive time.

## How It Works:

- **Input:** Takes addresses or coordinates and converts to lat/long.
- **Filtering:** Use `max_results` and `distance` for specific results.
- **Data Retrieval:** Fetches restaurant data from Google Places.
- **Drive Time Check:** Uses Haversine Distance formula. Utilizes `eta_threshold` to skip unnecessary drive time checks.

## Requirements

- Python 3.6+
- requests (>=2.0)

## Setup

1. Clone this repository:

```
git clone https://github.com/jludwig/nomad-diner.git
```

2. Navigate to the cloned directory and install the required packages:

```
pip install -r requirements.txt
```


3. Configure your Google Maps API Key:

Set your API key as an environment variable:

```
export GOOGLE_MAPS_API_KEY='YOUR_API_KEY'
```

🚨 Important: Ensure you've replaced YOUR_API_KEY with your actual Google Maps API key.

## Usage

Use the following syntax:

```
python nomad-diner.py [location] [options]
```

Example:

To find restaurants within 5km of Tokyo that have a minimum rating of 4.5 and are medium-priced:

```
python nomad-diner.py "Tokyo" --distance 5000 --min-rating 4.5 --max-price 2
```

### Additional Tips

- Use the -h option for a comprehensive list of available command-line options and further usage instructions:

```
python nomad-diner.py -h
```

- Rate Limits and Quotas: Always set up quotas for your API key in the Google Cloud Console to avoid unexpected charges.

## Versatility:

Though primarily for restaurants, the script can be adapted for other places with some tweaks.

## Limitations and Considerations

1. Limited QA, relying on manual tests.
2. Minimal error handling.
3. Dependent on Google's API - may break if there are changes.
4. Ensure API call quotas are set.
5. Requires API key with Geocoding, Places, and Directions API enabled.

## License

Licensed under the MIT License. Refer to the `LICENSE` file.
