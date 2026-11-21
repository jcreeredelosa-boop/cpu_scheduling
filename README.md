# Operating Systems Lab Activity 2 — CPU Scheduling

This project implements the five scheduling algorithms required by the lab:

1. First-Come, First-Served (FCFS)
2. Non-preemptive Shortest Job First (SJF)
3. Non-preemptive Priority Scheduling
4. Round Robin (default time quantum: 2 ms)
5. Preemptive Shortest Remaining Time First (SRTF)

## Run in VS Code

1. Extract the ZIP file.
2. Open the extracted `cpu_scheduling_lab2` folder in Visual Studio Code.
3. Make sure Python 3 is installed.
4. Open **Terminal → New Terminal**.
5. Run:

   ```bash
   python cpu_scheduling.py
   ```

   On some systems, use:

   ```bash
   python3 cpu_scheduling.py
   ```

No third-party Python packages are required.

## Files

- `cpu_scheduling.py` — complete simulator.
- `README.md` — these instructions.

## Laboratory datasets

The first four algorithms use the same dataset:
- P1: AT 0, BT 8, Priority 2
- P2: AT 0, BT 4, Priority 1
- P3: AT 0, BT 2, Priority 4
- P4: AT 0, BT 6, Priority 3

SRTF uses the separate arrival-time dataset specified in the activity:
- P1: AT 0, BT 8, Priority 2
- P2: AT 1, BT 4, Priority 1
- P3: AT 2, BT 2, Priority 4
- P4: AT 3, BT 1, Priority 3

## Experiment: change the Round Robin quantum

In `cpu_scheduling.py`, find:

```python
processes, gantt = round_robin(PROCESSES, quantum=2)
```

Change `2` to `4`, save, and rerun. Then change it to `1`, save, and rerun. Record the average WT, TAT, and RT for each test.

## Important formulas

- Turnaround Time: `TAT = CT - AT`
- Waiting Time: `WT = TAT - BT`
- Response Time: `RT = First CPU Start - AT`
- Average metric: `sum of metric values / number of processes`

The program prints Gantt charts, each process's CT/TAT/WT/RT, and average metrics.
