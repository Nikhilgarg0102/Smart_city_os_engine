from jobs import JOBS


def priority_scheduling(aging=False):
    """
    Non-preemptive Priority Scheduling.

    Lower priority number = higher priority.

    Without aging:
        effective_priority = fixed priority

    With aging:
        effective_priority =
            max(1, priority - (ticks_waited // 3))

    Tie-breaking:
        1. Lower effective priority
        2. Earlier arrival_time
        3. Lower job_id
    """

    time = 0
    completed = set()
    results = {}

    while len(completed) < len(JOBS):

        ready = [
            job for job in JOBS
            if job["job_id"] not in completed
            and job["arrival_time"] <= time
        ]

        # If CPU is idle, move to the next arrival.
        if not ready:
            time = min(
                job["arrival_time"]
                for job in JOBS
                if job["job_id"] not in completed
            )
            continue

        candidates = []

        for job in ready:

            ticks_waited = time - job["arrival_time"]

            if aging:
                effective_priority = max(
                    1,
                    job["priority"] - (ticks_waited // 3)
                )
            else:
                effective_priority = job["priority"]

            candidates.append(
                (
                    effective_priority,
                    job["arrival_time"],
                    job["job_id"],
                    job
                )
            )

        # Required dispatch tie-breaking.
        candidates.sort(
            key=lambda x: (x[0], x[1], x[2])
        )

        effective_priority, _, _, job = candidates[0]

        start_time = time
        completion_time = start_time + job["burst_time"]

        waiting_time = start_time - job["arrival_time"]
        turnaround_time = completion_time - job["arrival_time"]

        results[job["job_id"]] = {
            "arrival_time": job["arrival_time"],
            "burst_time": job["burst_time"],
            "fixed_priority": job["priority"],
            "effective_priority": effective_priority,
            "start_time": start_time,
            "completion_time": completion_time,
            "waiting_time": waiting_time,
            "turnaround_time": turnaround_time
        }

        time = completion_time
        completed.add(job["job_id"])

    return results


def print_results(title, results):

    print("\n" + "=" * 90)
    print(title)
    print("=" * 90)

    print(
        f"{'Job ID':<10}"
        f"{'Arrival':<10}"
        f"{'Burst':<8}"
        f"{'Priority':<10}"
        f"{'Effective':<12}"
        f"{'Start':<8}"
        f"{'Complete':<10}"
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
            f"{r['burst_time']:<8}"
            f"{r['fixed_priority']:<10}"
            f"{r['effective_priority']:<12}"
            f"{r['start_time']:<8}"
            f"{r['completion_time']:<10}"
            f"{r['waiting_time']:<10}"
            f"{r['turnaround_time']:<12}"
        )

        total_waiting += r["waiting_time"]
        total_turnaround += r["turnaround_time"]

    n = len(JOBS)

    average_waiting = total_waiting / n
    average_turnaround = total_turnaround / n

    print("-" * 90)
    print(f"Average Waiting Time    : {average_waiting:.2f}")
    print(f"Average Turnaround Time : {average_turnaround:.2f}")

    longest_job = max(
        results,
        key=lambda job_id: (
            results[job_id]["waiting_time"],
            job_id
        )
    )

    longest_wait = results[longest_job]["waiting_time"]

    print(
        f"Longest Waiting Job     : {longest_job} "
        f"({longest_wait} ticks)"
    )

    return average_waiting, average_turnaround, longest_job


if __name__ == "__main__":

    # ---------------------------------------------------------
    # No Aging
    # ---------------------------------------------------------

    no_aging_results = priority_scheduling(aging=False)

    no_aging_summary = print_results(
        "NON-PREEMPTIVE PRIORITY — WITHOUT AGING",
        no_aging_results
    )

    # ---------------------------------------------------------
    # With Aging
    # ---------------------------------------------------------

    aging_results = priority_scheduling(aging=True)

    aging_summary = print_results(
        "NON-PREEMPTIVE PRIORITY — WITH AGING",
        aging_results
    )

    # ---------------------------------------------------------
    # Acceptance checks
    # ---------------------------------------------------------

    print("\n" + "=" * 90)
    print("PRIORITY + AGING ACCEPTANCE CHECK")
    print("=" * 90)

    no_aging_longest = no_aging_summary[2]
    aging_longest = aging_summary[2]

    z3j02_no_aging_wait = no_aging_results["Z3-J02"]["waiting_time"]
    z3j02_aging_wait = aging_results["Z3-J02"]["waiting_time"]

    print(
        f"No-aging longest-wait job : "
        f"{no_aging_longest}"
    )

    print(
        f"Aging longest-wait job    : "
        f"{aging_longest}"
    )

    print(
        f"Z3-J02 wait without aging : "
        f"{z3j02_no_aging_wait}"
    )

    print(
        f"Z3-J02 wait with aging    : "
        f"{z3j02_aging_wait}"
    )

    if (
        no_aging_longest == "Z3-J02"
        and aging_longest != "Z3-J02"
        and z3j02_aging_wait < z3j02_no_aging_wait
    ):
        print("\nPASS: Priority aging acceptance criteria satisfied.")
    else:
        print("\nFAIL: Priority aging acceptance criteria not satisfied.")