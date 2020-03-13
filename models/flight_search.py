class FlightSearch:
    """
      This is our application state. Just a regular serializable Python class.
    """

    def __init__(self, origin: str = None, destination: str = None, 
                  travel_date: str = None, return_date: str = None, return_trip: int = -1):
        self.origin = origin
        self.destination = destination
        self.return_trip = return_trip
        self.travel_date = travel_date
        self.return_date = return_date