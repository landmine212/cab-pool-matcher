import heapq
import json
import os
from models import RideRequest, Cab

VALID_DESTINATIONS = ["Delhi", "Jaipur"]
VALID_TIME_SLOTS = ["Morning", "Afternoon", "Evening", "Night"]
CABS_FILE = "cabs.json"
STATE_FILE = "state.json"

class CabPoolMatcher:
    def __init__(self):
        self.cabs = []
        self.next_order = 1
        self.queues = {
            (dest, slot): []
            for dest in VALID_DESTINATIONS
            for slot in VALID_TIME_SLOTS
        }
        self.load_data()
