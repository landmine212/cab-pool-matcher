from datetime import datetime


class RideRequest:
    """Represents one student's request for a cab."""
def __init__(self, name, destination, time_slot, year, order, submitted_at=None):
        self.name = name
        self.destination = destination
        self.time_slot = time_slot
        self.year = year
        self.order = order
        self.submitted_at = submitted_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def to_dict(self):
        """Convert object into a dictionary for JSON saving."""
        return {
            "name": self.name,
            "destination": self.destination,
            "time_slot": self.time_slot,
            "year": self.year,
            "order": self.order,
            "submitted_at": self.submitted_at,
        }
