import tkinter as tk
from tkinter import messagebox, ttk
import Data.items as items

def run_simulation():
    try:
        scalar = 3
        bace_cost = float(entry_bace_cost.get()) / scalar
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
            expected_penalty = p_bad * (bace_cost / scalar)

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
        self.listbox = tk.Listbox(width=0)

        self.listbox.place(
            x=self.winfo_x(),
            y=self.winfo_y() + self.winfo_height(),
            width=entry_width * 2
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

# ** GUI **
root = tk.Tk()
root.title("Crafting Cost Simulator")
root.resizable(False, False)


# ** Result Frame **
result_frame = ttk.Frame(root)
result_frame.pack(padx=10, pady=5, fill='x')

cost_frame = ttk.Frame(result_frame)
cost_frame.pack(anchor="center")

label_prefix = tk.Label(cost_frame, text="Average Crafting Cost: ")
label_gp = tk.Label(cost_frame, text="0", fg="#b8860b", font=("Helvetica", 10, "bold"))
label_sp = tk.Label(cost_frame, text="0", fg="dim gray", font=("Helvetica", 10, "bold"))
label_cp = tk.Label(cost_frame, text="0", fg="sienna", font=("Helvetica", 10, "bold"))

label_prefix.pack(side="left")
label_gp.pack(side="left", padx=(5, 0))
label_sp.pack(side="left", padx=(5, 0))
label_cp.pack(side="left", padx=(5, 0))

time_label = ttk.Label(result_frame, text="Estimated Crafting Time:")
time_label.pack(anchor="center", pady=(5, 0))


# ** DC Frame **
frame_dc = ttk.LabelFrame(root, text="Item search")
frame_dc.pack(padx=10, pady=5, fill='x')

predefined_items = items.fetch_item()
ttk.Label(frame_dc, text="Search:").grid(row=0, column=0, sticky="e", pady=2)
entry_item = AutocompleteEntry(predefined_items, frame_dc, callback=populate_fields)
entry_item.insert(0, predefined_items[0])
entry_item.grid(row=0, column=1, columnspan=3, sticky="we", pady=2)

tk.Label(frame_dc, text="DC:").grid(row=1, column=0, sticky="e")
entry_dc = tk.Entry(frame_dc)
entry_dc.insert(0, "0")
entry_dc.grid(row=1, column=1, sticky="we")

tk.Label(frame_dc, text="Cost (GP)").grid(row=1, column=2, sticky="e")
entry_bace_cost = tk.Entry(frame_dc)
entry_bace_cost.insert(0, "0")
entry_bace_cost.grid(row=1, column=3, sticky="we")
frame_dc.columnconfigure((1, 3), weight=1)

# ** Player Skill Frame **
frame_skill = ttk.LabelFrame(root, text="Player Skill & Options")
frame_skill.pack(padx=10, pady=5, fill='x')

tk.Label(frame_skill, text="").grid(row=0, column=0)
tk.Label(frame_skill, text="Base").grid(row=0, column=2)
tk.Label(frame_skill, text="Modifier").grid(row=0, column=3)

tk.Label(frame_skill, text="Skill:").grid(row=1, column=0, columnspan=2, sticky="e")
entry_skill = tk.Entry(frame_skill)
entry_skill.insert(0, "0")
entry_skill.grid(row=1, column=2, sticky="we")

entry_skill_mod = tk.Entry(frame_skill)
entry_skill_mod.insert(0, "0")
entry_skill_mod.grid(row=1, column=3, sticky="we")

frame_skill.columnconfigure((2, 3), weight=1)


# ** Button Frame **
btn_frame = ttk.Frame(root)
btn_frame.pack(padx=10, pady=10, fill='x')

calculate_button = tk.Button(btn_frame, text="Calculate", command=run_simulation)
calculate_button.grid(row=0, column=0)
btn_frame.columnconfigure(0, weight=1)
calculate_button.pack(anchor="center")

root.mainloop()

