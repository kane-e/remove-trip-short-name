import sys
import os
import csv
import io

COLOR_RED   = "\033[1;31m"
COLOR_BLUE  = "\033[1;34m"
COLOR_GREEN = "\033[0;32m"
COLOR_RESET = "\033[0;0m"

def convert_trip_names():
    filepath = sys.argv[1]
    if len(sys.argv) < 2:
        print(COLOR_RED + "No filename provided!" + COLOR_RESET)
        exit()
    if not os.path.isfile(filepath):
        print(COLOR_RED + "File does not exist!" + COLOR_RESET)
    if not os.path.basename(filepath) == 'trips.txt':
        print(COLOR_RED + "Incorrect file input! Please input trips.txt" + COLOR_RESET)
        exit()
    make_new_file(filepath)

def make_new_file(filepath):
    with open(filepath, "rb") as file_raw:
        trips_txt = io.TextIOWrapper(file_raw)
        csv_file = csv.DictReader(trips_txt)
        csv_list = list(csv_file)
        for row in csv_list:
            if "trip_short_name" not in row or not row["trip_short_name"]:
                print(COLOR_BLUE + "no trip_short_name values are present and therefore cannot be deleted" + COLOR_RESET)
                return
        file_name = 'trips2.txt'
        if os.path.exists(file_name):
            print(COLOR_RED + "File with name " + file_name + " already exists in directory; cannot create a new one. Move this file and try again. Skipping..." + COLOR_RESET)
            return
        new_file = open(file_name, "w")
        new_csv_writer = csv.DictWriter(new_file, fieldnames=csv_file.fieldnames)
        new_csv_writer.writeheader()
        for row in csv_list:
            row["trip_short_name"] = ""
            new_csv_writer.writerow(row)
        new_file.close()
        print(COLOR_GREEN + "Exported " + file_name + " with trip short names removed" + COLOR_RESET)

if __name__ == "__main__":
    convert_trip_names()