#-----------------------------
# IMPORTED LIBRARIES
#-----------------------------
import time
import threading
import tkinter as tk
from datetime import datetime, timedelta

#-----------------------------
# set_alarm() FUNCTION  
# This function sets an alarm based on input from three tkinter variables
#-----------------------------
def set_alarm():

    if hour_var.get().isdigit() and \
        minute_var.get().isdigit() and \
        second_var.get().isdigit():
        
        alarm_time = f"{int(hour_var.get()):02d}:{int(minute_var.get()):02d}:{int(second_var.get()):02d}"
       
        popup_window = tk.Toplevel(window)
        popup_window.title("Alarm Set")
        popup_window.geometry("300x150+{}+{}".format(
            int(window.winfo_screenwidth() / 2 - 150),  # Center the window horizontally
            int(window.winfo_screenheight() / 2 - 75)  # Center the window vertically
        ))
        popup_window.resizable(False, False)
        message_label = tk.Label(popup_window, text="Alarm set for {}".format(alarm_time), font=("Arial", 16))
        message_label.pack(fill="both", padx=20, pady=10)
        close_message_label = tk.Label(popup_window, text="This window will close in 5 seconds.", font=("Arial", 12))
        close_message_label.pack(fill="both", padx=20, pady=10)

        # Automatically close the popup window after 5 seconds
        popup_window.after(5000, lambda: popup_window.destroy())

        threading.Thread(target=wait_for_alarm, args=(alarm_time,)).start()
    else:
        print("Invalid input. Please enter valid numbers for the hours, minutes, and seconds.")
#------------------------------
# wait_for_alarm() FUNCTION 
# This function waits for the alarm time to be reached and 
# then displays a popup window with a message to wake up the user 
#------------------------------
def wait_for_alarm(alarm_time):
    global alarm_active
    alarm_active = True
    while True:
        current_time = datetime.now().strftime("%H:%M:%S")
        if current_time == alarm_time:
            popup_window = tk.Toplevel(window)
            popup_window.title("Wake Up!")
            popup_window.geometry("300x120+{}+{}".format(
                int(window.winfo_screenwidth() / 2 - 150),  # Center the window horizontally
                int(window.winfo_screenheight() / 2 - 60)  # Center the window vertically
            ))
            popup_window.resizable(False, False)
            message_label = tk.Label(popup_window, text="Wake up!", font=("Arial", 24))
            message_label.pack(fill="both", padx=20, pady=20)

            break
        if not alarm_active:
            break
        time_remaining = datetime.strptime(alarm_time, "%H:%M:%S") - datetime.strptime(current_time, "%H:%M:%S")
        countdown_var.set(str(time_remaining))  # Update the countdown label
        time.sleep(1)
    # Reset the alarm_active variable
    alarm_active = False
#-----------------------------
# snooze_alarm() FUNCTION
# This function stops the alarm and sets a new alarm to go off in 5 minutes
#-----------------------------
def snooze_alarm():
    # Stop the alarm and set a new alarm to go off in 5 minutes
    hour = int(hour_var.get())
    minute = int(minute_var.get())
    second = int(second_var.get()) + 300  # Add 5 minutes to the current second
    if second >= 60:
        minute += 1
        second -= 60
    if minute >= 60:
        hour += 1
        minute -= 60
    hour_var.set(str(hour))
    minute_var.set(str(minute))
    second_var.set(str(second))
    start_alarm()
#-----------------------------
# stop_alarm() FUNCTION
# This function stops the alarm and clears the input fields
#-----------------------------
def stop_alarm():
    global alarm_active
    alarm_active = False  # Stop the countdown timer
    # Stop the alarm and clear the input fields
    hour_var.set("")
    minute_var.set("")
    second_var.set("")
    countdown_var.set("")
    clock_label.config(text=datetime.now().strftime("%H:%M:%S"))
#-----------------------------
# start_alarm() FUNCTION
# This function starts the alarm
#-----------------------------
def start_alarm():
    window.after(1000, update_clock)
#-----------------------------
# update_clock() FUNCTION
# This function updates the digital clock
#-----------------------------
def update_clock():
    current_time = datetime.now().strftime("%H:%M:%S")
    clock_label.config(text=current_time)
    window.after(1000, update_clock)

#-----------------------------
# GUI Create the main window
#-----------------------------
window = tk.Tk()
window.title("Alarm Clock")
window.configure(bg="sky blue")
window.geometry("500x500+{}+{}".format(
    int(window.winfo_screenwidth() / 2 - 200),  # Center the window horizontally
    int(window.winfo_screenheight() / 2 - 150)  # Center the window vertically
))
window.resizable(False, False)

# Create the digital clock
clock_frame = tk.Frame(window, bg="sky blue", width=440, height=220)
clock_frame.pack(pady=20)
clock_label = tk.Label(clock_frame, font=("DS-Digital", 80), fg="black", bg="sky blue")
clock_label.place(relx=0.5, rely=0.5, anchor="center")

update_clock()
# Create the input fields and buttons
input_frame = tk.Frame(window)
input_frame.pack(pady=20)
tk.Label(input_frame, text="Hour:", font=("Arial", 16)).grid(row=0, column=0)
tk.Label(input_frame, text="Minute:", font=("Arial", 16)).grid(row=1, column=0)
tk.Label(input_frame, text="Second:", font=("Arial", 16)).grid(row=2, column=0)

hour_var = tk.StringVar()
minute_var = tk.StringVar()
second_var = tk.StringVar()
countdown_var = tk.StringVar()

hour_entry = tk.Entry(input_frame, textvariable=hour_var, font=("Arial", 16)).grid(row=0, column=1)
minute_entry = tk.Entry(input_frame, textvariable=minute_var, font=("Arial", 16)).grid(row=1, column=1)
second_entry = tk.Entry(input_frame, textvariable=second_var, font=("Arial", 16)).grid(row=2, column=1)

set_button = tk.Button(input_frame, text="Set Alarm", font=("Arial", 16), command=set_alarm).grid(row=3, columnspan=2)
snooze_button = tk.Button(window, text="Snooze", font=("Arial", 16), command=snooze_alarm)
snooze_button.pack(side="left", padx=20)
stop_button = tk.Button(window, text="Stop", font=("Arial", 16), command=stop_alarm)
stop_button.pack(side="right", padx=20)

# Create the countdown label
countdown_frame = tk.Frame(window, bg="sky blue", width=440, height=220)
countdown_frame.pack(pady=20)
tk.Label(countdown_frame, textvariable=countdown_var, font=("Arial", 16)).pack()

#-----------------------------
# Start the program
#-----------------------------
window.mainloop()
