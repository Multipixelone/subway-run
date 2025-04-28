from nyct_gtfs import NYCTFeed

feed = NYCTFeed("A")
my_stop = ["A47N", "A47S"]
walking_time = 5

incoming_trains = set()

trains = feed.filter_trips(line_id=["C"], headed_for_stop_id=my_stop)
