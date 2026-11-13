import heapq
import json
import os
from models import RideRequest, Cab

VALID_DESTINATIONS = ["Delhi", "Jaipur"]
VALID_TIME_SLOTS = ["Morning", "Afternoon", "Evening", "Night"]
CABS_FILE = "cabs.json"
STATE_FILE = "state.json"
