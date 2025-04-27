from nyct_gtfs import NYCTFeed

feed = NYCTFeed("C")

print(feed.filter_trips(line_id=["C"]))
