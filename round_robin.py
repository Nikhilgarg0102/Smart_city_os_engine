from jobs import JOBS


def round_robin(quantum):
    """
    Round Robin scheduling.

    Boundary rule:
    If a new job arrives at exactly the tick when a quantum expires,
    the newly arrived job is added to the ready queue BEFORE the
    expired job is re-added to the back of the queue.

    Context-switch cost is zero.
    """

    jobs = sorted(JOBS, key=lambda j: (j["arrival_time"], j["job_id"]))

    remaining = {
        job["job_id"]: job["burst_time"]
        for job in jobs
    }

    first_start = {}
    completion = {}

    ready_queue = []
    arrived = set()
    completed = set()

    time = 0
    dispatches = []

    while len(completed) < len(jobs):

        # Add jobs that have arrived.
        for job in jobs:
            if (
                job["arrival_time"] <= time
                and job["job_id"] not in arrived
            ):
                ready_queue.append(job)
                arrived.add(job["job_id"])

        # If nobody is ready, jump to next arrival.
        if not ready_queue:
            next_job = min(
                (
                    job for job in jobs
                    if job["job_id"] not in arrived
                ),
                key=lambda j: (j["arrival_time"], j["job_id"])
            )

            time = next_job["arrival_time"]

            ready_queue.append(next_job)
            arrived.add(next_job["job_id"])

        current = ready_queue.pop(0)
        job_id = current["job_id"]

        # Record a dispatch slice.
        dispatches.append(job_id)

        if job_id not in first_start:
            first_start[job_id] = time

        run_time = min(quantum, remaining[job_id])

        start_time = time
        end_time = time + run_time

        remaining[job_id] -= run_time
        time = end_time

        # --------------------------------------------------------
        # Boundary convention:
        # First add NEW arrivals at this exact time.
        # Then re-add the expired job if it still has work.
        # --------------------------------------------------------

        for job in jobs:
            if (
                job["arrival_time"] <= time
                and job["job_id"] not in arrived
            ):
                ready_queue.append(job)
                arrived.add(job["job_id"])

        if remaining[job_id] == 0:
            completion[job_id] = time
            completed.add(job_id)
        else:
            ready_queue.append(current)

    # Calculate waiting and turnaround times.
    results = {}

    for job in jobs:
        job_id = job["job_id"]

        turnaround = (
            completion[job_id]
            - job["arrival_time"]
        )

        waiting = (
            turnaround
            - job["burst_time"]
        )

        results[job_id] = {
            "arrival_time": job["arrival_time"],
            "burst_time": job["burst_time"],
            "start_time": first_start[job_id],
            "completion_time": completion[job_id],
            "waiting_time": waiting,
            "turnaround_time": turnaround,
        }

    # A context switch means a DIFFERENT job starts running.
    context_switches = sum(
        1
        for i in range(1, len(dispatches))
        if dispatches[i] != dispatches[i - 1]
    )

    return results, dispatches, context_switches


def print_results(quantum, results, dispatches, context_switches):

    print("\n" + "=" * 80)
    print(f"ROUND ROBIN — QUANTUM = {quantum}")
    print("=" * 80)

    print(
        f"{'Job ID':<10}"
        f"{'Arrival':<10}"
        f"{'Burst':<10}"
        f"{'Start':<10}"
        f"{'Completion':<12}"
        f"{'Waiting':<10}"
        f"{'Turnaround':<12}"
    )

    total_waiting = 0
    total_turnaround = 0

    for job in sorted(JOBS, key=lambda j: j["job_id"]):

        job_id = job["job_id"]
        r = results[job_id]

        print(
            f"{job_id:<10}"
            f"{r['arrival_time']:<10}"
            f"{r['burst_time']:<10}"
            f"{r['start_time']:<10}"
            f"{r['completion_time']:<12}"
            f"{r['waiting_time']:<10}"
            f"{r['turnaround_time']:<12}"
        )

        total_waiting += r["waiting_time"]
        total_turnaround += r["turnaround_time"]

    n = len(JOBS)

    avg_waiting = total_waiting / n
    avg_turnaround = total_turnaround / n

    print("-" * 80)

    print(f"Average Waiting Time    : {avg_waiting:.2f}")
    print(f"Average Turnaround Time : {avg_turnaround:.2f}")

    print("\nDispatch slices:")
    print(" -> ".join(dispatches))

    print(f"\nNumber of dispatch slices : {len(dispatches)}")
    print(f"Context switches          : {context_switches}")

    return avg_waiting, avg_turnaround


if __name__ == "__main__":

    results_q3, dispatches_q3, switches_q3 = round_robin(3)

    avg_q3 = print_results(
        3,
        results_q3,
        dispatches_q3,
        switches_q3
    )

    results_q6, dispatches_q6, switches_q6 = round_robin(6)

    avg_q6 = print_results(
        6,
        results_q6,
        dispatches_q6,
        switches_q6
    )

    print("\n" + "=" * 80)
    print("ROUND ROBIN ACCEPTANCE CHECK")
    print("=" * 80)

    print(
        f"Quantum 3: {len(dispatches_q3)} dispatch slices, "
        f"{switches_q3} context switches"
    )

    print(
        f"Quantum 6: {len(dispatches_q6)} dispatch slices, "
        f"{switches_q6} context switches"
    )

    if (
        len(dispatches_q3) == 17
        and switches_q3 == 16
        and len(dispatches_q6) == 11
        and switches_q6 == 10
    ):
        print("\nPASS: Round Robin acceptance criteria satisfied.")
    else:
        print("\nFAIL: Round Robin acceptance criteria not satisfied.")

    print(
        "\nTheory statement: In a real OS, quantum 3 would cause more "
        "switching overhead than quantum 6 because it produces more "
        "context switches (16 versus 10), and real context switches "
        "consume CPU time."
    )