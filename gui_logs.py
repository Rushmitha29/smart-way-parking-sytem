import tkinter
from tkinter import scrolledtext, simpledialog

class ParkingGUI:
    def __init__(self):
        # --- Ask user for total slots ---
        self.capacity = simpledialog.askinteger("Parking Capacity", 
                                                "Enter total number of slots:", 
                                                minvalue=1, maxvalue=50)
        if not self.capacity:
            self.capacity = 4   # default if user cancels
        self.slot = self.capacity

        self.main_window = tkinter.Tk()
        self.main_window.title("Smart Parking System")
        

        # --- Title ---
        tkinter.Label(self.main_window, text="Smart Parking System", font=("Arial", 16)).pack(pady=10)

        # --- IR Inputs ---
        tkinter.Label(self.main_window, text="IR1 (0/1 or -1 to stop):").pack()
        self.ir1_entry = tkinter.Entry(self.main_window, width=10, validate="key")
        self.ir1_entry['validatecommand'] = (self.ir1_entry.register(self.validate_input), '%P')
        self.ir1_entry.pack()

        tkinter.Label(self.main_window, text="IR2 (0/1 or -1 to stop):").pack()
        self.ir2_entry = tkinter.Entry(self.main_window, width=10, validate="key")
        self.ir2_entry['validatecommand'] = (self.ir2_entry.register(self.validate_input), '%P')
        self.ir2_entry.pack()

        # --- Buttons ---
        self.process_btn = tkinter.Button(self.main_window, text="Process", command=self.process)
        self.process_btn.pack(pady=5)

        self.reset_btn = tkinter.Button(self.main_window, text="Reset", command=self.reset)
        self.reset_btn.pack(pady=5)

        self.stop_btn = tkinter.Button(self.main_window, text="Stop Program", command=self.main_window.destroy)
        self.stop_btn.pack(pady=5)

        # --- Slot Display ---
        self.slot_label = tkinter.Label(self.main_window, text=f"Slots Left: {self.slot}", font=("Arial", 12))
        self.slot_label.pack(pady=5)

        # --- Output Display (Scrolled Text) ---
        tkinter.Label(self.main_window, text="Parking Logs:").pack()
        self.output_box = scrolledtext.ScrolledText(self.main_window, width=50, height=12)
        self.output_box.pack()

        # --- Color Tags ---
        self.output_box.tag_config("entry", foreground="green")
        self.output_box.tag_config("exit", foreground="blue")
        self.output_box.tag_config("error", foreground="red")

        self.main_window.mainloop()

    # --------------------- Input Validation ----------------------
    def validate_input(self, value):
        if value in ("", "0", "1", "-1","-"):
            return True
        return False

    # --------------------- Processing Logic ----------------------
    def process(self):
        raw_ir1 = self.ir1_entry.get()
        raw_ir2 = self.ir2_entry.get()

        # Stop program
        if raw_ir1 == "-1" or raw_ir2 == "-1":
            self.log("Program Stopped.\n", "error")
            self.main_window.after(800, self.main_window.destroy)
            return

        # Validate numbers
        try:
            IR1 = int(raw_ir1)
            IR2 = int(raw_ir2)
        except:
            self.log("Invalid input! Enter 0, 1, or -1.\n\n", "error")
            return

        # -------- ENTRY CASE (IR1=0 first) --------
        if IR1 == 0 and IR2 == 1:
            if self.slot > 0:
                self.slot -= 1
                text = ("Gate Open (Entry)\n"
                        "Car Entered → Slot -1\n"
                        "Gate Close\n")
                self.log(text, "entry")
            else:
                self.log("Parking Full! Entry Blocked.\n", "error")

        # -------- EXIT CASE (IR2=0 first) --------
        elif IR1 == 1 and IR2 == 0 and self.slot < self.capacity:
            self.slot += 1
            text = ("Gate Open (Exit)\n"
                    "Car Exited → Slot +1\n"
                    "Gate Close\n")
            self.log(text, "exit")

        # -------- BOTH LOW --------
        elif IR1 == 0 and IR2 == 0 and self.slot<4:
            self.log("Both sensors triggered\n", "error")

        # -------- NO ACTIVITY --------
        else:
            self.log("No activity\n", "error")

        self.slot_label.config(text=f"Slots Left: {self.slot}")

    # --------------------- Logging Function ----------------------
    def log(self, text, tag=""):
        text += f"Slots Left: {self.slot}\n" + "-"*40 + "\n"
        self.output_box.insert(tkinter.END, text, tag)
        self.output_box.see(tkinter.END)

        # Save to file
        with open("parking_logs.txt", "a") as f:
            f.write(text)

    # --------------------- Reset Function ----------------------
    def reset(self):
        self.ir1_entry.delete(0, tkinter.END)
        self.ir2_entry.delete(0, tkinter.END)
        self.slot = self.capacity
        self.slot_label.config(text=f"Slots Left: {self.slot}")
        self.output_box.delete("1.0", tkinter.END)

# Run the GUI
gui = ParkingGUI()