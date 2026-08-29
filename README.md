# Smart City OS Engine

## Project Overview

The Smart City OS Engine is an Operating Systems simulation for managing
sensor-processing jobs across three smart-city zones: Zone-A, Zone-B,
and Zone-C.

The project implements CPU scheduling, synchronization, deadlock
avoidance, and memory-management concepts and then provides a cloud,
security, and IoT deployment blueprint for the same compute core.

---

# Part 1 — OS Compute Core

## Fixed Job List

The project uses exactly eight fixed sensor-processing jobs.

The job list is stored in `jobs.py` and is imported by the scheduling
implementations. The job list must not be changed because all scheduling
acceptance criteria depend on this exact input.

## Scheduling Algorithms

The following scheduling algorithms are implemented:

- First-Come, First-Served (FCFS)
- Non-preemptive Shortest Job First (SJF)
- Shortest Remaining Time First (SRTF)
- Round Robin with quantum 3
- Round Robin with quantum 6
- Non-preemptive Priority Scheduling
- Non-preemptive Priority Scheduling with Aging

### Measured Scheduling Results

| Algorithm | Average Waiting Time |
|---|---:|
| FCFS | 17.12 |
| SJF | 13.00 |
| SRTF | 11.50 |
| Priority without aging | 14.12 |
| Priority with aging | 17.12 |

For this fixed workload, SRTF produced the lowest measured average
waiting time at 11.50 ticks.

### Round Robin Results

| Quantum | Dispatch Slices | Context Switches |
|---:|---:|---:|
| 3 | 17 | 16 |
| 6 | 11 | 10 |

A real operating system would experience more switching overhead with
quantum 3 than quantum 6 because the quantum-3 simulation produced
16 context switches compared with 10 for quantum 6.

### Priority Aging Results

Without aging, `Z3-J02` had the longest waiting time at 33 ticks.

With aging, the longest-waiting job became `Z2-J03` at 29 ticks, while
`Z3-J02`'s waiting time decreased from 33 ticks to 23 ticks.

---

# Production Scheduling Decision

## Selected Family: SJF/SRTF

For this fixed sensor-processing workload, the **SJF/SRTF family** is
the single scheduling family I would choose for production.

SRTF produced the lowest measured average waiting time, **11.50 ticks**,
compared with **13.00 ticks for SJF** and **17.12 ticks for FCFS**.
Therefore, SRTF provided the best waiting-time performance among the
tested scheduling algorithms for this exact workload.

### Why the Other Three Families Are Less Suitable

#### 1. FCFS

FCFS is less suitable because it produced the highest measured average
waiting time among FCFS, SJF, and SRTF: **17.12 ticks**, compared with
SRTF's **11.50 ticks**. This indicates poorer responsiveness for the
fixed sensor-processing workload.

#### 2. Round Robin

Round Robin is less suitable because the quantum-3 configuration
generated **16 context switches across 17 dispatch slices**, while the
quantum-6 configuration still generated **10 context switches across
11 dispatch slices**. These frequent job changes would create greater
real CPU switching overhead than a scheduling approach that achieves
the workload's lower measured waiting time with less dependence on
time-slicing.

#### 3. Priority Scheduling

Priority scheduling is less suitable because the no-aging version
produced **14.12 ticks average waiting time**, which is higher than
SRTF's **11.50 ticks**. Furthermore, the no-aging run produced a
**33-tick wait for Z3-J02**, showing that fixed priorities can create
substantial waiting for lower-priority jobs.

---

# Synchronization

The project demonstrates a race condition using a shared Zone-B
compute-credit counter.

The counter starts at 100.

One thread subtracts 40 credits and another adds 25 credits. The
correct result is:

`100 - 40 + 25 = 85`

The unsynchronized implementation intentionally creates a read-modify-
write race condition.

Peterson's Algorithm is then used to protect the critical section.
The synchronized implementation produces exactly 85 across the
required test runs.

---

# Deadlock Avoidance

Banker's Algorithm is implemented using the required four-process,
three-resource scenario.

Resources:

- R0 — Compute slots
- R1 — Network channels
- R2 — Storage buffers

The implementation:

1. Calculates the Need matrix.
2. Checks the initial system state for safety.
3. Tests P1's request `[1, 0, 2]`.
4. Tests P0's request `[2, 0, 2]`.
5. Evaluates both requests independently against the original state.

The initial state is safe.

P1's request `[1, 0, 2]` is granted because the resulting state
remains safe.

P0's request `[2, 0, 2]` is denied because granting it would leave
the system in an unsafe state.

---

# Memory Management

The project implements both paging and segmentation address
translation.

## Paging

Page size:

`1024 bytes`

The page table is:

```text
Page 0 -> Frame 5
Page 1 -> Frame 2
Page 2 -> Frame 9
Page 3 -> Frame 1