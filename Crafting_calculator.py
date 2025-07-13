import tkinter as tk
from tkinter import messagebox
import random

def run_simulation():
    try:
        # Get values from input fields
        mod = int(entry_mod.get())
        bace_cost = float(entry_bace_cost.get())/3
        mod_cost = float(entry_mod_cost.get())/3
        skill = int(entry_skill.get())
        bace_dc = int(entry_bace_dc.get())
        mod_dc = int(entry_mod_dc.get())

        costs = 0

        rolls = [0,0]
        for x in range(1, 21):
            costs = (bace_cost + (mod_cost * mod))/2
            if x + skill >= bace_dc + mod_dc * mod:
                rolls[0] += 1
            else:
                rolls[1] += 1
            
        if rolls[0] == 0:
            result_label.config(text=f"Average Crafting Cost: N/A")
        else:
            p = 20/rolls[0]
            print(p)
            
            avg_cost = costs + (p * (bace_cost + (mod_cost * mod))/2)
            result_label.config(text=f"Average Crafting Cost: {avg_cost:.2f}")

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
tk.Label(root, text="Cost").grid(row=1, column=0, sticky="e")
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
entry_skill.grid(row=5, column=1, columnspan=2, sticky="we")

# Run simulation button
tk.Button(root, text="Calculate", command=run_simulation).grid(row=6, column=0, columnspan=3, pady=10)

# Result label
result_label = tk.Label(root, text="Estimated Crafting Cost: ")
result_label.grid(row=7, column=0, columnspan=3)

root.mainloop()
