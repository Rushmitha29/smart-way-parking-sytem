import tkinter
from tkinter import scrolledtext

class ParkingGUI:
    def __init__(self):
        self.slot = 4   # Initial parking slots
        
        self.main_window = tkinter.Tk()
        self.main_window.title("Smart Parking System")

        # --- Title ---
        tkinter.Label(self.main_window, text="Smart Parking System", font=("Arial", 16)).pack(pady=10)

        # --- IR Inputs ---
        tkinter.Label(self.main_window, text="IR1 (0/1):").pack()
        self.ir1_entry = tkinter.Entry(self.main_window, width=10)
        self.ir1_entry.pack()

        tkinter.Label(self.main_window, text="IR2 (0/1):").pack()
        self.ir2_entry = tkinter.Entry(self.main_window, width=10)
        self.ir2_entry.pack()

        # --- Buttons ---
        self.process_btn = tkinter.Button(self.main_window, text="Process", command=self.process)
        self.process_btn.pack(pady=5)

        self.reset_btn = tkinter.Button(self.main_window, text="Reset", command=self.reset)
        self.reset_btn.pack(pady=5)

        # --- Output Display (Scrolled Text) ---
        tkinter.Label(self.main_window, text="Parking Logs:").pack()
        self.output_box = scrolledtext.ScrolledText(self.main_window, width=40, height=12)
        self.output_box.pack()

        self.main_window.mainloop()

    # --------------------- Processing Logic ----------------------
    def process(self):
        raw_ir1 = self.ir1_entry.get()
        raw_ir2 = self.ir2_entry.get()

        # If user stops the program
        if raw_ir1 == "-1" or raw_ir2 == "-1":
            self.output_box.insert(tkinter.END, "Program Stopped.\n")
            self.main_window.after(800, self.main_window.destroy)
            return

        # Validate numbers
        try:
            IR1 = int(raw_ir1)
            IR2 = int(raw_ir2)
        except:
            self.output_box.insert(tkinter.END, "Invalid input! Enter 0 or 1.\n\n")
            return

        # -------- ENTRY CASE (IR1=0 first) --------
        if IR1 == 0 and IR2 == 1:
            if self.slot > 0:
                self.slot -= 1
                text = ("Gate Open (Entry)\n"
                        "Car Entered → Slot -1\n"
                        "Gate Close\n")
            else:
                text = "Parking Full! Entry Blocked.\n"

        # -------- EXIT CASE (IR2=0 first) --------
        elif IR1 == 1 and IR2 == 0 and self.slot<4:
            self.slot += 1
            text = ("Gate Open (Exit)\n"
                    "Car Exited → Slot +1\n"
                    "Gate Close\n")

        # -------- BOTH LOW --------
        elif IR1 == 0 and IR2 == 0:
            text = "Both sensors triggered \n"

        # -------- NO ACTIVITY --------
        else:
            text = "No activity\n"

        text += f"Slots Left: {self.slot}\n" + "-"*40 + "\n"
        self.output_box.insert(tkinter.END, text)

    # --------------------- Reset Function ----------------------
    def reset(self):
        self.ir1_entry.delete(0, tkinter.END)
        self.ir2_entry.delete(0, tkinter.END)
        self.slot = 4
        self.output_box.delete("1.0", tkinter.END)

# Run the GUI
gui = ParkingGUI()