"""
Usage:  python get_sensor_info.py _sds011_sensor_34801.csv

Given a file sufix of the sensor, this script goes to http://archive.luftdaten.info/
and fetches all the files with that sufix since 01-01-2016 and dumps them in a directory.

Then merges all the files into one called <file-sufix>_merged.csv
"""

import requests
import datetime
import os
import sys
import glob
import shutil

ARCHIVE_URL = "http://archive.luftdaten.info/"

FIRST_SENSOR_DATE = datetime.date(2016, 1, 1)


def download_files(sensor_suffix):
    """
    :param sensor_suffix: the sufix of the sensor files
    :return: the output directory of the files
    """
    current_dir = os.getcwd()
    output_dir = os.path.join(current_dir, sensor_suffix.split('.')[0])

    os.mkdir(output_dir)

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

    print("Got {} files".format(file_count))
    return output_dir


def merge_files(suffix, full_path):
    """
    Merges all the files in a directory into one file.

    :param suffix the sufix of the downloaded files - this is used for the merged file name
    :param full_path the full path to the directory
    :return full_path to the merged file
    """
    out_file_name = suffix.split('.')[0] + "_merged.csv"
    out_file_path = os.path.join(full_path, out_file_name)

    with open(out_file_path, 'wb') as outfile:
        for filename in glob.glob('{}/*.csv'.format(full_path)):
            if filename == out_file_path:
                # don't want to copy the output into the output
                continue
            with open(filename, 'rb') as readfile:
                shutil.copyfileobj(readfile, outfile)

    return out_file_path


if __name__ == "__main__":
    suffix = sys.argv[1]

    files_dir_path = download_files(suffix)
    merged_file_path = merge_files(suffix, files_dir_path)
