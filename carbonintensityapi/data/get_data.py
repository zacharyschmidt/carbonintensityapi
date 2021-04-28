import requests
from datetime import date, timedelta
import time
import json
import csv
from carbonintensityapi.utils.utils import flatten_json
import sys


# dateBegin = date.fromisoformat('2017-09-26')
dateBegin = date.fromisoformat('2019-06-29')
dateEnd = date.fromisoformat('2021-02-24')
num_of_days = dateEnd-dateBegin
print(num_of_days.days)
# figure out how to make this an absolute path. Do I need
# a script to execute module code?
data_file = open('data/raw/full_history3.csv', 'w')
csv_writer = csv.writer(data_file)

count = 0
for i in range(num_of_days.days + 1):
    for j in range(1, 10):

        print(dateBegin.isoformat())
        headers = {
            'Accept': 'application/json'
        }
        # date = '2020-08-25'
        period = j
        time.sleep(.3)
        r = requests.get(
            f'https://api.carbonintensity.org.uk/intensity/date/{dateBegin}/{period}',
            params={},
            headers=headers)
        try:
            r.raise_for_status()
        except requests.exceptions.Timeout:
            continue
        except requests.exceptions.TooManyRedirects:
            continue
        except requests.exceptions.HTTPError as e:
            print("Error: " + str(e))
            continue
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        data = flatten_json(r.json()['data'][0])
        print(data)
        if count == 0:
            header = data.keys()
            csv_writer.writerow(header)
            count += 1
        # print(data.values())
        csv_writer.writerow(data.values())

    dateBegin += timedelta(days=1)
data_file.close()
