"""
Given a full path to a directory, merges all the file contents into one file.

usage: python file_merger.py <directory>

output: a file in the given <directory> which contains the content of all the files in the <directory>
"""
import sys
import shutil
import os
import glob


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
    merge_files(sys.argv[1])