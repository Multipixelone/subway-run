from nyct_gtfs import NYCTFeed
import threading
import datetime
import time

my_stop = ["A47N", "A47S"]
man_walking_time = 5
brk_walking_time = 2
feed_refresh_delay = 65

incoming_trains = set()


def get_trains(action):
    global feed

    if action == "refresh":
        feed.refresh()
        trains = feed.trips[0]
    else:
        feed = NYCTFeed("A")

    trains = feed.filter_trips(headed_for_stop_id=my_stop, underway=True)

    arrivals_north = []
    arrivals_south = []

    for train_num in range(len(trains)):
        stops = trains[train_num].stop_time_updates
        for stop in stops:
            if stop.stop_id == my_stop[0]:
                # get arrival time (in minutes) and train number.
                # Ignore trains arriving too soon
                arrival_time = int(
                    (stop.arrival - datetime.datetime.now()).total_seconds() / 60
                )
                if arrival_time >= man_walking_time:
                    arrivals_north.append([arrival_time, trains[train_num].route_id])

    for train_num in range(len(trains)):
        stops = trains[train_num].stop_time_updates
        for stop in stops:
            if stop.stop_id == my_stop[1]:
                # get arrival time (in minutes) and train number.
                # Ignore trains arriving too soon
                arrival_time = int(
                    (stop.arrival - datetime.datetime.now()).total_seconds() / 60
                )
                if arrival_time >= brk_walking_time:
                    arrivals_south.append([arrival_time, trains[train_num].route_id])

    arrivals_north.sort()
    arrivals_south.sort()
    return (arrivals_north, arrivals_south)


def main():
    trains_north, trains_south = get_trains("new")
    while True:
        # build ticker accordingly; show first two arrivals if more than one train
        # array content: trains[arrival time in minutes][train number e.g. "D"]
        if trains_north:
            if len(trains_north) > 1:
                north_text = "MAN ({}):{}', ({}):{}'".format(
                    trains_north[0][1],
                    trains_north[0][0],
                    trains_north[1][1],
                    trains_north[1][0],
                )
            else:
                north_text = "MAN ({}) in {}'".format(
                    trains_north[0][1], trains_north[0][0]
                )
        else:
            north_text = "No MAN train data."

        if trains_south:
            if len(trains_south) > 1:
                south_text = "BRK ({}):{}', ({}):{}'".format(
                    trains_south[0][1],
                    trains_south[0][0],
                    trains_south[1][1],
                    trains_south[1][0],
                )
            else:
                south_text = "BRK ({}) in {}'".format(
                    trains_south[0][1], trains_south[0][0]
                )
        else:
            south_text = "No BRK train data."

        print(north_text)
        print(south_text)
        time.sleep(feed_refresh_delay)
        trains_north, trains_south = get_trains("refresh")


if __name__ == "__main__":
    main()
