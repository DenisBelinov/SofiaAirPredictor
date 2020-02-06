"""
usage: python download_weather_information.py <key> <latitude> <longitude>

result: a file containing HOURLY weather from today until 200 weeks back in the past
"""
import sys
import requests
import time

COUNT_SECONDS_IN_DAY = 86400

URL_TEMPLATE = "https://api.darksky.net/forecast/{}/{},{},{}?extend=hourly&exclude=currently,minutely,daily,alerts,flags"
WANTED_COLUMNS = ["time", "temperature", "windSpeed", "pressure", "humidity", "precipIntensity", "visibility" ]


def download_info(key, latitude, longitude):
    current_time_epoch = int(time.time())

    start_of_today = current_time_epoch - (current_time_epoch % COUNT_SECONDS_IN_DAY)

    out_file = str(latitude) + "," + str(longitude) + "_weather.csv"
    with open(out_file, "w+") as f:
        f.write(",".join(WANTED_COLUMNS) + "\n")
        current_time_iteration = start_of_today
        url = URL_TEMPLATE.format(key, latitude, longitude, current_time_iteration)
        r = requests.get(url)

        count = 0 # TODO: remove this
        while r.status_code == 200 and count < 200: # we don't need data before 200 weeks
            data = r.json()
            hourly_data = data["hourly"]["data"] # list of hourly data for the next

            for entry in reversed(hourly_data):
                content = map(str, [entry.get(col, 0) for col in WANTED_COLUMNS])
                line = ",".join(content)
                f.write(line + "\n")

            # because of the extend=hourly param in the API it returns the weather hourly for the next week
            current_time_iteration = current_time_iteration - 7 * COUNT_SECONDS_IN_DAY

            url = URL_TEMPLATE.format(key, latitude, longitude, current_time_iteration)
            r = requests.get(url)
            count += 1

            if count % 50 == 0:
                print("process: {} requests".format(count))

        print("Got {} lines".format(count))
        print("Reached {} time".format(current_time_iteration))


if __name__ == "__main__":
    key = sys.argv[1]
    latitude = sys.argv[2]
    longitude = sys.argv[3]

    download_info(key, latitude, longitude)