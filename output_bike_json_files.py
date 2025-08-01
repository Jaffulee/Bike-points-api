from datetime import datetime
import json
import time
import requests as rq


def extract_bike_files():
    """
    Extracts data from the Transport for London BikePoint API and writes it to a local JSON file.

    Implements retry logic and stale data validation:
    - Retries up to `max_tries` times if the API response fails or is invalid.
    - Validates data freshness by checking the most recent 'modified' timestamp in the response.
    - If the data is stale (older than `staleness_days_criteria`), it skips writing the file.
    - Writes the data to a `data/` directory with a timestamped filename if the data is valid.
    """
    url = 'https://api.tfl.gov.uk/BikePoint'
    response = rq.get(url)

    num_tries = 0
    max_tries = 10
    sleep_time_seconds = 10
    staleness_days_criteria = 2

    while num_tries < max_tries:
        try:
            response.raise_for_status()
            data = response.json()
            length_data = len(data)

            if length_data < 50:
                raise Exception('Data too short')

            # Extract "modified" timestamps from the nested JSON
            dates = []
            for outerdict in data:
                for innerdict in outerdict['additionalProperties']:
                    try:
                        dateval = datetime.strptime(innerdict['modified'], '%Y-%m-%dT%H:%M:%S.%fZ')
                    except ValueError:
                        dateval = datetime.strptime(innerdict['modified'], '%Y-%m-%dT%H:%M:%SZ')

                    if dateval:
                        dates.append(dateval)

            max_date = max(dates)
            now_date = datetime.now()
            stale_days = (now_date - max_date).days

            if stale_days > staleness_days_criteria:
                raise Exception('Stale data, oh no')

            # Save JSON data locally with timestamp in filename
            filename = 'bike_api' + now_date.strftime('%Y-%m-%d_%H-%M-%S') + '.json'
            filepath = 'data/' + filename

            with open(filepath, 'w') as file:
                json.dump(data, file)

            break  # Exit loop on successful run

        except rq.exceptions.RequestException as e:
            print(f"Request error: {e}")
            print(f"HTTP status code: {response.status_code}")
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
        except Exception as e:
            print(f"General error: {e}")
        except:
            print('Unexpected error')

        # Retry logic
        num_tries += 1
        print(f'Waiting {sleep_time_seconds} seconds before retrying...')
        time.sleep(sleep_time_seconds)

    if num_tries == max_tries:
        print('Exceeded maximum number of retries. Exiting.')


if __name__ == '__main__':
    extract_bike_files()
