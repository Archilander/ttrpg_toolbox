import tkinter as tk
from tkinter import messagebox
import random
import Data.items as items

def run_simulation():
    try:
        # Get values from input fields
        bace_cost = float(entry_bace_cost.get()) / 2
        skill = int(entry_skill.get()) + int(entry_skill_mod.get())
        DC = int(entry_dc.get())

        bad_failures = 0
        successes = 0

        for x in range(1, 21):
            roll_result = x + skill

            if roll_result >= DC:
                successes += 1
            elif DC - roll_result >= 4:
                bad_failures += 1

        target_craft_cost = bace_cost
        try:
            avg_craft_check = ((10.5-max(10.5, bad_failures) + skill) * DC) / 10
            time_weeks = target_craft_cost / avg_craft_check
        except:
            time_weeks = -1

        if successes == 0 or time_weeks < 0:
            label_gp.config(text=f"N/A")
            label_sp.config(text=f"N/A")
            label_cp.config(text=f"N/A")
            time_label.config(text=f"Average Crafting Cost: N/A")
        else:
            p_bad = bad_failures / successes
            expected_penalty = p_bad * (bace_cost / 2)

            avg_cost = bace_cost + expected_penalty
            total_cp = round(avg_cost * 100) 
            GP = total_cp // 100
            SP = (total_cp % 100) // 10
            CP = total_cp % 10

            total_minutes = int(time_weeks * 7 * 24 * 60)

            minutes_in_month = 4 * 7 * 24 * 60
            minutes_in_week = 7 * 24 * 60
            minutes_in_day = 24 * 60
            minutes_in_hour = 60

            months = total_minutes // minutes_in_month
            total_minutes %= minutes_in_month

            weeks = total_minutes // minutes_in_week
            total_minutes %= minutes_in_week

            days = total_minutes // minutes_in_day
            total_minutes %= minutes_in_day

            hours = total_minutes // minutes_in_hour
            minutes = total_minutes % minutes_in_hour

            label_gp.config(text=f"{GP}")
            label_sp.config(text=f"{SP}")
            label_cp.config(text=f"{CP}")

            time_label.config(text=f"Crafting Time: {months}M {weeks}W {days}D {hours}H {minutes}m")

    except ValueError:
        messagebox.showerror("Invalid input", "Please enter valid numeric values.")


class AutocompleteEntry(tk.Entry):
    def __init__(self, suggestion_list, master=None, callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.suggestion_list = sorted(suggestion_list)
        self.listbox = None
        self.callback = callback
        self.bind("<KeyRelease>", self.on_keyrelease)
        self.bind("<Down>", self.move_focus_to_listbox)

    def on_keyrelease(self, event):
        if event.keysym in ("Up", "Down", "Return"):
            return 
        text = self.get()
        self.show_listbox([item for item in self.suggestion_list if text.lower() in item.lower()])

    def show_listbox(self, matches):
        if self.listbox:
            self.listbox.destroy()

        if not matches or self.get() == "":
            return

        entry_width = self.winfo_width()
        self.listbox = tk.Listbox(width=0)  # width=0 allows it to auto-expand if using `place` + `config`

        self.listbox.place(
            x=self.winfo_x(),
            y=self.winfo_y() + self.winfo_height(),
            width=entry_width * 2  # Span ~2 columns
        )
        self.listbox.bind("<ButtonRelease-1>", self.on_listbox_click)
        self.listbox.bind("<Return>", self.on_listbox_enter)
        self.listbox.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())

        for match in matches:
            self.listbox.insert(tk.END, match)

    def on_listbox_click(self, event):
        if self.listbox:
            index = self.listbox.nearest(event.y)
            self.select_item(index)

    def on_listbox_enter(self, event):
        if self.listbox:
            index = self.listbox.curselection()
            if index:
                self.select_item(index[0])
            return "break"

    def move_focus_to_listbox(self, event):
        if self.listbox:
            self.listbox.focus_set()
            self.listbox.selection_set(0)
            self.listbox.activate(0)
            return "break"

    def select_item(self, index):
        selection = self.listbox.get(index)
        self.delete(0, tk.END)
        self.insert(0, selection)
        self.listbox.destroy()
        self.listbox = None
        if self.callback:
            self.callback(selection) 

def populate_fields(item_name):
    price, dc = items.fetch_variables(item_name)
    entry_bace_cost.delete(0, tk.END)
    entry_bace_cost.insert(0, f"{price}")
    entry_dc.delete(0, tk.END)
    entry_dc.insert(0, f"{dc}")

# Set up GUI window
root = tk.Tk()
root.title("Crafting Cost Simulator")
# root.geometry("400x300")
root.resizable(False, False)

# DC row
predefined_items = items.fetch_item()
tk.Label(root, text="Item:").grid(row=0, column=0, sticky="e", pady=2)
entry_item = AutocompleteEntry(predefined_items, root, callback=populate_fields)
entry_item.insert(0, predefined_items[0])
entry_item.grid(row=0, column=1, columnspan=2, sticky="we", pady=2)

# Spacer
tk.Label(root, text="").grid(row=1)

tk.Label(root, text="DC:").grid(row=2, column=0, sticky="e")
entry_dc = tk.Entry(root)
entry_dc.insert(0, "0")
entry_dc.grid(row=2, column=1, columnspan=2, sticky="we")

# Cost row
tk.Label(root, text="Cost (GP)").grid(row=3, column=0, sticky="e")
entry_bace_cost = tk.Entry(root)
entry_bace_cost.insert(0, "0")
entry_bace_cost.grid(row=3, column=1, columnspan=2, sticky="we")

# Header row
tk.Label(root, text="").grid(row=4, column=0)
tk.Label(root, text="Base").grid(row=4, column=1)
tk.Label(root, text="Modifier").grid(row=4, column=2)

# Skill input (below modifier)
tk.Label(root, text="Skill:").grid(row=5, column=0, sticky="e")
entry_skill = tk.Entry(root)
entry_skill.insert(0, "0")
entry_skill.grid(row=5, column=1, sticky="we")

entry_skill_mod = tk.Entry(root)
entry_skill_mod.insert(0, "0")
entry_skill_mod.grid(row=5, column=2, sticky="we")

tk.Label(root, text="Special Material cost:").grid(row=6, column=0, sticky="e")
material_mod = tk.Entry(root)
material_mod.insert(0, "0")
material_mod.grid(row=6, column=1, columnspan=2, sticky="we")

# Run simulation button
tk.Button(root, text="Calculate", command=run_simulation).grid(row=7, column=0, columnspan=3, pady=10)

# Result label
result_frame = tk.Frame(root)
result_frame.grid(row=8, column=0, columnspan=3)

label_prefix = tk.Label(result_frame, text="Average Crafting Cost: ")
label_gp = tk.Label(result_frame, text="0", fg="gold", font=("Helvetica", 10, "bold"))
label_sp = tk.Label(result_frame, text="0", fg="gray", font=("Helvetica", 10, "bold"))
label_cp = tk.Label(result_frame, text="0", fg="sienna", font=("Helvetica", 10, "bold"))

label_prefix.pack(side="left")
label_gp.pack(side="left")
label_sp.pack(side="left")
label_cp.pack(side="left")


time_label = tk.Label(root, text="Estimated Crafting Time: ")
time_label.grid(row=9, column=0, columnspan=3)

root.mainloop()
