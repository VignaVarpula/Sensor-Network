import tkinter as tk
import matplotlib.pyplot as plt
from tkinter import *

window = Tk()
window.geometry("1600x800")

# Load the background image using PhotoImage
# Adjust the path to the image file as needed
background_image = PhotoImage(file="C:\\Users\\Varpula Vigna\\OneDrive\\Desktop\\WISE Project - Sensor Network\\sensor network.png")

# Create a label with the background image
background_label = Label(window, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

label_1 = Label(window, text="WIRELESS SENSOR NETWORK")
font_tuple = ("comic sans ms", 50, "bold")
label_1.config(font=font_tuple)
label_1.pack()

def communicating_sensors(sensors, d):
    def distance(sensor1, sensor2):
        x1, y1 = sensor1
        x2, y2 = sensor2
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    # Create adjacency list for graph
    adj_list = {i: set() for i in sensors}
    for i in sensors:
        for j in sensors:
            if i != j and distance(sensors[i], sensors[j]) <= d:
                adj_list[i].add(j)
                adj_list[j].add(i)

    # Find the largest subset where all nodes are directly connected
    def find_max_clique():
        max_clique = []
        nodes = list(adj_list.keys())
        
        def is_clique(candidate):
            return all(v in adj_list[u] for u in candidate for v in candidate if u != v)
        
        def backtrack(start, clique):
            nonlocal max_clique
            if len(clique) > len(max_clique):
                max_clique = clique[:]
            for i in range(start, len(nodes)):
                node = nodes[i]
                if all(node in adj_list[member] for member in clique):
                    clique.append(node)
                    backtrack(i + 1, clique)
                    clique.pop()
        
        backtrack(0, [])
        return max_clique

    max_sensor = find_max_clique()
    return len(max_sensor), max_sensor

def plot_graph(sensors):
    x_values = [sensor[0] for sensor in sensors.values()]
    y_values = [sensor[1] for sensor in sensors.values()]

    plt.scatter(x_values, y_values, color='red', label='Sensors')
    plt.xlabel('X-coordinate')
    plt.ylabel('Y-coordinate')
    plt.title('Sensor Coordinates')
    plt.grid(True)
    plt.legend()
    plt.show()

def input_window():
    def create_sensor_entries():
        try:
            num_sensors = int(entry_n.get())
            for widget in sensor_frame.winfo_children():
                widget.destroy()
            for i in range(num_sensors):
                label_sensor_i = tk.Label(sensor_frame, text=f"Sensor {i + 1} (x y):", bg='lightblue')
                label_sensor_i.configure(font=font_tuple)
                label_sensor_i.grid(row=i, column=0, padx=5, pady=5)
                entry_sensor_i = tk.Entry(sensor_frame)
                entry_sensor_i.grid(row=i, column=1, padx=5, pady=5)
                entries_sensors[i + 1] = entry_sensor_i
        except ValueError:
            pass

    def result_window():
        result_window = Toplevel(root)
        result_window.geometry('1600x800')
        result_window.configure(bg="lightgreen")

        try:
            n = int(entry_n.get())
            d = float(entry_d.get())
            sensors = {}
            for i in range(1, n + 1):
                x, y = map(float, entries_sensors[i].get().split())
                sensors[i] = [x, y]

            max_size, max_sensor = communicating_sensors(sensors, d)
            result_label = Label(result_window, text=f"RESULT \n\n Max Size: {max_size}\nMax Sensor: {max_sensor}", bg="lightgreen", font=("arial", 40, "bold"))
            result_label.pack()

            exit_button = tk.Button(result_window, text="EXIT", height=1, width=10, font=("arial", 10, "bold"), command=result_window.destroy)
            exit_button.place(x=700, y=400)
        except ValueError:
            pass

    def graph_window():
        try:
            n = int(entry_n.get())
            d = float(entry_d.get())
            sensors = {}
            for i in range(1, n + 1):
                x, y = map(float, entries_sensors[i].get().split())
                sensors[i] = [x, y]

            plot_graph(sensors)
        except ValueError:
            pass

    root = Toplevel(window)
    root.title("Sensor Communication")
    root.geometry('1600x800')
    root.configure(bg='lightblue')

    label_n = tk.Label(root, text="Enter the number of sensors (n):", bg='lightblue')
    font_tuple = ("comic Sans MS", 20, "bold")
    label_n.configure(font=font_tuple)
    label_n.grid(row=0, column=0, padx=5, pady=5)
    entry_n = tk.Entry(root)
    entry_n.grid(row=0, column=1, padx=5, pady=5)

    label_d = tk.Label(root, text="Enter the communication distance (d):", bg='lightblue')
    label_d.configure(font=font_tuple)
    label_d.grid(row=1, column=0, padx=5, pady=5)
    entry_d = tk.Entry(root)
    entry_d.grid(row=1, column=1, padx=5, pady=5)

    label_sensors = tk.Label(root, text="Sensor coordinates will appear here:", bg='lightblue')
    label_sensors.configure(font=font_tuple)
    label_sensors.grid(row=2, column=0, padx=5, pady=5, columnspan=2)

    sensor_frame = tk.Frame(root, bg='lightblue')
    sensor_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    entries_sensors = {}

    update_button = tk.Button(root, text="Update Sensor Inputs", bg="lightpink", font=("arial", 10, "bold"), command=create_sensor_entries)
    update_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    graph_button = tk.Button(root, text="SHOW GRAPH", bg="lightpink", font=("arial", 10, "bold"), command=graph_window)
    graph_button.grid(row=5, column=0, padx=5, pady=5)

    result_button = tk.Button(root, text="SHOW RESULT", bg="lightpink", font=("arial", 10, "bold"), command=result_window)
    result_button.grid(row=5, column=1, padx=5, pady=5)

start_button = tk.Button(window, text="START", font=("arial", 20, "bold"), height=1, width=10, command=input_window)
start_button.place(x=650, y=600)

window.mainloop()
