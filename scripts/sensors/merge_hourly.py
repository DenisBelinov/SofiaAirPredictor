"""
Given a file containing a csv sensor data with time converted in Epoch
1. Trims the data to just timestamp, p1, p2
2. Sorts the data
3. Merges all data with the same hour into one, averaging all the entries

usage: python merge_hourly.py <file-path>

output: a file with the data merged
"""
import sys


def trim_lines(lines):
    """
    Currently the indexes are hardcoded, lets hope all csv are the same format :)

    :param lines: a list of lines from a csv file of sensor data

    :return: a list of lists containing the needed information from the sensor
    :type: [[timestamp, P1, P2]]
    """
    new_lines = []

    for line in lines:
        split_line = line.split(';')

        timestamp = split_line[5]
        p1 = split_line[6]
        p2 = split_line[9]

        new_lines.append([timestamp, p1, p2])

    return new_lines


def merge_hourly(file_path):
    out_file_path = file_path + "_merged_hourly"
    with open(file_path, 'r') as in_file, open(out_file_path, "w+") as out_file:
        lines = in_file.readlines()

        trimmed_data = trim_lines(lines[1:]) # remove the first heading row

        sorted_data = sorted(trimmed_data, key=lambda data: data[0])

        count = 0
        epoch = 0
        p1Sum = 0
        p2Sum = 0

        for data in sorted_data:
            currentEpoch = int(data[0])
            try:
                p1 = float(data[1])
                p2 = float(data[2])
            except ValueError:
                continue

            # TODO: remove this when we find the cause of faulty data
            if p1 > 600 or p2 > 600:
                print("I've found a strange entry on: {}, skipping it.".format(currentEpoch))
                continue

            if (epoch != currentEpoch and epoch != 0):
                p1Sum /= count
                p2Sum /= count

                values = [str(epoch), str(p1Sum), str(p2Sum)]
                c = ';'
                out_file.write(c.join(values) + "\n")
                p1Sum = 0
                p2Sum = 0
                count = 0

            epoch = currentEpoch

            p1Sum += p1
            p2Sum += p2
            count += 1

        if p1Sum + p2Sum != 0:
            p1Sum /= count
            p2Sum /= count
            values = [str(epoch), str(p1Sum), str(p2Sum)]
            c = ';'
            out_file.write(c.join(values) + "\n")


if __name__ == "__main__":
    file_path = sys.argv[1]

    merge_hourly(file_path)


