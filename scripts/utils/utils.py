import json


def loadParameters():
    """Load parameters from config file."""
    f = open('./config/config.json')
    data = json.load(f)
    rows = data['rows']
    gap = data['gap']
    f.close()
    return rows, gap
