import tkinter as tk
from tkinter import messagebox, ttk
import Data.items as items

predefined_items = items.fetch_item()

def on_entry_select(index):
    def callback(selected_value):
        entry_feats[index] = selected_value
        print(entry_feats)
    return callback

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
            width=entry_width * 1
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


root = tk.Tk()
root.title("Crafting Cost Simulator")
root.resizable(False, False)

main_container = ttk.Frame(root)
main_container.pack(padx=10, pady=5, fill='x')

frame_stats = ttk.LabelFrame(main_container, text="Player Stats")
frame_stats.grid(row=0, column=0)

tk.Label(frame_stats, text="Str:").grid(row=0, column=0)
entry_stat_str = tk.Entry(frame_stats, width=5)
entry_stat_str.insert(0, "1")
entry_stat_str.grid(row=0, column=1, sticky="we", pady=8)

tk.Label(frame_stats, text="Dex:").grid(row=0, column=2)
entry_stat_str = tk.Entry(frame_stats, width=5)
entry_stat_str.insert(0, "1")
entry_stat_str.grid(row=0, column=3, sticky="we", pady=8)

tk.Label(frame_stats, text="Con:").grid(row=0, column=4)
entry_stat_str = tk.Entry(frame_stats, width=5)
entry_stat_str.insert(0, "1")
entry_stat_str.grid(row=0, column=5, sticky="we", pady=8)

tk.Label(frame_stats, text="Int:").grid(row=0, column=6)
entry_stat_str = tk.Entry(frame_stats, width=5)
entry_stat_str.insert(0, "1")
entry_stat_str.grid(row=0, column=7, sticky="we", pady=8)

tk.Label(frame_stats, text="Wis:").grid(row=0, column=8)
entry_stat_str = tk.Entry(frame_stats, width=5)
entry_stat_str.insert(0, "1")
entry_stat_str.grid(row=0, column=9, sticky="we", pady=8)

tk.Label(frame_stats, text="Cha:").grid(row=0, column=10)
entry_stat_str = tk.Entry(frame_stats, width=5)
entry_stat_str.insert(0, "1")
entry_stat_str.grid(row=0, column=11, sticky="we", pady=8)

frame_feats = ttk.LabelFrame(main_container, text="Current feats")
frame_feats.grid(row=1, column=0)

entry_feats = [None] * 25
for i in range(25):
    entry = AutocompleteEntry(predefined_items, frame_feats, callback=on_entry_select(i))
    entry.insert(0, predefined_items[0])
    entry.grid(row=i, column=0, sticky="we", pady=2, padx=8)
    entry_feats[i] = predefined_items[0] 


root.mainloop()