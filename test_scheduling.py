
from scheduling import run_algorithm

processes = [
    {"pid": "P1", "arrival": 0, "burst": 5, "priority": 2},
    {"pid": "P2", "arrival": 1, "burst": 3, "priority": 1},
    {"pid": "P3", "arrival": 2, "burst": 8, "priority": 3},
    {"pid": "P4", "arrival": 3, "burst": 6, "priority": 2}
]

algorithms = [
    "FCFS",
    "SJF (Non-preemptive)",
    "SJF (Preemptive)",
    "Priority (Non-preemptive)",
    "Priority (Preemptive)",
    "Round Robin"
]

for algorithm in algorithms:
    result = run_algorithm(processes, algorithm, quantum=2)

    print("\n", "=" * 45)
    print(algorithm)
    print("=" * 45)

    print("Gantt Chart:")

    for segment in result["segments"]:
        print(
            segment["pid"],
            segment["start"],
            "to",
            segment["end"]
        )

    print("\nProcess Metrics:")

    for process in result["metrics"]:
        print(process)

    print("\nAverage Waiting Time:", result["avg_waiting"])
    print("Average Turnaround Time:", result["avg_turnaround"])
    print("Average Response Time:", result["avg_response"])
