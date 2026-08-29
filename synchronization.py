import threading
import time


# ============================================================
# Configuration
# ============================================================

INITIAL_CREDIT = 100
SUBTRACT_AMOUNT = 40
ADD_AMOUNT = 25
TEST_RUNS = 5


# ============================================================
# Part 1: Unsynchronized Race Condition
# ============================================================

def run_race_condition():
    """
    Demonstrates a race condition.

    Both threads perform:
        1. Read shared counter
        2. Sleep briefly
        3. Modify local value
        4. Write shared counter

    Because there is no synchronization, one update can overwrite
    the other update.
    """

    counter = {"value": INITIAL_CREDIT}

    def subtract_credits():
        old_value = counter["value"]
        time.sleep(0.01)
        counter["value"] = old_value - SUBTRACT_AMOUNT

    def add_credits():
        old_value = counter["value"]
        time.sleep(0.01)
        counter["value"] = old_value + ADD_AMOUNT

    thread1 = threading.Thread(target=subtract_credits)
    thread2 = threading.Thread(target=add_credits)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    return counter["value"]


# ============================================================
# Part 2: Peterson's Algorithm
# ============================================================

class PetersonLock:
    """
    Two-thread Peterson's Algorithm.

    flag[i] indicates that thread i wants to enter the
    critical section.

    turn indicates which thread should get priority if both
    threads want to enter at the same time.
    """

    def __init__(self):
        self.flag = [False, False]
        self.turn = 0

    def acquire(self, thread_id):
        other = 1 - thread_id

        self.flag[thread_id] = True
        self.turn = other

        while self.flag[other] and self.turn == other:
            time.sleep(0)

    def release(self, thread_id):
        self.flag[thread_id] = False


def run_peterson():
    """
    Runs the same read-modify-write operations, but protects
    the critical section with Peterson's Algorithm.
    """

    counter = {"value": INITIAL_CREDIT}

    lock = PetersonLock()

    def worker(thread_id, operation):

        lock.acquire(thread_id)

        try:
            # Critical section:
            # read -> delay -> modify -> write
            old_value = counter["value"]

            # Keep the delay inside the critical section so that
            # Peterson's Algorithm protects the complete operation.
            time.sleep(0.01)

            if operation == "subtract":
                counter["value"] = old_value - SUBTRACT_AMOUNT
            else:
                counter["value"] = old_value + ADD_AMOUNT

        finally:
            lock.release(thread_id)

    thread1 = threading.Thread(
        target=worker,
        args=(0, "subtract")
    )

    thread2 = threading.Thread(
        target=worker,
        args=(1, "add")
    )

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    return counter["value"]


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("TASK 5 — RACE CONDITION AND PETERSON'S ALGORITHM")
    print("=" * 70)

    print("\nInitial Zone-B compute-credit counter:", INITIAL_CREDIT)
    print("Completed job consumes:", SUBTRACT_AMOUNT)
    print("SLA-breach reimbursement adds:", ADD_AMOUNT)
    print("Correct arithmetic result: 85")

    # --------------------------------------------------------
    # Unsynchronized runs
    # --------------------------------------------------------

    print("\n" + "-" * 70)
    print("UNSYNCHRONIZED RACE CONDITION")
    print("-" * 70)

    race_results = []

    for run in range(1, TEST_RUNS + 1):
        result = run_race_condition()
        race_results.append(result)

        print(f"Run {run}: final counter = {result}")

    incorrect_runs = [
        result for result in race_results
        if result != 85
    ]

    print(
        f"\nIncorrect unsynchronized runs: "
        f"{len(incorrect_runs)}/{TEST_RUNS}"
    )

    if incorrect_runs:
        print(
            "PASS: Race condition is observable because at least "
            "one run differs from the correct value of 85."
        )
    else:
        print(
            "FAIL: All unsynchronized runs produced 85. "
            "Race condition was not observed."
        )

    # --------------------------------------------------------
    # Peterson runs
    # --------------------------------------------------------

    print("\n" + "-" * 70)
    print("PETERSON'S ALGORITHM")
    print("-" * 70)

    peterson_results = []

    for run in range(1, TEST_RUNS + 1):
        result = run_peterson()
        peterson_results.append(result)

        print(f"Run {run}: final counter = {result}")

    if all(result == 85 for result in peterson_results):
        print(
            "\nPASS: Peterson's Algorithm produced exactly 85 "
            "on all 5 runs."
        )
    else:
        print(
            "\nFAIL: Peterson's Algorithm did not produce 85 "
            "on every run."
        )

    # --------------------------------------------------------
    # Final acceptance check
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("TASK 5 ACCEPTANCE CHECK")
    print("=" * 70)

    if (
        any(result != 85 for result in race_results)
        and all(result == 85 for result in peterson_results)
    ):
        print("PASS: Race condition demonstrated and fixed with Peterson's Algorithm.")
    else:
        print("FAIL: Task 5 acceptance criteria not satisfied.")