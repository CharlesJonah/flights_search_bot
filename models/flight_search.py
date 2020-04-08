class FlightSearch:
    """
      Flight search  state management class
    """

    def __init__(self, origin: str = None, destination: str = None,
                 travel_date: str = None, return_date: str = None, return_trip: str = 'no',
                 origin_city: str = None, destination_city: str = None, cabin_class: str = None,
                 adults: int = 1, children: int = 0, infants: int = 0):
        self.origin = origin
        self.origin_city = origin_city
        self.destination = destination
        self.destination_city = destination_city
        self.return_trip = return_trip
        self.travel_date = travel_date
        self.return_date = return_date
        self.cabin_class = cabin_class
        self.adults = adults
        self.children = children
        self.infants = infants
