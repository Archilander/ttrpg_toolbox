import tkinter as tk
from tkinter import messagebox
import random

def run_simulation():
    try:
        # Get values from input fields
        mod = int(entry_mod.get())
        bace_cost = float(entry_bace_cost.get())/2
        mod_cost = float(entry_mod_cost.get())/2
        skill = int(entry_skill.get()) + int(entry_skill_mod.get())
        bace_dc = int(entry_bace_dc.get())
        mod_dc = int(entry_mod_dc.get())
        DC = bace_dc + mod_dc * mod

        cost = 0

        target_craft_cost = (bace_cost + mod_cost * mod) * 2
        avg_craft_check = ((10.5 + skill) * DC) * 0.25
        time_weeks = target_craft_cost / avg_craft_check

        bad_failures = 0
        successes = 0

        cost = (bace_cost + (mod_cost * mod))

        for x in range(1, 21):
            roll_result = x + skill

            if roll_result >= DC:
                successes += 1
            elif DC - roll_result >= 4:
                bad_failures += 1

        if successes == 0:
            label_gp.config(text=f"N/A")
            label_sp.config(text=f"N/A")
            label_cp.config(text=f"N/A")
            time_label.config(text=f"Average Crafting Cost: N/A")
        else:
            # Chance of a bad failure per success
            p_bad = bad_failures / successes
            expected_penalty = p_bad * ((bace_cost + (mod_cost * mod)) / 2)

            avg_cost = cost + expected_penalty
            total_cp = round(avg_cost * 100)  # Convert to copper for precision
            GP = total_cp // 100
            SP = (total_cp % 100) // 10
            CP = total_cp % 10

            total_hours = int(time_weeks * 7 * 24)

            months = total_hours // (4 * 7 * 24)
            remaining_hours = total_hours % (4 * 7 * 24)

            weeks = remaining_hours // (7 * 24)
            remaining_hours %= (7 * 24)

            days = remaining_hours // 24
            hours = remaining_hours % 24

            label_gp.config(text=f"{GP}")
            label_sp.config(text=f"{SP}")
            label_cp.config(text=f"{CP}")

            time_label.config(text=f"Crafting Time: {months}M {weeks}W {days}D {hours}H")

    except ValueError:
        messagebox.showerror("Invalid input", "Please enter valid numeric values.")

# Set up GUI window
root = tk.Tk()
root.title("Crafting Cost Simulator")

# Header row
tk.Label(root, text="").grid(row=0, column=0)
tk.Label(root, text="Base").grid(row=0, column=1)
tk.Label(root, text="Modifier").grid(row=0, column=2)

# Cost row
tk.Label(root, text="Cost (GP)").grid(row=1, column=0, sticky="e")
entry_bace_cost = tk.Entry(root)
entry_bace_cost.insert(0, "0")
entry_bace_cost.grid(row=1, column=1)

entry_mod_cost = tk.Entry(root)
entry_mod_cost.insert(0, "0")
entry_mod_cost.grid(row=1, column=2)

# DC row
tk.Label(root, text="DC").grid(row=2, column=0, sticky="e")
entry_bace_dc = tk.Entry(root)
entry_bace_dc.insert(0, "0")
entry_bace_dc.grid(row=2, column=1)

entry_mod_dc = tk.Entry(root)
entry_mod_dc.insert(0, "0")
entry_mod_dc.grid(row=2, column=2)

# Spacer
tk.Label(root, text="").grid(row=3)

# Modifier input (below table)
tk.Label(root, text="Modifier:").grid(row=4, column=0, sticky="e")
entry_mod = tk.Entry(root)
entry_mod.insert(0, "0")
entry_mod.grid(row=4, column=1, columnspan=2, sticky="we")

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
