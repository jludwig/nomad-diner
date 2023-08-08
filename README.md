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

## Installation

1. Clone this repository:

```
git clone https://github.com/jludwig/nomad-diner.git
```

2. Navigate to the cloned directory and install the required packages:

```
pip install -r requirements.txt
```

**Note:** Remember to replace `YOUR_GOOGLE_MAPS_API_KEY` in the script with your actual API key. And, don't forget to set up quotas on your API calls to avoid potential surprises.

## Usage

```
python nomad-diner.py "Tokyo" --distance 5000 --min-rating 4.5 --max-price 2
```

Finds restaurants within 5km of Tokyo with at least a 4.5 rating and medium price.

Refer to the script's help (`-h` option) for detailed usage instructions.

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
