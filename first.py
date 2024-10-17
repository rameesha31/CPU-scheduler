import csv
import matplotlib.pyplot as plt
import pandas as pd

class Process:
    def __init__(self, pid, arrival_time, burst_time, priority):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.remaining_time = burst_time
        self.start_time = None
        self.end_time = None
        self.waiting_time = 0
        self.turnaround_time = 0
        self.CPU_time=self.burst_time-self.arrival_time

    def __repr__(self):
        return f"Process(pid={self.pid}, arrival={self.arrival_time}, burst={self.burst_time}, priority={self.priority})"

def read_processes_from_dataframe(df):
    processes = []
    for index, row in df.iterrows():
        process = Process(
            pid=int(row['pid']),
            arrival_time=int(row['arrival_time']),
            burst_time=int(row['burst_time']),
            priority=int(row['priority'])
        )
        processes.append(process)
    print(f"Successfully read {len(processes)} processes from dataframe.")
    return processes

def fcfs_scheduling(processes):
    processes.sort(key=lambda x: x.arrival_time)
    current_time = 0
    scheduled_processes = []
    for process in processes:
        if current_time < process.arrival_time:
            current_time = process.arrival_time
        process.start_time = current_time
        process.end_time = current_time + process.burst_time
        process.turnaround_time = process.end_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time
        current_time += process.burst_time
        scheduled_processes.append(process)
    return scheduled_processes

def sjf_scheduling(processes):
    
    processes.sort(key=lambda x: x.burst_time)
    current_time = 0
    scheduled_processes = []
    while processes:
        available_processes = [p for p in processes if p.arrival_time <= current_time]
        if not available_processes:
            current_time = processes[0].arrival_time
            continue
        next_process = min(available_processes, key=lambda x: x.burst_time)
        processes.remove(next_process)
        if current_time < next_process.arrival_time:
            current_time = next_process.arrival_time
        next_process.start_time = current_time
        next_process.end_time = current_time + next_process.burst_time
        next_process.turnaround_time = next_process.end_time - next_process.arrival_time
        next_process.waiting_time = next_process.turnaround_time - next_process.burst_time
        current_time += next_process.burst_time
        scheduled_processes.append(next_process)
    return scheduled_processes

def round_robin_scheduling(processes):
    current_time = 0
    ready_queue = []
    scheduled_processes = []
    process_queue = processes.copy()

    # Calculate the average burst time
    average_burst_time = sum(p.burst_time for p in processes) / len(processes)
    time_quantum = round(average_burst_time)

    # Sort processes by arrival time
    processes.sort(key=lambda x: x.arrival_time)
    remaining_processes = processes.copy()

    while remaining_processes or ready_queue:
        # Add processes to the ready queue whose arrival time is less than or equal to the current time
        while remaining_processes and remaining_processes[0].arrival_time <= current_time:
            ready_queue.append(remaining_processes.pop(0))

        if ready_queue:
            process = ready_queue.pop(0)

            if process.start_time is None:
                process.start_time = current_time

            if process.remaining_time > time_quantum:
                current_time += time_quantum
                process.remaining_time -= time_quantum
                # Add process back to the ready queue
                while remaining_processes and remaining_processes[0].arrival_time <= current_time:
                    ready_queue.append(remaining_processes.pop(0))
                ready_queue.append(process)
            else:
                current_time += process.remaining_time
                process.end_time = current_time
                process.turnaround_time = process.end_time - process.arrival_time
                process.waiting_time = process.turnaround_time - process.burst_time
                process.remaining_time = 0
                scheduled_processes.append(process)
        else:
            current_time += 1

    return scheduled_processes

def priority_scheduling_preemptive(processes):
    current_time = 0
    ready_queue = []
    scheduled_processes = []
    processes.sort(key=lambda x: x.arrival_time)
    remaining_processes = processes.copy()

    while remaining_processes or ready_queue:
        # Add processes to the ready queue whose arrival time is less than or equal to the current time
        while remaining_processes and remaining_processes[0].arrival_time <= current_time:
            ready_queue.append(remaining_processes.pop(0))

        # If ready_queue is not empty, get the highest priority process
        if ready_queue:
            # Sort ready_queue based on priority (higher priority first)
            ready_queue.sort(key=lambda x: x.priority)
            process = ready_queue.pop(0)

            # If the process is running for the first time, set the start time
            if process.start_time is None:
                process.start_time = current_time

            # Process runs for one time unit
            process.remaining_time -= 1
            current_time += 1

            # If the process is completed
            if process.remaining_time == 0:
                process.end_time = current_time
                process.turnaround_time = process.end_time - process.arrival_time
                process.waiting_time = process.turnaround_time - process.burst_time
                scheduled_processes.append(process)
            else:
                # Put the process back into the ready queue if it is not finished
                ready_queue.append(process)
        else:
            current_time += 1

    return scheduled_processes

# Define the multilevel queue scheduling function
def multilevel_queue_scheduling(processes):
    # Create queues for each priority level
    queue1 = [p for p in processes if p.priority == 1]
    queue2 = [p for p in processes if p.priority == 2]
    queue3 = [p for p in processes if p.priority == 3]
    queue4 = [p for p in processes if p.priority == 4]
    queue5 = [p for p in processes if p.priority == 5]

    def execute_queue(queue, current_time):
        for process in queue:
            if current_time < process.arrival_time:
                current_time = process.arrival_time
            process.start_time = current_time
            process.completion_time = current_time + process.burst_time
            process.end_time = process.completion_time
            current_time += process.burst_time
        return current_time

    current_time = 0
    for queue in [queue1, queue2, queue3, queue4, queue5]:
        current_time = execute_queue(queue, current_time)

    # Calculate turnaround time and waiting time for each process
    for process in processes:
        process.turnaround_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time

    return processes



def draw_gantt_chart(processes):
    fig, gnt = plt.subplots()
    gnt.set_xlabel('Time')
    gnt.set_ylabel('Processes')
    gnt.set_ylim(0, 10)
    gnt.set_xlim(0, max(p.end_time for p in processes))
    gnt.set_yticks([15, 30, 45, 60, 75])
    gnt.set_yticklabels([p.pid for p in processes])
    
    for p in processes:
        gnt.broken_barh([(p.start_time, p.end_time - p.start_time)], (p.pid * 10, 9), facecolors=('tab:blue'))
    
    plt.show()

def evaluate_performance(processes):
    total_turnaround_time = sum(p.turnaround_time for p in processes)
    total_waiting_time = sum(p.waiting_time for p in processes)
    avg_turnaround_time = total_turnaround_time / len(processes) if processes else 0
    avg_waiting_time = total_waiting_time / len(processes) if processes else 0
    return avg_turnaround_time, avg_waiting_time





def main():
    
    df = pd.read_csv("processes.csv")
    print(df)
    
    processes = read_processes_from_dataframe(df)
    
    if not processes:
        print("No processes found. Please check the input file.")
        return

    print("Select a scheduling algorithm:")
    print("1. First Come First Serve (FCFS)")
    print("2. Shortest Job First (SJF)")
    print("3. Round Robin (RR)")
    print("4. Priority Scheduling")
    print("5. Multilevel Queue Scheduling")
    choice = int(input("Enter your choice: "))

    if choice == 1:
        scheduled_processes = fcfs_scheduling(processes)
    elif choice == 2:
        scheduled_processes = sjf_scheduling(processes)
    elif choice == 3:
        scheduled_processes = round_robin_scheduling(processes)
    elif choice == 4:
        scheduled_processes = priority_scheduling_preemptive(processes)
    else:
        scheduled_processes = multilevel_queue_scheduling(processes)

    
    print("Scheduled Processes:")
    for process in scheduled_processes:
        print(process)
    
    
    avg_turnaround_time, avg_waiting_time = evaluate_performance(scheduled_processes)
    
    print(f"Average Turnaround Time: {avg_turnaround_time}")
    print(f"Average Waiting Time: {avg_waiting_time}")

    # draw_gantt_chart(scheduled_processes)

if __name__ == "__main__":
    main()
