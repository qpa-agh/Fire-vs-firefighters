import json


def loadParameters():
    """Load parameters from config file."""
    f = open('./config/config.json')
    data = json.load(f)
    width = data['width']
    rows = data['rows']
    f.close()
    return width, rows
