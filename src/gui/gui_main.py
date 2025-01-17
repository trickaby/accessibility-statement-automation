import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from src.gui.gui_styles import AppStyle
from src.main import run_logic
from src.modules.constant_values import output_path_dir
from src.modules.data_handler import open_csv

root = tk.Tk()

def start_gui():

    def upload_file():
        file_path = filedialog.askopenfilename(
            title="Select a CSV File",
            filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*"))
        )
        if file_path:
            file_label.config(text=f"Selected: {file_path}")
            selected_file.set(file_path)

    def run_scraper():
        input_file_path = selected_file.get()
        file_name = os.path.basename(selected_file.get())
        output_file_path = output_path_dir + "Results " + file_name
        if not input_file_path:
            messagebox.showerror("Error", "Please upload a CSV file before running.")
            return
        headless_mode = headless_var.get()

        try:
            result = run_logic(input_file_path, output_file_path, headless_mode)
            messagebox.showinfo("Success", f"Scraper completed. Results written to: {result}")
            response = messagebox.askyesno("Open report", "Open accessibility report")
            if response:
                open_csv(result)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    root.title("Accessibility Statement automation")
    root.geometry("900x600")
    AppStyle(root)

    frame = tk.Frame(root, bg="#f9f9f9", padx=10, pady=10)
    frame.pack(padx=20, pady=20)

    # File upload section
    selected_file = tk.StringVar()

    ttk.Label(frame, style="Header.TLabel", text="Step 1: Upload a CSV File").pack(padx=10, pady=10)

    ttk.Button(frame, style='TButton', text="Upload CSV", command=upload_file).pack(pady=5)
    file_label = ttk.Label(frame, style='TLabel', text="No file selected", wraplength=350)
    file_label.pack(pady=5)

    # Options section
    ttk.Label(frame, style='Header.TLabel', text="Step 2: Configure Options").pack(padx=10, pady=10)
    headless_var = tk.BooleanVar(value=False)
    ttk.Checkbutton(frame, style='TCheckbutton', text="Run Headless", variable=headless_var).pack(pady=5)

    # Run button
    ttk.Label(frame, style='Header.TLabel', text="Step 3: Run the Scraper").pack(padx=10, pady=10)
    ttk.Button(frame, style='TButton', text="Go", command=run_scraper).pack(pady=20)

    # Stop button
    ttk.Button(frame, style='TButton', text='Finish', command=root.destroy).pack(pady=20)
    root.mainloop()
