def prepare_processes(processes):
    if not processes:
        raise ValueError("Please add at least one process.")

    prepared = []

    for index, process in enumerate(processes):
        prepared.append({
            "pid": str(process["pid"]),
            "arrival": int(process["arrival"]),
            "burst": int(process["burst"]),
            "priority": int(process["priority"]),
            "remaining": int(process["burst"]),
            "index": index
        })

    return prepared


def merge_segments(segments):
    merged = []

    for segment in segments:
        if (
            merged
            and merged[-1]["pid"] == segment["pid"]
            and merged[-1]["end"] == segment["start"]
        ):
            merged[-1]["end"] = segment["end"]
        else:
            merged.append(segment.copy())

    return merged


def calculate_metrics(processes, completion, first_start):
    metrics = []

    for process in processes:
        pid = process["pid"]
        arrival = process["arrival"]
        burst = process["burst"]

        ct = completion[pid]
        tat = ct - arrival
        wt = tat - burst
        rt = first_start[pid] - arrival

        metrics.append({
            "pid": pid,
            "arrival": arrival,
            "burst": burst,
            "priority": process["priority"],
            "completion": ct,
            "turnaround": tat,
            "waiting": wt,
            "response": rt
        })

    count = len(metrics)

    return {
        "metrics": metrics,
        "avg_waiting": sum(p["waiting"] for p in metrics) / count,
        "avg_turnaround": sum(p["turnaround"] for p in metrics) / count,
        "avg_response": sum(p["response"] for p in metrics) / count
    }


def non_preemptive(processes, mode):
    pending = prepare_processes(processes)

    time = min(p["arrival"] for p in pending)
    segments = []
    completion = {}
    first_start = {}

    while pending:
        ready = [
            p for p in pending
            if p["arrival"] <= time
        ]

        if not ready:
            next_time = min(p["arrival"] for p in pending)
            segments.append({
                "pid": "IDLE",
                "start": time,
                "end": next_time
            })
            time = next_time
            continue

        if mode == "FCFS":
            selected = min(
                ready,
                key=lambda p: (p["arrival"], p["index"])
            )

        elif mode == "SJF":
            selected = min(
                ready,
                key=lambda p: (
                    p["burst"],
                    p["arrival"],
                    p["index"]
                )
            )

        elif mode == "PRIORITY":
            selected = min(
                ready,
                key=lambda p: (
                    p["priority"],
                    p["arrival"],
                    p["index"]
                )
            )

        start = time
        end = start + selected["burst"]

        first_start[selected["pid"]] = start
        completion[selected["pid"]] = end

        segments.append({
            "pid": selected["pid"],
            "start": start,
            "end": end
        })

        time = end
        pending.remove(selected)

    result = calculate_metrics(
        prepare_processes(processes),
        completion,
        first_start
    )

    result["segments"] = merge_segments(segments)

    return result


def preemptive(processes, mode):
    pending = prepare_processes(processes)

    time = min(p["arrival"] for p in pending)
    total = len(pending)

    completion = {}
    first_start = {}
    segments = []

    while len(completion) < total:
        ready = [
            p for p in pending
            if p["arrival"] <= time
            and p["remaining"] > 0
        ]

        if not ready:
            segments.append({
                "pid": "IDLE",
                "start": time,
                "end": time + 1
            })
            time += 1
            continue

        if mode == "SJF":
            selected = min(
                ready,
                key=lambda p: (
                    p["remaining"],
                    p["arrival"],
                    p["index"]
                )
            )

        else:
            selected = min(
                ready,
                key=lambda p: (
                    p["priority"],
                    p["arrival"],
                    p["index"]
                )
            )

        pid = selected["pid"]

        if pid not in first_start:
            first_start[pid] = time

        segments.append({
            "pid": pid,
            "start": time,
            "end": time + 1
        })

        selected["remaining"] -= 1
        time += 1

        if selected["remaining"] == 0:
            completion[pid] = time

    result = calculate_metrics(
        pending,
        completion,
        first_start
    )

    result["segments"] = merge_segments(segments)

    return result


def round_robin(processes, quantum):
    pending = prepare_processes(processes)

    if quantum <= 0:
        raise ValueError("Time quantum must be positive.")

    pending.sort(
        key=lambda p: (p["arrival"], p["index"])
    )

    time = pending[0]["arrival"]
    queue = []
    next_process = 0

    completion = {}
    first_start = {}
    segments = []

    while len(completion) < len(pending):

        while (
            next_process < len(pending)
            and pending[next_process]["arrival"] <= time
        ):
            queue.append(pending[next_process])
            next_process += 1

        if not queue:
            next_time = pending[next_process]["arrival"]

            segments.append({
                "pid": "IDLE",
                "start": time,
                "end": next_time
            })

            time = next_time
            continue

        selected = queue.pop(0)
        pid = selected["pid"]

        if pid not in first_start:
            first_start[pid] = time

        start = time
        execution = min(quantum, selected["remaining"])

        time += execution
        selected["remaining"] -= execution

        segments.append({
            "pid": pid,
            "start": start,
            "end": time
        })

        while (
            next_process < len(pending)
            and pending[next_process]["arrival"] <= time
        ):
            queue.append(pending[next_process])
            next_process += 1

        if selected["remaining"] > 0:
            queue.append(selected)
        else:
            completion[pid] = time

    result = calculate_metrics(
        pending,
        completion,
        first_start
    )

    result["segments"] = merge_segments(segments)

    return result


def run_algorithm(processes, algorithm, quantum=2):

    if algorithm == "FCFS":
        return non_preemptive(processes, "FCFS")

    elif algorithm == "SJF (Non-preemptive)":
        return non_preemptive(processes, "SJF")

    elif algorithm == "SJF (Preemptive)":
        return preemptive(processes, "SJF")

    elif algorithm == "Priority (Non-preemptive)":
        return non_preemptive(processes, "PRIORITY")

    elif algorithm == "Priority (Preemptive)":
        return preemptive(processes, "PRIORITY")

    elif algorithm == "Round Robin":
        return round_robin(processes, quantum)

    else:
        raise ValueError("Unknown scheduling algorithm.")