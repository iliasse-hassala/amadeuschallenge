import web
import csv
from collections import Counter
import json

# usage 0.0.0.0:8080/top_airports/n (where n is the number of the Top n airports)

csvfile = "bookings.csv"

urls = (
    '/top_airports/(.*)', 'index'
)


class index:

    def GET(self, n):
        airports_names_passengers_number_dict = dict()
        with open(csvfile, 'r') as csv_reader:
            data = csv.reader(csv_reader, delimiter='^', quotechar='\'')
            next(data, None)
            for row in data:
                try:
                    airports_name = row[12].strip()
                    number_of_passengers = row[34]
                    if (not airports_name in airports_names_passengers_number_dict):
                        airports_names_passengers_number_dict[airports_name] = number_of_passengers
                    else:
                        airports_names_passengers_number_dict[airports_name] = int(airports_names_passengers_number_dict[airports_name]) + int(number_of_passengers)
                except:
                    pass
            counter = Counter(airports_names_passengers_number_dict).most_common(int(n))
            counter_json = json.dumps(counter)
            return counter_json


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
