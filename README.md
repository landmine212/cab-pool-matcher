# SUTT Backend Task 1: Cab Pool Matcher

A command-line Python application to organize end-of-semester cab sharing from BITS Pilani to **Delhi** and **Jaipur**, giving priority to senior students when seats are limited.

## How to Run

1. Make sure **Python 3** is installed on your computer (no external packages are required).
2. Open a terminal inside this project folder (`cab-pool-matcher`) and run:
   ```bash
   python main.py
   ```
3. Follow the numbered menu prompts (`1` to `5`) in the terminal to add ride requests, preview matches, or dispatch cabs.
4. *(Optional)* To reset the app back to a fresh state, delete `state.json` and run `python main.py` again.

## Cab File Format (`cabs.json`)

When the app starts fresh, it loads the available cabs from `cabs.json`. Each cab entry specifies the driver's name, seat capacity (`1` to `4`), destination (`Delhi` or `Jaipur`), and time slot (`Morning`, `Afternoon`, `Evening`, or `Night`):

```json
[
  {
    "driver_name": "Ramesh Kumar",
    "capacity": 4,
    "destination": "Delhi",
    "time_slot": "Morning"
  },
  {
    "driver_name": "Vikram Verma",
    "capacity": 2,
    "destination": "Jaipur",
    "time_slot": "Afternoon"
  }
]
```

## Why JSON Instead of `pickle`?

* **Human-Readable:** Anyone can open `cabs.json` or `state.json` in a text editor to inspect, verify, or debug waiting queues and cab assignments.
* **Safe:** Python's `pickle` module can execute arbitrary code when loading untrusted files, whereas `json` only stores plain data.
* **Portable:** JSON is a universal text format that works across different Python versions and other programming languages.

---

## Answers to Tricky Situations

### 1. Half-Empty Cab
When **Dispatch a Cab** is chosen, the app pops students from that trip's priority queue until **either** the cab reaches its seat capacity **or** the waiting queue becomes empty. If only 1 or 2 students are waiting, the cab still departs with those students, marks `has_left = True`, and never accepts new passengers afterward.

### 2. No Cabs Left
If all cabs for a specific trip (or all cabs overall) have already left, new students can still submit requests and remain safely stored in their trip's priority queue. If the user attempts to dispatch a cab for a trip with no open cabs left, the app prints `"Cannot dispatch: No open cabs left..."` and leaves the waiting queue unchanged so no student's request is ever lost.

### 3. Same-Year Tie-Breaking
Each request is given an incremental integer `order` (`1, 2, 3, ...`) when created and is stored in Python's `heapq` as the tuple:
`(-request.year, request.order, request)`

* `-request.year` ensures higher years pop first (for example, `-5` pops before `-4`).
* If two students are in the same year, Python compares `request.order` next, so whoever requested earlier (`order = 2` vs `order = 5`) gets the seat first.
* Because `order` is unique for every request, Python never attempts to directly compare two `RideRequest` objects (which would raise a `TypeError`).

### 4. Performance at Scale (1,000 Waiting Requests)
Let `N = 1,000` be the number of waiting students in a trip's queue, and `C` be the total number of cabs:

* **Adding one request:** `O(log N)` — Inserting into a binary heap (`heapq.heappush`) only swaps elements along the height of the tree (`log2(1000)` is about 10 steps).
* **Adding all 1,000 requests:** `O(N log N)` — Performing `N` heap insertions, each taking `O(log N)` time.
* **Sending off one cab (up to 4 students):** `O(K log N) = O(log N)` — Popping up to `K <= 4` students with `heapq.heappop` takes `O(log N)` per student, and `K` is bounded by a small constant (at most 4).
* **Finding an open cab for a trip:** `O(C)` — The app scans the cab list in fixed file order until it finds the first matching cab where `has_left` is `False`.
