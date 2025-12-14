import simpy
import pandas as pd
import matplotlib.pyplot as plt


#DAtaset



waste_data = [
    {"Bin_ID": "B001", "Arrival_Time": 0,  "Service_Time": 6},
    {"Bin_ID": "B002", "Arrival_Time": 2,  "Service_Time": 7},
    {"Bin_ID": "B003", "Arrival_Time": 4,  "Service_Time": 5},
    {"Bin_ID": "B004", "Arrival_Time": 6,  "Service_Time": 8},
    {"Bin_ID": "B005", "Arrival_Time": 8,  "Service_Time": 6},
    {"Bin_ID": "B006", "Arrival_Time": 10, "Service_Time": 7},
    {"Bin_ID": "B007", "Arrival_Time": 12, "Service_Time": 5},
    {"Bin_ID": "B008", "Arrival_Time": 14, "Service_Time": 8},
    {"Bin_ID": "B009", "Arrival_Time": 16, "Service_Time": 6},
    {"Bin_ID": "B010","Arrival_Time": 18, "Service_Time": 7},
]

data = pd.DataFrame(waste_data)


# Bin Process

def bin_process(env, bin_data, trucks, wait_times):
    # Wait untill bin arrival 
    yield env.timeout(bin_data["Arrival_Time"] - env.now)
    arrival = env.now

    with trucks.request() as req:
        yield req
        start_service = env.now
        wait_time = start_service - arrival

        yield env.timeout(bin_data["Service_Time"])
        wait_times.append(wait_time)


# Simulation Runner

def run_simulation(truck_count):
    env = simpy.Environment()
    trucks = simpy.Resource(env, capacity=truck_count)
    wait_times = []

    for _, row in data.iterrows():
        env.process(bin_process(env, row, trucks, wait_times))

    env.run()

    return (
        sum(wait_times) / len(wait_times),  
        max(wait_times)                     
    )


# Experiments

truck_counts = [1, 2, 3]
avg_waits = []
max_waits = []

for t in truck_counts:
    avg, mx = run_simulation(t)
    avg_waits.append(avg)
    max_waits.append(mx)
    print(f"Trucks: {t} | Avg wait: {avg:.2f} min | Max wait: {mx:.2f} min")


# GRAPH 1: Average Waiting Time

plt.figure()
plt.plot(truck_counts, avg_waits, marker='o')
plt.xlabel("Number of Trucks")
plt.ylabel("Average Waiting Time (minutes)")
plt.title("Average Waiting Time vs Number of Trucks")
plt.grid(True)
plt.savefig("avg_waiting_time.png")
plt.close()



# GRAPH 2: Maximum Waiting Time 

plt.figure()
plt.bar(truck_counts, max_waits)
plt.xlabel("Number of Trucks")
plt.ylabel("Maximum Waiting Time (minutes)")
plt.title("Maximum Waiting Time vs Number of Trucks")
plt.grid(True, axis='y')
plt.savefig("max_waiting_time.png")
plt.close()
print("Graphs saved as avg_waiting_time.png and max_waiting_time.png")
