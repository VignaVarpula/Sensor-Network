import tkinter as tk
import matplotlib.pyplot as plt
from tkinter import *

window = Tk()
window.geometry("1600x800")

background_image = PhotoImage(file="C:\\Users\\Varpula Vigna\\OneDrive\\Desktop\\WISE Project - Sensor Network\\sensor network.png")

background_label = Label(window, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

label_1 = Label(window, text="WIRELESS SENSOR NETWORK")
font_tuple = ("comic sans ms", 50, "bold")
label_1.config(font=font_tuple)
label_1.pack()

def communicating_sensors(sensors, d, n):
    communicable_sensors = []
    for i in range(1, n):
        set_sensors = set()  
        for j in range(i + 1, n + 1):
            x1, y1 = sensors[i]
            x2, y2 = sensors[j]
            distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
            if distance <= d:
                set_sensors.add(i)
                set_sensors.add(j)
        communicable_sensors.append(list(set_sensors))

    max_size = 0
    max_sensor = []
    for i in communicable_sensors:
        length = len(i)
        if length > max_size:
            max_size = length
            max_sensor = i

    return max_size, max_sensor

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
                entry_text = entries_sensors[i].get()
                if entry_text.strip() == "":
                    continue  
                x, y = map(float, entry_text.split())
                sensors[i] = [x, y]

            print(f"Number of sensors: {n}, Distance: {d}, Sensors: {sensors}") 

            max_size, max_sensor = communicating_sensors(sensors, d, n)
            result_label = Label(result_window, text=f"RESULT \n\n Max Size: {max_size}\nMax Sensor: {max_sensor}", bg="lightgreen", font=("arial", 40, "bold"))
            result_label.pack()

            exit_button = tk.Button(result_window, text="EXIT", height=1, width=10, font=("arial", 10, "bold"), command=result_window.destroy)
            exit_button.place(x=700, y=400)
        except ValueError as ve:
            print(f"ValueError: {ve}")  

    def graph_window():
        try:
            n = int(entry_n.get())
            d = float(entry_d.get())
            sensors = {}
            for i in range(1, n + 1):
                entry_text = entries_sensors[i].get()
                if entry_text.strip() == "":
                    continue 
                x, y = map(float, entry_text.split())
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
    graph_button.grid(row=8, column=0, padx=5, pady=5)

    result_button = tk.Button(root, text="SHOW RESULT", bg="lightpink", font=("arial", 10, "bold"), command=result_window)
    result_button.grid(row=8, column=1, padx=5, pady=5)


start_button = tk.Button(window, text="START", font=("arial", 20, "bold"), height=1, width=10, command=input_window)
start_button.place(x=650, y=600)

window.mainloop()
