import csv
import glob
from collections import Counter
from operator import itemgetter
import dateutil.parser
import matplotlib.pyplot as plt


def number_of_line_csv(csvfile):
    with open(csvfile, 'r') as csv_reader:
        reader = csv.reader(csv_reader)
        row_count = sum(1 for row in reader)
        return row_count


def top_10_airports(csvfile):
    airports_names_passengers_number_dict = dict()
    with open(csvfile, 'r') as csv_reader:
        data = csv.reader(csv_reader, delimiter='^', quotechar='\'')
        next(data, None)
        for row in data:
            try:
                airports_name = row[12].strip()
                number_of_passengers = row[34]
                if (not airports_name in airports_names_passengers_number_dict):
                    airports_names_passengers_number_dict[
                        airports_name] = number_of_passengers
                else:
                    airports_names_passengers_number_dict[airports_name] = int(
                        airports_names_passengers_number_dict[airports_name]) + int(number_of_passengers)
            except:
                pass

        return Counter(airports_names_passengers_number_dict).most_common(10)


def plot_monthly_number_of_searches(csvfile, dest=[]):
    date_list = []
    month_number_of_occ_dict = dict()
    dest_month_dict = {d: {} for d in dest}
    with open(csvfile, 'r') as csv_reader:
        data = csv.reader(csv_reader, delimiter='^', quotechar='\'')
        next(data, None)
        for row in data:
            try:
                date = row[0]
                destination = row[6]
                for d in dest:
                    if(d == destination):
                        t = dateutil.parser.parse(date, fuzzy=True)
                        month = t.month
                        month_number_of_occ_dict = dest_month_dict[d]
                        if(not month in month_number_of_occ_dict):
                            month_number_of_occ_dict[month] = 1
                        else:
                            month_number_of_occ_dict[month] = int(
                                month_number_of_occ_dict[month]) + 1
                        dest_month_dict[d] = month_number_of_occ_dict
            except:
                pass
        for dest_plot in dest_month_dict.keys():
            counter = Counter(dest_month_dict[dest_plot])
            list_month_occ = sorted(counter.items(), key=itemgetter(0))
            plt.plot([p[0] for p in list_month_occ], [p[1] for p in list_month_occ], label=dest_plot)
        plt.title(
            "Searches for flights arriving at Malaga, Madrid or Barcelona")
        plt.legend(loc='upper right')
        plt.show()


def match_searches_bookings(searchesfile, bookingsfile):
    with open(searchesfile, 'r') as csv_searches, open(bookingsfile, 'r') as csv_bookings:
        searches = csv.reader(csv_searches, delimiter='^', quotechar='\'')
        bookings = csv.reader(csv_bookings, delimiter='^', quotechar='\'')
        next(searches, None)
        next(bookings, None)
        for row_searches in searches:
            for row_bookings in bookings:
                try:
                    searches_origin = row_searches[5]
                    searches_destination = row_searches[6]

                    bookings_dep_port = row_bookings[9].strip()
                    booking_arr_port = row_bookings[12].strip()

                    if(searches_origin == bookings_dep_port and searches_destination == booking_arr_port):
                        print searches_origin, searches_destination, "1"
                except:
                    pass


def main():

    # First exercise: count the number of lines in Python for each file
    # (csv header included)
    files_to_read = glob.glob("*.csv")
    for file_name in files_to_read:
        print "number of lines in : ", file_name, number_of_line_csv(file_name)

    # Second exercise: top 10 arrival airports in the world in 2013 (using the bookings file)
    #(csv header excluded) !!!One line is missing data!!!
    print "Top 10 arrival airports in the world in 2013 and their passengers number : ", top_10_airports("bookings.csv")

    # Third exercise: plot the monthly number of searches for flights arriving
    # at Malaga, Madrid or Barcelona
    plot_monthly_number_of_searches("searches.csv", ["AGP", "MAD", "BCN"])

    #Bonus exercise 1 : match searches with bookings
    #work in progress
    #match_searches_bookings("searches.csv", "bookings.csv")


if __name__ == "__main__":
    main()
