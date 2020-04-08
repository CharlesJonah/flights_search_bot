class CustomAdaptiveCard:
    @staticmethod
    def create_number_of_passengers_card():
        return {
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "type": "AdaptiveCard",
            "version": "1.0",
            "body": [
                    {
                        "type": "TextBlock",
                        "text": "Passengers",
                        "size": "medium",
                        "isSubtle": True,
                    },
                {
                        "type": "Input.Number",
                        "id": "adults",
                        "placeholder": "Enter number of adults",
                        "min": 1,
                        "max": 1000,
                        "value": 3
                        },
                {
                        "type": "Input.Number",
                        "id": "children",
                        "placeholder": "Enter number of children",
                        "min": 1,
                        "max": 1000,
                        "value": 0
                        },
                {
                        "type": "Input.Number",
                        "id": "infants",
                        "placeholder": "Enter number of infants",
                        "min": 1,
                        "max": 1000,
                        "value": 0
                        }
            ],
            "actions": [
                {
                    "type": "Action.Submit",
                    "title": "Submit"
                }
            ]
        }

    @staticmethod
    def create_flight_summary_adaptive_card(flight_search, flight_search_results_url):
        return {
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "version": "1.0",
            "type": "AdaptiveCard",
            "body": [
                {
                    "type": "TextBlock",
                    "text": "Flight Search Summary",
                    "size": "extraLarge",
                    "weight": "bolder",
                    "isSubtle": False,
                },
                {
                    "type": "TextBlock",
                    "text": flight_search["travel_date"],
                    "weight": "bolder",
                    "spacing": "none",
                },
                {
                    "type": "ColumnSet",
                    "separator": True,
                    "columns": [
                        {
                            "type": "Column",
                            "width": 1,
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "text": flight_search["origin_city"],
                                    "isSubtle": True,
                                },
                                {
                                    "type": "TextBlock",
                                    "size": "extraLarge",
                                    "color": "accent",
                                    "text": flight_search["origin"],
                                    "spacing": "none",
                                },
                            ],
                        },
                        {
                            "type": "Column",
                            "width": "auto",
                            "items": [
                                {"type": "TextBlock", "text": " "},
                                {
                                    "type": "Image",
                                    "url": "http://messagecardplayground.azurewebsites.net/assets/airplane.png",
                                    "size": "small",
                                    "spacing": "none",
                                },
                            ],
                        },
                        {
                            "type": "Column",
                            "width": 1,
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "horizontalAlignment": "right",
                                    "text": flight_search["destination_city"],
                                    "isSubtle": True,
                                },
                                {
                                    "type": "TextBlock",
                                    "horizontalAlignment": "right",
                                    "size": "extraLarge",
                                    "color": "accent",
                                    "text": flight_search["destination"],
                                    "spacing": "none",
                                },
                            ],
                        },
                    ],
                },
                {
                    "type": "TextBlock",
                    "text": flight_search["return_date"],
                    "weight": "bolder",
                    "spacing": "none",
                },
                {
                    "type": "ColumnSet",
                    "separator": True,
                    "columns": [
                        {
                            "type": "Column",
                            "width": 1,
                            "items": [
                                {"type": "TextBlock",
                                    "text": flight_search["destination_city"], "isSubtle": True},
                                {
                                    "type": "TextBlock",
                                    "size": "extraLarge",
                                    "color": "accent",
                                    "text": flight_search["destination"],
                                    "spacing": "none",
                                },
                            ],
                        },
                        {
                            "type": "Column",
                            "width": "auto",
                            "items": [
                                {"type": "TextBlock", "text": " "},
                                {
                                    "type": "Image",
                                    "url": "http://messagecardplayground.azurewebsites.net/assets/airplane.png",
                                    "size": "small",
                                    "spacing": "none",
                                },
                            ],
                        },
                        {
                            "type": "Column",
                            "width": 1,
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "horizontalAlignment": "right",
                                    "text": flight_search["origin_city"],
                                    "isSubtle": True,
                                },
                                {
                                    "type": "TextBlock",
                                    "horizontalAlignment": "right",
                                    "size": "extraLarge",
                                    "color": "accent",
                                    "text": flight_search["origin"],
                                    "spacing": "none",
                                },
                            ],
                        },
                    ],
                },
                {
                    "type": "ColumnSet",
                    "spacing": "medium",
                    "columns": [
                        {
                            "type": "Column",
                            "width": "1",
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "text": "Adults",
                                    "size": "medium",
                                    "isSubtle": True,
                                },
                                {
                                    "type": "TextBlock",
                                    "text": "Children",
                                    "size": "medium",
                                    "isSubtle": True,
                                },
                                {
                                    "type": "TextBlock",
                                    "text": "Infants",
                                    "size": "medium",
                                    "isSubtle": True,
                                }
                            ],
                        },
                        {
                            "type": "Column",
                            "width": 1,
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "horizontalAlignment": "right",
                                    "text": flight_search["adults"],
                                    "size": "medium",
                                    "weight": "bolder",
                                },
                                {
                                    "type": "TextBlock",
                                    "horizontalAlignment": "right",
                                    "text": flight_search["children"],
                                    "size": "medium",
                                    "weight": "bolder",
                                },
                                {
                                    "type": "TextBlock",
                                    "horizontalAlignment": "right",
                                    "text": flight_search["infants"],
                                    "size": "medium",
                                    "weight": "bolder",
                                }
                            ],
                        },
                    ],
                },
                {
                    "type": "ActionSet",
                    "actions": [
                        {
                            "type": "Action.OpenUrl",
                            "title": "Search Flights",
                            "url": flight_search_results_url
                        },
                        {
                            "type": "Action.Submit",
                            "title": "Modify Flight Search",
                            "data": 'modify'
                        },
                        {
                            "type": "Action.Submit",
                            "title": "Exit/Cancel",
                            "data": 'exit'
                        }
                    ]
                }
            ],
        }
