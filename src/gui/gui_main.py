import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from src.main import run_logic

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
        file_path = selected_file.get()
        if not file_path:
            messagebox.showerror("Error", "Please upload a CSV file before running.")
            return
        headless_mode = headless_var.get()

        try:
            result = run_logic(file_path, headless_mode)
            messagebox.showinfo("Success", f"Scraper completed: {result}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    root.title("Accessibility Statement automation")
    selected_file = tk.StringVar()
    headless_var = tk.BooleanVar(value=False)
    # File upload section
    ttk.Label(root, text="Step 1: Upload a CSV File").pack(pady=5)
    upload_button = ttk.Button(root, text="Upload CSV", command=upload_file)
    upload_button.pack(pady=5)
    file_label = ttk.Label(root, text="No file selected", wraplength=350)
    file_label.pack(pady=5)

    # Options section
    ttk.Label(root, text="Step 2: Configure Options").pack(pady=10)
    headless_checkbox = ttk.Checkbutton(root, text="Run Headless", variable=headless_var)
    headless_checkbox.pack(pady=5)

    # Run button
    ttk.Label(root, text="Step 3: Run the Scraper").pack(pady=10)
    run_button = ttk.Button(root, text="Go", command=run_scraper)
    run_button.pack(pady=20)

    stop_button = ttk.Button(root, text='Finish', command=root.destroy)
    stop_button.pack(pady=20)
    root.mainloop()
