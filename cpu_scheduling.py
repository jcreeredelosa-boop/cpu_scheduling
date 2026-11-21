# Operating Systems Laboratory Activity 2
# CPU Scheduling Simulator - Python 3

from collections import deque
from copy import deepcopy

# Dataset for FCFS, SJF, Priority Scheduling, and Round Robin
PROCESSES = [
    {"pid": "P1", "at": 0, "bt": 6, "priority": 3},
    {"pid": "P2", "at": 0, "bt": 3, "priority": 1},
    {"pid": "P3", "at": 0, "bt": 5, "priority": 4},
    {"pid": "P4", "at": 0, "bt": 2, "priority": 2},
]

# Separate dataset for SRTF, as required by the laboratory activity
SRTF_PROCESSES = [
    {"pid": "P1", "at": 0, "bt": 8, "priority": 2},
    {"pid": "P2", "at": 1, "bt": 4, "priority": 1},
    {"pid": "P3", "at": 2, "bt": 2, "priority": 4},
    {"pid": "P4", "at": 3, "bt": 1, "priority": 3},
]


def prepare(processes):
    """Make a fresh working copy and initialize scheduling fields."""
    result = deepcopy(processes)
    for process in result:
        process["remaining"] = process["bt"]
        process["first_start"] = None
    return result


def record_run(process, start, end, gantt):
    """Record a CPU interval and update the process state."""
    if start == end:
        return

    # Merge consecutive intervals belonging to the same process.
    if gantt and gantt[-1][2] == process["pid"] and gantt[-1][1] == start:
        gantt[-1] = (gantt[-1][0], end, process["pid"])
    else:
        gantt.append((start, end, process["pid"]))

    if process["first_start"] is None:
        process["first_start"] = start

    process["remaining"] -= end - start
    if process["remaining"] == 0:
        process["ct"] = end


def finish_results(processes):
    """Calculate turnaround, waiting, and response times."""
    for process in processes:
        process["tat"] = process["ct"] - process["at"]
        process["wt"] = process["tat"] - process["bt"]
        process["rt"] = process["first_start"] - process["at"]


def fcfs(data):
    """First-Come, First-Served scheduling."""
    processes = prepare(data)
    time = 0
    gantt = []

    for process in sorted(processes, key=lambda p: (p["at"], p["pid"])):
        if time < process["at"]:
            time = process["at"]
        start = time
        time += process["bt"]
        record_run(process, start, time, gantt)

    finish_results(processes)
    return processes, gantt


def non_preemptive(data, mode):
    """Non-preemptive SJF or Priority scheduling."""
    processes = prepare(data)
    time = 0
    completed = set()
    gantt = []

    while len(completed) < len(processes):
        ready = [
            p for p in processes
            if p["pid"] not in completed and p["at"] <= time
        ]

        if not ready:
            time = min(
                p["at"] for p in processes if p["pid"] not in completed
            )
            continue

        if mode == "sjf":
            chosen = min(ready, key=lambda p: (p["bt"], p["at"], p["pid"]))
        elif mode == "priority":
            # A smaller priority number means a higher priority.
            chosen = min(
                ready, key=lambda p: (p["priority"], p["at"], p["pid"])
            )
        else:
            raise ValueError("mode must be 'sjf' or 'priority'")

        start = time
        time += chosen["bt"]
        record_run(chosen, start, time, gantt)
        completed.add(chosen["pid"])

    finish_results(processes)
    return processes, gantt


def round_robin(data, quantum=2):
    """Round Robin scheduling using the specified time quantum."""
    if quantum <= 0:
        raise ValueError("Time quantum must be greater than zero.")

    processes = prepare(data)
    by_arrival = sorted(processes, key=lambda p: (p["at"], p["pid"]))
    ready = deque()
    gantt = []
    time = 0
    index = 0

    while index < len(by_arrival) or ready:
        if not ready:
            time = max(time, by_arrival[index]["at"])

        while index < len(by_arrival) and by_arrival[index]["at"] <= time:
            ready.append(by_arrival[index])
            index += 1

        process = ready.popleft()
        start = time
        end = time + min(quantum, process["remaining"])
        record_run(process, start, end, gantt)
        time = end

        # Add newly arrived processes before re-queuing the unfinished one.
        while index < len(by_arrival) and by_arrival[index]["at"] <= time:
            ready.append(by_arrival[index])
            index += 1

        if process["remaining"] > 0:
            ready.append(process)

    finish_results(processes)
    return processes, gantt


def srtf(data):
    """Preemptive Shortest Remaining Time First scheduling."""
    processes = prepare(data)
    time = min(p["at"] for p in processes)
    completed = set()
    gantt = []

    while len(completed) < len(processes):
        ready = [
            p for p in processes
            if p["at"] <= time
            and p["pid"] not in completed
            and p["remaining"] > 0
        ]

        if not ready:
            time = min(
                p["at"] for p in processes
                if p["pid"] not in completed and p["at"] > time
            )
            continue

        chosen = min(
            ready, key=lambda p: (p["remaining"], p["at"], p["pid"])
        )

        # Run for one millisecond, then re-evaluate for possible preemption.
        start = time
        end = time + 1
        record_run(chosen, start, end, gantt)
        time = end

        if chosen["remaining"] == 0:
            completed.add(chosen["pid"])

    finish_results(processes)
    return processes, gantt


def display(title, processes, gantt):
    """Print the Gantt chart, process metrics, and average metrics."""
    print("\n" + "=" * 76)
    print(title)
    print("=" * 76)

    print("\nGANTT CHART")
    print(" | ".join(
        f"{pid} [{start}-{end}]" for start, end, pid in gantt
    ))

    print("\nPROCESS METRICS")
    print(
        f"{'PID':<6}{'AT':>6}{'BT':>6}{'PR':>6}"
        f"{'CT':>7}{'TAT':>7}{'WT':>7}{'RT':>7}"
    )

    for p in sorted(processes, key=lambda item: item["pid"]):
        print(
            f"{p['pid']:<6}{p['at']:>6}{p['bt']:>6}{p['priority']:>6}"
            f"{p['ct']:>7}{p['tat']:>7}{p['wt']:>7}{p['rt']:>7}"
        )

    count = len(processes)
    print(f"\nAverage Waiting Time: "
          f"{sum(p['wt'] for p in processes) / count:.2f} ms")
    print(f"Average Turnaround Time: "
          f"{sum(p['tat'] for p in processes) / count:.2f} ms")
    print(f"Average Response Time: "
          f"{sum(p['rt'] for p in processes) / count:.2f} ms")


def main():
    processes, gantt = fcfs(PROCESSES)
    display("1. FCFS", processes, gantt)

    processes, gantt = non_preemptive(PROCESSES, "sjf")
    display("2. NON-PREEMPTIVE SJF", processes, gantt)

    processes, gantt = non_preemptive(PROCESSES, "priority")
    display("3. NON-PREEMPTIVE PRIORITY", processes, gantt)

    processes, gantt = round_robin(PROCESSES, quantum=2)
    display("4. ROUND ROBIN (QUANTUM = 2)", processes, gantt)

    processes, gantt = srtf(SRTF_PROCESSES)
    display("5. SRTF (SEPARATE ARRIVAL-TIME DATASET)", processes, gantt)


if __name__ == "__main__":
    main()
