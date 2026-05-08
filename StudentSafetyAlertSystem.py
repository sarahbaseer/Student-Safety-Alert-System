import tkinter as tk

#load data from file
outbreaks = []

def load_data():
    global outbreaks
    outbreaks = []

    file = open("/users/sarahbaseer/Documents/GitHub/ssas/outbreaks.txt", "r")
    #strip whitespace and split by comma, then create alert dictionary and add to list
    for line in file:
        line = line.strip()
        parts = line.split(",")

        alert = {
            "name": parts[0],
            "type": parts[1],
            "location": parts[2],
            "severity": parts[3],
            "prevention": parts[4]
        }

        outbreaks.append(alert)

    file.close()

load_data()

#gui setup
window = tk.Tk()
window.title("Student Safety Alert System")
window.geometry("1000x700")

#main layout, sidebar on left, content on right
main_frame = tk.Frame(window)
main_frame.pack(fill="both", expand=True)

sidebar = tk.Frame(main_frame, width=300, bg="#cccccc")
sidebar.pack(side="left", fill="y")

content = tk.Frame(main_frame, bg="white")
content.pack(side="right", fill="both", expand=True)

#output box
output_box = tk.Text(content, height=25, width=80)
output_box.pack(pady=10, padx=10, fill="both", expand=True)

#functions
def clear_output():
    output_box.delete("1.0", tk.END)

def display_text(text):
    output_box.insert(tk.END, text + "\n")

#function to print alert details in output box
def print_alert(alert, index=None):
    display_text("\n-------------------")
    if index is not None:
        display_text(f"Alert #{index+1}")

    display_text(f"Name: {alert['name']}")
    display_text(f"Type: {alert['type']}")
    display_text(f"Location: {alert['location']}")
    display_text(f"Severity: {alert['severity']}")
    display_text(f"Prevention: {alert['prevention']}")

    if alert["severity"] == "Red":
        display_text("Recommendation: Avoid immediately.")
    elif alert["severity"] == "Orange":
        display_text("Recommendation: Use caution.")
    else:
        display_text("Recommendation: Stay informed.")

#view all alerts with index numbers
def view_all_alerts():
    clear_output()
    for i in range(len(outbreaks)):
        print_alert(outbreaks[i], i)

#view one alert using index
def view_single_alert():
    clear_output()
    choice = entry.get()

    if choice.isdigit():
        index = int(choice) - 1

        if 0 <= index < len(outbreaks):
            print_alert(outbreaks[index], index)
        else:
            #input validation for out of range index
            display_text("Invalid alert number.")
    else:
        display_text("Enter a valid number.")

#filter by location (case-insensitive)
def filter_by_location():
    clear_output()
    user_location = entry.get()

    found = False

    for alert in outbreaks:
        if alert["location"].lower() == user_location.lower():
            print_alert(alert)
            found = True
    #input validation for no matches found
    if not found:
        display_text("No alerts found for that location.")

#filter by type (case-insensitive)
def filter_by_type():
    clear_output()
    user_type = entry.get()

    found = False

    for alert in outbreaks:
        if alert["type"].lower() == user_type.lower():
            print_alert(alert)
            found = True
    #input validation for no matches found
    if not found:
        display_text("No alerts found for that type.")

#count severity levels
def count_severity():
    clear_output()

    red = orange = yellow = 0

    for alert in outbreaks:
        if alert["severity"] == "Red":
            red += 1
        elif alert["severity"] == "Orange":
            orange += 1
        else:
            yellow += 1

    display_text("----- Severity Summary -----")
    display_text(f"Red: {red}")
    display_text(f"Orange: {orange}")
    display_text(f"Yellow: {yellow}")

#add new alert to file
def add_new_alert():
    name = name_entry.get().strip()
    type_ = type_entry.get().strip()
    location = location_entry.get().strip()
    severity = severity_entry.get().strip()
    prevention = prevention_entry.get().strip()

    #input validation to ensure all fields are filled
    if not name or not type_ or not location or not severity or not prevention:
        display_text("Please fill in all fields.")
        return

    new_line = f"{name},{type_},{location},{severity},{prevention}\n"

    #append new alert to file
    file = open("/users/sarahbaseer/Documents/GitHub/ssas/outbreaks.txt", "a")
    file.write(new_line)
    file.close()

    load_data()
    display_text("New alert added successfully!")

#sidebar user interface
tk.Label(sidebar, text="Input (Number / Location / Type):", bg="#3d85c6").pack(pady=5)
entry = tk.Entry(sidebar, width=25)
entry.pack(pady=5)

tk.Label(sidebar, text="Add New Alert", bg="#3d85c6", font=("Arial", 14, "bold")).pack(pady=10)
tk.Label(sidebar, text="Name", bg="#3d85c6").pack()
name_entry = tk.Entry(sidebar, width=25)
name_entry.pack()

tk.Label(sidebar, text="Type", bg="#3d85c6").pack()
type_entry = tk.Entry(sidebar, width=25)
type_entry.pack()

tk.Label(sidebar, text="Location", bg="#3d85c6").pack()
location_entry = tk.Entry(sidebar, width=25)
location_entry.pack()

tk.Label(sidebar, text="Severity (Red / Orange / Yellow)", bg="#3d85c6").pack()
severity_entry = tk.Entry(sidebar, width=25)
severity_entry.pack()

tk.Label(sidebar, text="Prevention", bg="#3d85c6").pack()
prevention_entry = tk.Entry(sidebar, width=25)
prevention_entry.pack()

#buttons ui
tk.Button(sidebar, text="View All Alerts", command=view_all_alerts).pack(fill="x", pady=2)
tk.Button(sidebar, text="View Single Alert", command=view_single_alert).pack(fill="x", pady=2)
tk.Button(sidebar, text="Filter by Location", command=filter_by_location).pack(fill="x", pady=2)
tk.Button(sidebar, text="Filter by Type", command=filter_by_type).pack(fill="x", pady=2)
tk.Button(sidebar, text="Count Severity", command=count_severity).pack(fill="x", pady=2)
tk.Button(sidebar, text="Add New Alert", command=add_new_alert).pack(fill="x", pady=5)
tk.Button(sidebar, text="Clear Output", command=clear_output).pack(fill="x", pady=2)
tk.Button(sidebar, text="Exit", command=window.quit).pack(fill="x", pady=10)

#run the application
window.mainloop()