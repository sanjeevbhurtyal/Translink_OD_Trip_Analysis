TIME_PERIOD_MAP = {
    "Weekday (12:00am-8:29:59am)": "Weekday AM",
    "Weekday (8:30am-2:59:59pm)": "Weekday Interpeak",
    "Weekday (3:00pm-6:59:59pm)": "Weekday PM",
    "Weekday (7:00pm-11:59:59pm)": "Weekday Evening",
    "Weekend": "Weekend",
}

MONTH_MAP = {
    "01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr",
    "05": "May", "06": "Jun", "07": "Jul", "08": "Aug",
    "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dec",
}

OPERATOR_MODE_MAP = {
    # ------------------
    # Bus operators
    # ------------------
    "Brisbane Bus Lines": "bus",
    "Bus Qld Lockyer Valley": "bus",
    "Buslink Sunshine Coast": "bus",
    "Caboolture Bus Lines": "bus",
    "Clarks Logan City Bus Service": "bus",
    "Hornibrook Bus Lines": "bus",
    "Kangaroo Bus Lines": "bus",
    "Logan Coaches": "bus",
    "Mt Gravatt Bus Service": "bus",
    "Park Ridge Transit": "bus",
    "Sunbus": "bus",
    "Sunbus Sunshine Coast": "bus",
    "Surfside Buslines": "bus",
    "Thompson Bus Services": "bus",
    "Transdev Queensland": "bus",
    "Transport for Brisbane": "bus",
    "Westside Bus Company": "bus",

    # ------------------
    # Rail operators
    # ------------------
    "Queensland Rail": "rail",
    "Gold Coast Light Rail": "rail",

    # ------------------
    # Ferry operators
    # ------------------
    "TfB Ferries": "ferry",
    "SeaLink": "ferry",
}