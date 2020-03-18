class FlightSearch:
    """
      This is our application state. Just a regular serializable Python class.
    """

    def __init__(self, origin: str = None, destination: str = None, 
                  travel_date: str = None, return_date: str = None, return_trip: int = -1,
                  origin_city: str = None, destination_city: str = None,):
        self.origin = origin
        self.origin_city = origin_city
        self.destination = destination
        self.destination_city = destination_city
        self.return_trip = return_trip
        self.travel_date = travel_date
        self.return_date = return_date