"""
Usage:  python main.py <region-name> <dir-with-sensor-data> <dir-with-sensor-data>

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
    sensor_dirs = sys.argv[2:]

    print("Alias: {}".format(alias))

    merged_files = []

    # merge the files for each dir
    for dir in sensor_dirs:
        file_name = os.path.basename(dir)
        merged_file_path = merge_files(file_name, dir)

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
    # for file in merged_files:
    #     dir_to_remove = os.path.dirname(file)
    #     shutil.rmtree(dir_to_remove)

    # merge the merged files
    all_in_one_file_path = merge_files("all", merged_files_dir)


    # convert the time to linux epoch
    converted_file_path = convert_time_to_epoch(all_in_one_file_path)

    # merge the data by hour
    merge_hourly(converted_file_path)