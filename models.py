from datetime import datetime


class RideRequest:
    """Represents one student's request for a cab."""
def __init__(self, name, destination, time_slot, year, order, submitted_at=None):
        self.name = name
        self.destination = destination
        self.time_slot = time_slot
        self.year = year
