from datetime import datetime
# import datetime
import json
import time
import requests as rq


def extract_bike_files():

    url = 'https://api.tfl.gov.uk/BikePoint'
    response = rq.get(url)

    num_tries = 0
    max_tries = 10
    sleep_time_seconds = 10
    staleness_days_criteria = 2

    while num_tries<max_tries:
        try:
            response.raise_for_status()
            data = response.json()
            length_data = len(data)
            if length_data<50:
                raise Exception('Data too short')
            
            #Get date modified from json to check staleness
            dates = []

            for outerdict in data:
                for innerdict in outerdict['additionalProperties']:
                    try:
                        dateval = datetime.strptime(innerdict['modified'],'%Y-%m-%dT%H:%M:%S.%fZ')
                    except:
                        dateval = datetime.strptime(innerdict['modified'],'%Y-%m-%dT%H:%M:%SZ')
                    if dateval:
                        dates.append(dateval)
            max_date = max(dates)
            now_date = datetime.now()
            stale_days = (now_date-max_date).days
            # print(stale_days)
            if staleness_days_criteria>2:
                raise Exception('Stale data, oh no')

            filename = 'bike_api'+now_date.strftime('%Y-%m-%d_%H-%M-%S')+'.json'
            filepath = 'data/'+filename
            with open(filepath,'w') as file: #export
                json.dump(data,file)
            break
        #error logic
        except rq.exceptions.RequestException as e:
            print(e)
            status_code = response.status_code
            status_code_raw = response.raw
            print(status_code)
            print()
        except json.JSONDecodeError as e:
            print(e)
        except Exception as e:
            print(e)
        except:
            print('oop')

        #retry mechanism
        num_tries+=1
        print(f'waiting {sleep_time_seconds} seconds')
        time.sleep(sleep_time_seconds)

    if num_tries == max_tries:
        print('ran out of tries')

if __name__ == '__main__':
    extract_bike_files()

