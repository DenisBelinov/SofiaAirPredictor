"""
Given a file path of sensor data, the script generates a new file with all the timestamps converted to linux epoch.
Also all times are rounded to an hour.

Added benefit: any excess headers are removed
"""
import sys
import datetime
import calendar


def convert_time_to_epoch(file_path):
    out_file_path = file_path + "_converted"
    with open(file_path, 'r') as in_file, open(out_file_path, "w+") as out_file:
        lines = iter(in_file.readlines())

        out_file.write(next(lines)) # write the csv header in the new file

        for line in lines:
            try:
                words = line.split(';')

                time = words[5]
                time = time.replace('-', ':')
                time = time.replace('T', ':')
                h = time.split(':')
                h = [int(i) for i in h]

                april_first = datetime.datetime(*h)
                epoch = calendar.timegm(april_first.timetuple())
                epoch = epoch - (epoch % 3600)
                words[5] = str(epoch)
                c = ';'
                line = c.join(words)

                out_file.write(line)
            except ValueError:
                continue


if __name__ == "__main__":
    file_path = sys.argv[1]

    convert_time_to_epoch(file_path)