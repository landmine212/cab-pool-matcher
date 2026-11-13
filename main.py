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
    def load_cabs_from_file(self):
        """Load initial cabs from cabs.json."""
        if not os.path.exists(CABS_FILE):
            print(f"Error: '{CABS_FILE}' not found. Starting with 0 cabs.")
            return []
        try:
            with open(CABS_FILE, "r", encoding="utf-8") as f:
                raw_cabs = json.load(f)
            return [Cab.from_dict(item) for item in raw_cabs]
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error reading '{CABS_FILE}': {e}. Starting with 0 cabs.")
            return []

    def load_data(self):
        """Load previous state if state.json exists; otherwise start fresh from cabs.json."""
        if not os.path.exists(STATE_FILE):
            self.cabs = self.load_cabs_from_file()
            return

        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

                self.next_order = data["next_order"]
            self.cabs = [Cab.from_dict(c) for c in data["cabs"]]

            for item in data["waiting_requests"]:
                req = RideRequest.from_dict(item)
                trip = (req.destination, req.time_slot)
                heapq.heappush(self.queues[trip], (-req.year, req.order, req))

            print("Previous session restored from state.json!")
        except (json.JSONDecodeError, KeyError, TypeError):
            print("Warning: state.json was missing or corrupted. Starting fresh from cabs.json.")
            self.cabs = self.load_cabs_from_file()
