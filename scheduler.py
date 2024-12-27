import sys
import queue

class Process:
    def __init__(self, name, arrival_time, priority, total_time, block_interval):
        self.name = name
        self.arrival_time = arrival_time
        self.priority = priority
        self.time_left = total_time
        self.time_to_next_block = block_interval
        self.block_interval = block_interval
        self.unblock_time = None
        self.time_last_run = -1

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.time_last_run < other.time_last_run


def read_input_file(filename):
    processes = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('#') or not line:
                continue  # Skip comments and blank lines
            name, priority, arrival_time, total_time, block_interval = line.split()
            processes.append(
                Process(
                    name=name,
                    arrival_time=int(arrival_time),
                    priority=int(priority),
                    total_time=int(total_time),
                    block_interval=int(block_interval),
                )
            )
    return processes


def scheduler(processes, time_slice, block_duration):
    # Initialize the queues
    arrival_queue = queue.PriorityQueue()
    ready_queue = queue.PriorityQueue()
    blocked_queue = queue.PriorityQueue()

    # Populate the arrival queue
    for process in processes:
        arrival_queue.put((process.arrival_time, process))

    current_time = 0
    total_turnaround_time = 0
    total_processes = len(processes)

    output = []

    while not arrival_queue.empty() or not ready_queue.empty() or not blocked_queue.empty():
        # Check for newly arrived processes
        while not arrival_queue.empty() and arrival_queue.queue[0][0] <= current_time:
            _, process = arrival_queue.get()
            ready_queue.put((-process.priority, process))  # Add to ready queue with priority

        # Check for unblocked processes
        while not blocked_queue.empty() and blocked_queue.queue[0][0] <= current_time:
            _, process = blocked_queue.get()
            ready_queue.put((-process.priority, process))  # Add back to ready queue

        start_time = current_time

        if ready_queue.empty():
            # No processes are ready; advance to the next event
            next_event_time = float('inf')
            if not arrival_queue.empty():
                next_event_time = min(next_event_time, arrival_queue.queue[0][0])
            if not blocked_queue.empty():
                next_event_time = min(next_event_time, blocked_queue.queue[0][0])

            idle_time = next_event_time - current_time
            current_time = next_event_time
            output.append(f"{start_time}\t(IDLE)\t{idle_time}\tI")
        else:
            # Select the next process to run
            _, current_process = ready_queue.get()
            current_process.time_last_run = current_time

            # Determine process's next state
            if current_process.time_left <= time_slice:
                # Process finishes execution
                duration = current_process.time_left
                current_time += duration
                total_turnaround_time += current_time - current_process.arrival_time
                output.append(f"{start_time}\t{current_process.name}\t{duration}\tT")
            elif current_process.time_to_next_block <= time_slice:
                # Process will block for I/O
                duration = current_process.time_to_next_block
                current_time += duration
                current_process.time_left -= duration
                current_process.time_to_next_block = current_process.block_interval
                current_process.unblock_time = current_time + block_duration
                blocked_queue.put((current_process.unblock_time, current_process))
                output.append(f"{start_time}\t{current_process.name}\t{duration}\tB")
            else:
                # Process is preempted after the time slice
                duration = time_slice
                current_time += duration
                current_process.time_left -= duration
                current_process.time_to_next_block -= duration
                ready_queue.put((-current_process.priority, current_process))
                output.append(f"{start_time}\t{current_process.name}\t{duration}\tP")

    # Calculate and output the average turnaround time
    average_turnaround_time = total_turnaround_time / total_processes
    output.append(f"Average turnaround time: {average_turnaround_time:.2f}")

    # Print the scheduling decisions
    for line in output:
        print(line)


# Example Usage
def main():
    if len(sys.argv) != 4:
        print("Usage: python3 scheduler.py <input_file> <time_slice> <block_duration>")
        return

    input_file = sys.argv[1]
    time_slice = int(sys.argv[2])
    block_duration = int(sys.argv[3])

    processes = read_input_file(input_file)
    scheduler(processes, time_slice, block_duration)


if __name__ == "__main__":
    main()
