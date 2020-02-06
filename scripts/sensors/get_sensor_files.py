"""
Given a file sufix of the sensor, this script goes to http://archive.luftdaten.info/
and fetches all the files with that sufix since 01-01-2016 and dumps them in a directory.

Usage: python get_sensor_files.py _sds011_sensor_34801.csv

output: a directory with all the files in the archivce since @FIRST_SENSOR_DATE
"""
import datetime
import os
import requests
import sys

ARCHIVE_URL = "http://archive.luftdaten.info/"

FIRST_SENSOR_DATE = datetime.date(2016, 1, 1)


def download_files(sensor_suffix):
    """
    :param sensor_suffix: the sufix of the sensor files
    :return: the output directory of the files
    """
    current_dir = os.getcwd()
    output_dir = os.path.join(current_dir, sensor_suffix.split('.')[0])

    try:
        os.mkdir(output_dir)
    except FileExistsError:
        pass

    current_date = FIRST_SENSOR_DATE
    today = datetime.date.today()
    file_count = 0

    while current_date < today:
        file_name = str(current_date) + sensor_suffix
        file_path = os.path.join(output_dir, file_name)

        url = ARCHIVE_URL + str(current_date) + "/" + file_name
        r = requests.get(url=url)

        if r.status_code == 200:
            with open(file_path, "w+") as output_file:
                output_file.write(r.text)

            file_count += 1

        current_date = current_date + datetime.timedelta(days=1)

    print("Got {} files for sensor {}".format(file_count, sensor_suffix))
    return output_dir


if __name__ == "__main__":
    suffix = sys.argv[1]

    download_files(suffix)