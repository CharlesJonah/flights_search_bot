class CustomAdaptiveCard:
    @staticmethod
    def create_flight_summary_adaptive_card(flight):
        print('--', flight)
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
                    "text": flight["travel_date"],
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
                                    "text": flight["origin_city"],
                                    "isSubtle": True,
                                },
                                {
                                    "type": "TextBlock",
                                    "size": "extraLarge",
                                    "color": "accent",
                                    "text": flight["origin"],
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
                                    "text": flight["destination_city"],
                                    "isSubtle": True,
                                },
                                {
                                    "type": "TextBlock",
                                    "horizontalAlignment": "right",
                                    "size": "extraLarge",
                                    "color": "accent",
                                    "text": flight["destination"],
                                    "spacing": "none",
                                },
                            ],
                        },
                    ],
                },
                {
                    "type": "TextBlock",
                    "text": flight["return_date"],
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
                                {"type": "TextBlock", "text": flight["destination_city"], "isSubtle": True},
                                {
                                    "type": "TextBlock",
                                    "size": "extraLarge",
                                    "color": "accent",
                                    "text": flight["destination"],
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
                                    "text": flight["origin_city"],
                                    "isSubtle": True,
                                },
                                {
                                    "type": "TextBlock",
                                    "horizontalAlignment": "right",
                                    "size": "extraLarge",
                                    "color": "accent",
                                    "text": flight["origin"],
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
                                    "text": "Total",
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
                                    "text": "$4,032.54",
                                    "size": "medium",
                                    "weight": "bolder",
                                }
                            ],
                        },
                    ],
                },
            ],
        }