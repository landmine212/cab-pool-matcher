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

    def save_state(self):
        """Save all cabs and waiting students to a readable JSON file."""
        waiting_list = []
        for queue in self.queues.values():
            for _, _, req in queue:
                waiting_list.append(req.to_dict())

        state = {
            "next_order": self.next_order,
            "cabs": [cab.to_dict() for cab in self.cabs],
            "waiting_requests": waiting_list,
        }

        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)

    def add_request(self, name, destination, time_slot, year):
        """Add a student request into the priority queue for their trip."""
        req = RideRequest(name, destination, time_slot, year, self.next_order)
        self.next_order += 1

        trip = (destination, time_slot)
        heapq.heappush(self.queues[trip], (-req.year, req.order, req))
        self.save_state()
        print(f"\nAdded request: {req.name} (Year {req.year}) -> {destination}, {time_slot}")

    def view_status(self):
        """Display everyone still waiting and the status of every cab."""
        print("\n--- WAITING LIST ---")
        any_waiting = False
        for (dest, slot), queue in self.queues.items():
            if queue:
                any_waiting = True
                print(f"\nTrip: {dest} - {slot}")
                for _, _, req in sorted(queue):
                    print(f"  * {req}")
        if not any_waiting:
            print("No students currently waiting.")

        print("\n--- ALL CABS ---")
        if not self.cabs:
            print("No cabs loaded.")
        for idx, cab in enumerate(self.cabs, start=1):
            print(f"{idx}. {cab}")

    def find_matches(self):
        """Preview who would get into each open cab right now without changing queues."""
        print("\n--- MATCH PREVIEW (NO SEATS ASSIGNED YET) ---")
        temp_queues = {trip: list(q) for trip, q in self.queues.items()}

        open_cabs = [cab for cab in self.cabs if not cab.has_left]
        if not open_cabs:
            print("No open cabs available right now.")
            return
