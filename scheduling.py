from jobs import JOBS


def tie_key(job):
    """
    Required tie-breaking rule:
    1. Earlier arrival_time
    2. Lower job_id
    """
    return (job["arrival_time"], job["job_id"])


def print_results(name, results):
    print("\n" + "=" * 70)
    print(name)
    print("=" * 70)

    print(f"{'Job ID':<10}{'Arrival':<10}{'Burst':<10}"
          f"{'Start':<10}{'Completion':<12}{'Waiting':<10}{'Turnaround':<12}")

    total_waiting = 0
    total_turnaround = 0

    for job_id in sorted(results):
        r = results[job_id]

        print(f"{job_id:<10}{r['arrival_time']:<10}{r['burst_time']:<10}"
              f"{r['start_time']:<10}{r['completion_time']:<12}"
              f"{r['waiting_time']:<10}{r['turnaround_time']:<12}")

        total_waiting += r["waiting_time"]
        total_turnaround += r["turnaround_time"]

    n = len(results)

    avg_waiting = total_waiting / n
    avg_turnaround = total_turnaround / n

    print("-" * 70)
    print(f"Average Waiting Time    : {avg_waiting:.2f}")
    print(f"Average Turnaround Time : {avg_turnaround:.2f}")

    return avg_waiting, avg_turnaround


# ============================================================
# FCFS
# ============================================================

def fcfs():
    time = 0
    results = {}

    ordered_jobs = sorted(JOBS, key=tie_key)

    for job in ordered_jobs:
        if time < job["arrival_time"]:
            time = job["arrival_time"]

        start_time = time
        completion_time = start_time + job["burst_time"]

        waiting_time = start_time - job["arrival_time"]
        turnaround_time = completion_time - job["arrival_time"]

        results[job["job_id"]] = {
            "arrival_time": job["arrival_time"],
            "burst_time": job["burst_time"],
            "start_time": start_time,
            "completion_time": completion_time,
            "waiting_time": waiting_time,
            "turnaround_time": turnaround_time,
        }

        time = completion_time

    return results


# ============================================================
# Non-preemptive SJF
# ============================================================

def sjf():
    time = 0
    completed = set()
    results = {}

    while len(completed) < len(JOBS):

        ready = [
            job for job in JOBS
            if job["job_id"] not in completed
            and job["arrival_time"] <= time
        ]

        if not ready:
            time = min(
                job["arrival_time"]
                for job in JOBS
                if job["job_id"] not in completed
            )
            continue

        # SJF criterion = shortest burst time.
        # Tie: earlier arrival_time, then lower job_id.
        job = min(
            ready,
            key=lambda j: (
                j["burst_time"],
                j["arrival_time"],
                j["job_id"]
            )
        )

        start_time = time
        completion_time = start_time + job["burst_time"]

        waiting_time = start_time - job["arrival_time"]
        turnaround_time = completion_time - job["arrival_time"]

        results[job["job_id"]] = {
            "arrival_time": job["arrival_time"],
            "burst_time": job["burst_time"],
            "start_time": start_time,
            "completion_time": completion_time,
            "waiting_time": waiting_time,
            "turnaround_time": turnaround_time,
        }

        time = completion_time
        completed.add(job["job_id"])

    return results


# ============================================================
# SRTF
# ============================================================

def srtf():
    time = 0
    completed = set()
    remaining = {
        job["job_id"]: job["burst_time"]
        for job in JOBS
    }

    results = {}

    while len(completed) < len(JOBS):

        ready = [
            job for job in JOBS
            if job["job_id"] not in completed
            and job["arrival_time"] <= time
        ]

        if not ready:
            time = min(
                job["arrival_time"]
                for job in JOBS
                if job["job_id"] not in completed
            )
            continue

        # SRTF criterion = shortest remaining time.
        # Tie: earlier arrival_time, then lower job_id.
        job = min(
            ready,
            key=lambda j: (
                remaining[j["job_id"]],
                j["arrival_time"],
                j["job_id"]
            )
        )

        job_id = job["job_id"]

        if job_id not in results:
            results[job_id] = {
                "arrival_time": job["arrival_time"],
                "burst_time": job["burst_time"],
                "start_time": time,
            }

        # Run for one tick.
        remaining[job_id] -= 1
        time += 1

        if remaining[job_id] == 0:
            completion_time = time

            waiting_time = (
                completion_time
                - job["arrival_time"]
                - job["burst_time"]
            )

            turnaround_time = completion_time - job["arrival_time"]

            results[job_id]["completion_time"] = completion_time
            results[job_id]["waiting_time"] = waiting_time
            results[job_id]["turnaround_time"] = turnaround_time

            completed.add(job_id)

    return results


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":

    fcfs_results = fcfs()
    fcfs_avg = print_results("FCFS", fcfs_results)

    sjf_results = sjf()
    sjf_avg = print_results("Non-Preemptive SJF", sjf_results)

    srtf_results = srtf()
    srtf_avg = print_results("SRTF", srtf_results)

    print("\n" + "=" * 70)
    print("REQUIRED AVERAGE WAITING-TIME ORDER")
    print("=" * 70)

    print(f"FCFS : {fcfs_avg[0]:.2f}")
    print(f"SJF  : {sjf_avg[0]:.2f}")
    print(f"SRTF : {srtf_avg[0]:.2f}")

    if srtf_avg[0] < sjf_avg[0] < fcfs_avg[0]:
        print("\nPASS: SRTF < SJF < FCFS")
    else:
        print("\nFAIL: Required ordering was not achieved.")