# ============================================================
# Task 6 — Banker's Algorithm
# Smart City Zone Controller Resource Management
# ============================================================

AVAILABLE = [3, 3, 2]

MAX_NEED = {
    "P0": [7, 5, 3],
    "P1": [3, 2, 2],
    "P2": [9, 0, 2],
    "P3": [2, 2, 2],
}

ALLOCATION = {
    "P0": [0, 1, 0],
    "P1": [2, 0, 0],
    "P2": [3, 0, 2],
    "P3": [2, 1, 1],
}


def calculate_need(max_need, allocation):
    """Calculate Need = Max Need - Allocation."""
    need = {}

    for process in max_need:
        need[process] = [
            max_need[process][i] - allocation[process][i]
            for i in range(len(max_need[process]))
        ]

    return need


def is_less_or_equal(a, b):
    """Return True if every element of a is <= corresponding b."""
    return all(x <= y for x, y in zip(a, b))


def add_resources(a, b):
    """Element-wise addition of two resource vectors."""
    return [x + y for x, y in zip(a, b)]


def safety_algorithm(available, allocation, need):
    """
    Banker's safety algorithm.

    Determines whether the current state is safe and returns
    one valid safe sequence if one exists.
    """

    work = available.copy()

    finish = {
        process: False
        for process in allocation
    }

    safe_sequence = []

    while len(safe_sequence) < len(allocation):

        found_process = False

        for process in allocation:

            if finish[process]:
                continue

            # A process can finish if its remaining Need
            # can be satisfied by currently available Work.
            if is_less_or_equal(need[process], work):

                # When the process finishes, its allocated
                # resources are released.
                work = add_resources(
                    work,
                    allocation[process]
                )

                finish[process] = True
                safe_sequence.append(process)
                found_process = True

        if not found_process:
            break

    is_safe = len(safe_sequence) == len(allocation)

    return is_safe, safe_sequence


def request_resources(
    process,
    request,
    available,
    allocation,
    need
):
    """
    Test a resource request using Banker's Algorithm.

    The function works on copies, so the original state is never
    modified. This is important because Task 6 requires the two
    requests to be evaluated independently.
    """

    # Step 1: Request must not exceed the process's remaining Need.
    if not is_less_or_equal(request, need[process]):
        return False, "Request exceeds the process's remaining Need."

    # Step 2: Request must not exceed Available resources.
    if not is_less_or_equal(request, available):
        return False, "Request exceeds currently Available resources."

    # Make hypothetical copies.
    new_available = available.copy()

    new_allocation = {
        p: allocation[p].copy()
        for p in allocation
    }

    new_need = {
        p: need[p].copy()
        for p in need
    }

    # Hypothetically grant the request.
    new_available = [
        new_available[i] - request[i]
        for i in range(len(request))
    ]

    new_allocation[process] = [
        new_allocation[process][i] + request[i]
        for i in range(len(request))
    ]

    new_need[process] = [
        new_need[process][i] - request[i]
        for i in range(len(request))
    ]

    # Step 3: Check whether the resulting state is safe.
    safe, sequence = safety_algorithm(
        new_available,
        new_allocation,
        new_need
    )

    if safe:
        return True, sequence

    return False, "granting the request would leave the system in an unsafe state."


def print_need_matrix(need):
    print("\n" + "=" * 70)
    print("NEED MATRIX")
    print("=" * 70)

    print(f"{'Process':<12}{'R0':<8}{'R1':<8}{'R2':<8}")

    for process in need:
        print(
            f"{process:<12}"
            f"{need[process][0]:<8}"
            f"{need[process][1]:<8}"
            f"{need[process][2]:<8}"
        )


def print_state():
    print("\n" + "=" * 70)
    print("BANKER'S ALGORITHM — SMART CITY RESOURCE STATE")
    print("=" * 70)

    print("\nResources:")
    print("R0 = Compute slots")
    print("R1 = Network channels")
    print("R2 = Storage buffers")

    print("\nAvailable:")
    print(AVAILABLE)

    print("\nMaximum Need:")
    for process, values in MAX_NEED.items():
        print(f"{process}: {values}")

    print("\nAllocation:")
    for process, values in ALLOCATION.items():
        print(f"{process}: {values}")


if __name__ == "__main__":

    # --------------------------------------------------------
    # Calculate Need Matrix
    # --------------------------------------------------------

    NEED = calculate_need(
        MAX_NEED,
        ALLOCATION
    )

    print_state()
    print_need_matrix(NEED)

    # --------------------------------------------------------
    # Initial Safety Check
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("INITIAL SAFETY CHECK")
    print("=" * 70)

    safe, safe_sequence = safety_algorithm(
        AVAILABLE,
        ALLOCATION,
        NEED
    )

    if safe:
        print("Initial state: SAFE")
        print(
            "One valid safe sequence:",
            " -> ".join(safe_sequence)
        )
    else:
        print("Initial state: UNSAFE")
        print("No valid safe sequence exists.")

    # --------------------------------------------------------
    # Request A — P1 [1, 0, 2]
    # IMPORTANT: Uses ORIGINAL state.
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("REQUEST A — P1 requests [1, 0, 2]")
    print("=" * 70)

    request_p1 = [1, 0, 2]

    granted, result = request_resources(
        "P1",
        request_p1,
        AVAILABLE,
        ALLOCATION,
        NEED
    )

    if granted:
        print("P1 request [1, 0, 2]: GRANTED")
        print(
            "Resulting state is SAFE."
        )
        print(
            "Safe sequence after hypothetical grant:",
            " -> ".join(result)
        )
    else:
        print("P1 request [1, 0, 2]: DENIED")
        print("Reason:", result)

    # --------------------------------------------------------
    # Request B — P0 [2, 0, 2]
    # IMPORTANT: Again uses ORIGINAL state.
    # It must NOT use P1's hypothetical allocation.
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("REQUEST B — P0 requests [2, 0, 2]")
    print("=" * 70)

    request_p0 = [2, 0, 2]

    granted, result = request_resources(
        "P0",
        request_p0,
        AVAILABLE,
        ALLOCATION,
        NEED
    )

    if granted:
        print("P0 request [2, 0, 2]: GRANTED")
        print(
            "Resulting state is SAFE."
        )
        print(
            "Safe sequence after hypothetical grant:",
            " -> ".join(result)
        )
    else:
        print("P0 request [2, 0, 2]: DENIED")
        print(
            "Reason:",
            result
        )

    # --------------------------------------------------------
    # Final Acceptance Check
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("TASK 6 ACCEPTANCE CHECK")
    print("=" * 70)

    p1_granted, _ = request_resources(
        "P1",
        [1, 0, 2],
        AVAILABLE,
        ALLOCATION,
        NEED
    )

    p0_granted, p0_reason = request_resources(
        "P0",
        [2, 0, 2],
        AVAILABLE,
        ALLOCATION,
        NEED
    )

    if (
        safe
        and p1_granted
        and not p0_granted
        and "unsafe" in str(p0_reason).lower()
    ):
        print(
            "PASS: Banker's Algorithm acceptance criteria satisfied."
        )
    else:
        print(
            "FAIL: Banker's Algorithm acceptance criteria not satisfied."
        )