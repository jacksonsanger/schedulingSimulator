# Round-Robin Scheduler with Priorities

This project implements a priority-based Round-Robin CPU scheduling algorithm, simulating the execution of processes based on priority levels, time slices, and blocking intervals. The program efficiently handles process queues, manages CPU allocation, and provides detailed output for simulation analysis.

## Features

- **Priority-Based Round-Robin Scheduling**: Combines priority and round-robin scheduling to allocate CPU time fairly.
- **Process Management**: Simulates processes with arrival times, total execution times, and blocking intervals.
- **Queue Handling**: Uses `PriorityQueue` for ArrivalQueue, BlockedQueue, and ReadyQueue for efficient scheduling.
- **Preemptive Execution**: Ensures lower-priority processes yield to higher-priority ones while maintaining fairness for processes with equal priority.
- **Detailed Output**:
  - Logs each interval of execution or idle time.
  - Reports the average turnaround time for all processes.

## Input Format

The program accepts the following command-line arguments:

1. **Input File Name**: Specifies the list of processes to schedule.
2. **Time Slice**: Maximum CPU time allocated to a process before preemption.
3. **Block Duration**: Time a process remains unavailable after blocking for I/O.

## Output Format

- Displays the specified time slice and block duration.
- Logs execution intervals with:
  - Simulation time
  - Process name (or "(IDLE)")
  - Interval length
  - Status code:
    - `B`: Blocked
    - `P`: Preempted
    - `T`: Terminated
    - `I`: Idle
- Calculates and displays the average turnaround time of all processes.

## Implementation Details

- **Process Class**:
  - Encapsulates process attributes like priority, arrival time, total execution time, and block interval.
  - Maintains runtime details such as remaining CPU time and blocking status.
- **Queues**:
  - **ArrivalQueue**: Tracks processes waiting to enter the ReadyQueue.
  - **BlockedQueue**: Manages processes that are unavailable due to I/O blocking.
  - **ReadyQueue**: Prioritizes processes based on priority and round-robin order.
- **Scheduler**:
  - Updates simulation time dynamically.
  - Moves processes between queues based on state transitions (e.g., blocked, ready).
  - Executes the highest-priority process or enters an idle state if no process is available.
  - Ensures round-robin scheduling for processes with equal priority.

## Example Execution

- Processes are prioritized based on priority levels, with round-robin fairness among processes of equal priority.
- Idle periods are accurately accounted for in the simulation.
- The final output includes the average turnaround time for analysis.