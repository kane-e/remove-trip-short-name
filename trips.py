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
    shortname_map = make_tripname_map(filepath)
    if not os.path.basename(filepath) == 'trips.txt':
        print(COLOR_RED + "Incorrect file input! Please input trips.txt" + COLOR_RESET)
        exit()
    make_new_file(filepath, shortname_map)

def make_tripname_map(filepath):
    short_name_map = {}
    with open(filepath, "rb") as trips_file_raw:
        trips_txt = io.TextIOWrapper(trips_file_raw)
        trips_csv = csv.DictReader(trips_txt)
        for row in trips_csv:
            if "trip_short_name" not in row or not row["trip_short_name"]:
                print(COLOR_BLUE + "no trip_short_name values are present and therefore cannot be deleted" + COLOR_RESET)
            short_name_map[row['trip_short_name']] = ''
    return(short_name_map)

def make_new_file(filepath, shortname_map, field_names=["trip_short_name"]):
    with open(filepath, "rb") as file_raw:
        trips_txt = io.TextIOWrapper(file_raw)
        csvfile = csv.DictReader(trips_txt)
        file_name = 'trips2.txt'
        if os.path.exists(file_name):
            print(COLOR_RED + "File with name " + file_name + " already exists in directory; cannot create a new one. Move this file and try again. Skipping..." + COLOR_RESET)
            return
        new_file = open(file_name, "w")
        new_csv_writer = csv.DictWriter(new_file, fieldnames=csvfile.fieldnames)
        new_csv_writer.writeheader()
        for row in csvfile:
            row_copy = row.copy()
            for field_name in field_names:
                if row[field_name] not in shortname_map:
                    print(COLOR_BLUE + "Invalid field name " + field_name + " for file " + file_name + ", skipping this file" + COLOR_RESET)
                    return
                found_trip_name = row_copy[field_name]
                row_copy[field_name] = shortname_map[found_trip_name] if found_trip_name in shortname_map else found_trip_name
            new_csv_writer.writerow(row_copy)
        new_file.close()
        print(COLOR_GREEN + "Exported " + file_name + " with trip short names removed" + COLOR_RESET)

if __name__ == "__main__":
    convert_trip_names()