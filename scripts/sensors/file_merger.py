"""
Given a full path to a directory, merges all the file contents into one file.

I left this script in case we need to merge any other files.
"""
import sys
import shutil
import os
import glob


def main(full_path):
    out_file_name = "merged.csv"
    out_file_path = os.path.join(full_path, out_file_name)

    with open(out_file_path, 'wb') as outfile:
        for filename in glob.glob('{}/*.csv'.format(full_path)):
            if filename == out_file_path:
                # don't want to copy the output into the output
                continue
            with open(filename, 'rb') as readfile:
                shutil.copyfileobj(readfile, outfile)


if __name__ == "__main__":
    main(sys.argv[1])