import matplotlib.pyplot as plt
import numpy as np

def get_num_processes():
    while True:
        try:
            num_processes = int(input("Enter how many processes you would like to analyze: "))
            if num_processes > 0:
                return num_processes
            else:
                print("Number of processes must be greater than 0. Please try again.")
        except ValueError:
            print("Please enter a valid integer.")

def generate_random_data(num_processes):
    burst_durations = []
    priorities = np.random.permutation(np.arange(1, num_processes + 1)).tolist()

    for i in range(1, num_processes + 1):
        burst = np.random.choice(range(1, 51))
        priority = priorities[i-1]
        burst_durations.append(burst)
        
    return burst_durations, priorities

def generate_range_data(num_processes):
    burst_durations = []
    priorities = []
    
    burst_min = int(input("Enter the minimum burst duration: "))
    burst_max = int(input("Enter the maximum burst duration: "))
    
    available_priorities = list(range(1, num_processes + 1))
    
    for i in range(1, num_processes + 1):
        burst = np.random.choice(range(burst_min, burst_max + 1))
        
        # Ensure unique priorities
        priority = np.random.choice(available_priorities)
        available_priorities.remove(priority)
        
        burst_durations.append(burst)
        priorities.append(priority)

    return burst_durations, priorities

def manual_input_data(num_processes):
    burst_durations = []
    priorities = []
    for i in range(1, num_processes + 1):
        burst = int(input(f"Enter burst duration for P{i}: "))
        priority = int(input(f"Enter priority for P{i}: "))
        burst_durations.append(burst)
        priorities.append(priority)

    print(burst_durations, priorities)
    return burst_durations, priorities

def generate_table(num_processes, burst_durations, priorities):
    print("{:<10} {:<20} {:<10}".format("Process", "Burst Duration (ms)", "Priority"))
    for i in range(1, num_processes + 1):
        print("{:<10} {:<20} {:<10}".format(f"P{i}", burst_durations[i-1], priorities[i-1]))

def generate_bar_chart1(num_processes, burst_durations, priorities, ax):
    x_values = np.arange(1, num_processes + 1)
    colors = plt.cm.viridis(np.linspace(0, 1, num_processes))
    ax.bar(x_values, burst_durations, color=colors, label=[f'P{i}' for i in range(1, num_processes + 1)])
    ax.set_xlabel("Process")
    ax.set_ylabel("Burst Duration (ms)")

# def generate_bar_chart2(num_processes, burst_durations, priorities, ax):
#     # Calculate the start and end times for each process    
#     start_times = np.cumsum([0] + burst_durations[:-1]) 
#     end_times = np.cumsum(burst_durations)

#     colors = plt.cm.viridis(np.linspace(0, 1, num_processes))


#     for i in range(num_processes):
#         y_values = np.full_like(start_times, 0)
#         ax.barh(y_values, width=end_times[i] - start_times[i], left=start_times[i], color=colors[i], label=f'P{i + 1}')

#     ax.set_xlabel("Time")
#     ax.set_ylabel("Process")
#     ax.set_yticks([1])  # Set y-ticks for a single bar
#     ax.set_title("Total Burst Duration time for all processes")

#     x_ticks = np.concatenate(([0], end_times))
#     ax.set_xticks(x_ticks)
#     ax.set_xticklabels(x_ticks)

def generate_bar_chart2(num_processes, burst_durations, priorities, ax):
    colors = plt.cm.viridis(np.linspace(0, 1, num_processes))

    for i in range(num_processes):
        ax.barh(i, burst_durations[i], color=colors[i], label=f'P{i + 1}', left=np.sum(burst_durations[:i]))

    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Process")
    ax.set_yticks(range(num_processes))
    ax.set_yticklabels([f'P{i + 1}' for i in range(num_processes)])
    ax.set_title("Gantt Chart with Burst Durations")
    ax.legend()

    x_ticks = np.concatenate(([0], np.cumsum(burst_durations)))
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_ticks)

def generate_bar_chart3(num_processes, burst_durations, priorities, ax):
    colors = plt.cm.viridis(np.linspace(0, 1, num_processes))
    sorted_indices = np.argsort(burst_durations)[::-1]
    sorted_burst_durations = np.array(burst_durations)[sorted_indices]
    sorted_colors = np.array(colors)[sorted_indices]
    bottom = np.zeros(num_processes)

    cumulative_burst_durations = np.zeros(num_processes)

    for i in range(num_processes):
        ax.barh(1, sorted_burst_durations[i], left=bottom[i], color=sorted_colors[i], label=f'P{sorted_indices[i] + 1}')
        bottom[i] += sorted_burst_durations[i]
        cumulative_burst_durations[i] = np.sum(sorted_burst_durations[:i+1])

    ax.set_xlabel("Burst Duration (ms)")
    ax.set_ylabel("Process")
    ax.set_yticks([1])
    ax.set_title("Sorted Stacked Bar Chart with Burst Durations")
    ax.legend()

    x_ticks = np.concatenate(([0], burst_durations))
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_ticks)



def main():
    num_processes = get_num_processes() 
    option = int(input("Would you like Burst Durations and Priorities to be:\n1. Randomly generated\n2. Range\n3. Manually\nEnter your choice (1/2/3): "))
    if option == 1:
        burst_durations, priorities = generate_random_data(num_processes)
    elif option == 2:
        burst_durations, priorities = generate_range_data(num_processes)
    elif option == 3:
        burst_durations, priorities = manual_input_data(num_processes)
    else:
        print("Invalid choice. Exiting.")
        return

    # Generate the figure and set its size
    fig = plt.figure(figsize=(20, 20))

    # Generate table at subplot position (2, 2)
    ax4 = fig.add_subplot(221, frame_on=False) # no visible frame 
    ax4.xaxis.set_visible(False) # hide the x axis
    ax4.yaxis.set_visible(False) # hide the y axis

    table_data = [("Process", "Burst Duration (ms)", "Priority")] + \
                [(f"P{i}", burst_durations[i-1], priorities[i-1]) for i in range(1, num_processes + 1)]
    table = ax4.table(cellText=table_data, loc='center', cellLoc = 'center', rowLoc = 'center')
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 3.5)
    # Create a grid of 2x2 subplots and generate each of bar chart in those
    ax1 = fig.add_subplot(222)
    generate_bar_chart1(num_processes, burst_durations, priorities, ax1) 
    ax2 = fig.add_subplot(223)
    generate_bar_chart2(num_processes, burst_durations, priorities, ax2)
    ax3 = fig.add_subplot(224)
    generate_bar_chart3(num_processes, burst_durations, priorities, ax3)

    plt.tight_layout()
    plt.subplots_adjust(wspace=0.4, hspace=0.4)

    # Show the entire figure
    plt.show()

if __name__ == "__main__":
    main()
