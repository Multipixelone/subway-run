from nyct_gtfs import NYCTFeed

feed = NYCTFeed("A")

incoming_trains = set()

trains = feed.filter_trips(line_id=["C"], headed_for_stop_id=["A47N"])

for train in trains:
    if train.stop_time_updates[0].stop_id == "A47N":
        incoming_trains.add((train.location_status, train.direction, train.arrival))
    print(incoming_trains)


# print(str(trains[0]))


# print(trains[0].stop_time_updates[0].stop_name)

# print(trains[0].stop_time_updates[0].arrival)
