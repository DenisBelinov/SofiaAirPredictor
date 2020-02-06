"""
Usage:  python main.py <region-name> _sds011_sensor_34801.csv _sds011_sensor_123.csv _sds011_sensor_1337.csv

output:
a directory called <region-name>_merged with contents:
  1. a file <sensor_suffix>_merged for each sensor containing all the data merged
  2. all_merged.csv - a file containing all the data from the sensors merged
  3. all_merged.csv_converted - same as all_merged.csv but with the timestamps changed to epoch
  4. all_merged.csv_converted_merged_hourly - all the data, but merged by hour
"""

import os
import sys
import shutil

from get_sensor_files import download_files
from datetime_to_epoch import convert_time_to_epoch
from file_merger import merge_files
from merge_hourly import merge_hourly


if __name__ == "__main__":
    alias = sys.argv[1]
    suffixes = sys.argv[2:]

    print("Alias: {}".format(alias))
    print("Sensors: {}".format(suffixes))

    merged_files = []
    # get the files and merge them for each suffix
    for suffix in suffixes:
        files_dir_path = download_files(suffix)
        merged_file_path = merge_files(suffix, files_dir_path)

        merged_files.append(merged_file_path)

    # move the merged files to a different dir and merge them in one
    current_dir = os.getcwd()
    merged_files_dir = os.path.join(current_dir, alias + "_merged")

    try:
        os.mkdir(merged_files_dir)
    except FileExistsError:
        pass

    for file_path in merged_files:
        target_path = os.path.join(merged_files_dir, os.path.basename(file_path))
        shutil.move(file_path, target_path)

    # cleanup all files from the sensors
    for file in merged_files:
        dir_to_remove = os.path.dirname(file)
        shutil.rmtree(dir_to_remove)

    # merge the merged files
    all_in_one_file_path = merge_files("all", merged_files_dir)


    # convert the time to linux epoch
    converted_file_path = convert_time_to_epoch(all_in_one_file_path)

    # merge the data by hour
    merge_hourly(converted_file_path)


