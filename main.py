import argparse
import csv
import datetime
import os


class Reading:

    def __init__ (self, min_temp, max_temp, date, max_humidity, mean_temp, mean_humidity):
        self.min_temp = min_temp
        self.max_temp = max_temp
        self.date = date
        self.max_humidity = max_humidity
        self.mean_temp = mean_temp
        self.mean_humidity = mean_humidity

    def __str__(self):
        return "Date: {}, Min Temp: {}, Max Temp: {}, Max Humidity: {}, Mean Temp: {}, Mean Humidity: {}".format(
            self.date, self.min_temp, self.max_temp, self.max_humidity, self.mean_temp, self.mean_humidity )


class Result:
    def __init__(self, value, date):
        self.value = value
        self.date = date


class FileHandler:
    def __init__ (self):
        self.dir_path = 'weatherfiles\\'

    def read_data(self, file_name, readings):
        with open(self.dir_path + file_name, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                reading = Reading(row['Min TemperatureC'], row['Max TemperatureC'], row['PKT'], row['Max Humidity'], row['Mean TemperatureC'], row[' Mean Humidity'])
                readings.append(reading)

    def get_yearly_data(self, year):
        file_names = os.listdir(self.dir_path)

        chosen_filenames = []
        year = str(year)
        for file_name in file_names:
            if year in file_name:
                chosen_filenames.append(file_name)

        readings = []

        for chosen_filename in chosen_filenames:
            self.read_data(chosen_filename, readings)

        return readings

    def get_monthly_data(self, year, month):
        file_names = os.listdir(self.dir_path)
        datetime_obj = datetime.datetime.strptime(str(month), "%m")
        month_name = datetime_obj.strftime("%b")

        chosen_filename = None
        year = str(year)
        for file_name in file_names:
            if year in file_name and month_name in file_name:
                chosen_filename = file_name

        readings = []
        self.read_data(chosen_filename, readings)
        return readings


def get_max_temp(readings):
    result = Result(float('-inf'), None)
    for reading in readings:
        if reading.max_temp.isdigit():
            current_value = int(reading.max_temp)
            if current_value > result.value:
                result.value = current_value
                result.date = reading.date
    return result


def get_min_temp(readings):
    result = Result(float('inf'), None)
    for reading in readings:
        if reading.min_temp.isdigit():
            current_value = int(reading.min_temp)
            if current_value < result.value:
                result.value = current_value
                result.date = reading.date
    return result


def get_max_humidity(readings):
    result = Result(float('-inf'), None)
    for reading in readings:
        if reading.max_humidity.isdigit():
            current_value = int(reading.max_humidity)
            if current_value > result.value:
                result.value = current_value
                result.date = reading.date
    return result


def convert_date(date):
    return datetime.datetime.strptime(date, "%Y-%m-%d").date()


def get_highest_avg_temp(readings):
    highest_avg_temp = float('-inf')
    for reading in readings:
        if reading.mean_temp.isdigit():
            current_value = int(reading.mean_temp)
            if current_value > highest_avg_temp:
                highest_avg_temp = current_value
    return highest_avg_temp


def get_lowest_avg_temp(readings):
    lowest_avg_temp = float('inf')
    for reading in readings:
        if reading.mean_temp.isdigit():
            current_value = int(reading.mean_temp)
            if current_value < lowest_avg_temp:
                lowest_avg_temp = current_value
    return lowest_avg_temp


def get_avg_mean_humidity(readings):
    humidity_sum = 0
    count = 0
    for reading in readings:
        if reading.mean_humidity.isdigit():
           humidity_sum = int(reading.mean_humidity) + humidity_sum
           count = 1 + count
    return humidity_sum/count


def print_yearly_output(year):
    file_handler = FileHandler()
    yearly_data = file_handler.get_yearly_data(year)

    max_temp_result = get_max_temp(yearly_data)
    max_temp_date = convert_date(max_temp_result.date)
    max_temp_month = max_temp_date.strftime("%B")
    print("Highest: {}C on {} {}" .format(max_temp_result.value, max_temp_month, max_temp_date.day))

    min_temp_result =  get_min_temp(yearly_data)
    min_temp_date = convert_date(min_temp_result.date)
    min_temp_month = min_temp_date.strftime("%B")
    print("Lowest: {}C on {} {}".format(min_temp_result.value, min_temp_month, min_temp_date.day))

    max_humidity_result = get_max_humidity(yearly_data)
    max_humidity_date = convert_date(max_humidity_result.date)
    max_humidity_month = max_humidity_date.strftime("%B")
    print("Humidity: {}% on {} {}".format(max_humidity_result.value, max_humidity_month, max_humidity_date.day))


def print_monthly_output(year, month):
    file_handler = FileHandler()
    monthly_data = file_handler.get_monthly_data(year, month)

    avg_highest_temp_result = get_highest_avg_temp(monthly_data)

    print("Highest Average: {}C".format(avg_highest_temp_result))

    print("Lowest Average: {}C".format(get_lowest_avg_temp(monthly_data)))

    print("Average Mean Humidity: {}%".format(get_avg_mean_humidity(monthly_data)))




def main():
    # print_yearly_output(2004)
    # print_monthly_output(2005, 8)
    parser = argparse.ArgumentParser()
    parser.add_argument("format", help="yearly or monthly format of data")
    parser.add_argument("date", help="date")

    args = parser.parse_args()

    print(args.format)
    print(args.date)


if __name__ == '__main__':
        main()