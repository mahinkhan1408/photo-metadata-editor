import os
import csv
import subprocess
from tkinter import Tk, Button, filedialog, messagebox, simpledialog, Label, StringVar

# Path to exiftool executable (adjust as needed)
exiftool_path = "c:/Scr/exiftool.exe"

# GUI root window setup
root = Tk()
root.title("Photos EXIF Data Editor")
root.geometry("450x230")
root.resizable(False, False)

folder_path = StringVar()

# Function to select folder
def select_folder():
    folder = filedialog.askdirectory()
    if folder:
        folder_path.set(folder)

# Main function to apply metadata
def update_metadata_sorted():
    folder = folder_path.get()
    if not folder:
        messagebox.showerror("Error", "No folder selected.")
        return

    # Ask for metadata CSV
    csv_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if not csv_path:
        return

    # Ask user for camera model and make
    model = simpledialog.askstring("Camera Model", "Enter camera model (e.g., Mini 20T Pro):")
    make = simpledialog.askstring("Camera Make", "Enter camera make (e.g., Armer):")

    metadata_rows = []
    try:
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                metadata_rows.append(row)
    except Exception as e:
        messagebox.showerror("CSV Error", f"Failed to read CSV file.\n\n{e}")
        return

    image_files = sorted(f for f in os.listdir(folder) if f.lower().endswith((".jpg", ".jpeg")))

    if len(metadata_rows) != len(image_files):
        messagebox.showerror("Mismatch", f"{len(image_files)} images but {len(metadata_rows)} metadata rows.")
        return

    # Apply metadata row by row
    for i, filename in enumerate(image_files):
        row = metadata_rows[i]
        try:
            lat = float(row['latitude'])
            lon = float(row['longitude'])
            datetime_val = row['datetime']
            full_path = os.path.join(folder, filename)

            subprocess.run([
                exiftool_path,
                f"-GPSLatitude={abs(lat)}",
                f"-GPSLatitudeRef={'N' if lat >= 0 else 'S'}",
                f"-GPSLongitude={abs(lon)}",
                f"-GPSLongitudeRef={'E' if lon >= 0 else 'W'}",
                f"-Model={model}",
                f"-Make={make}",
                f"-DateTimeOriginal={datetime_val}",
                "-overwrite_original",
                full_path
            ], capture_output=True, text=True)
        except Exception as err:
            messagebox.showwarning("Warning", f"Error processing {filename}:\n{err}")

    messagebox.showinfo("Success", "Metadata successfully applied to all images.")

# GUI Elements
Label(root, text="📸 Photos EXIF Data Editor", font=("Helvetica", 14, "bold")).pack(pady=10)
Label(root, text="1. Select folder containing images").pack()
Button(root, text="📂 Browse Folder", width=30, command=select_folder).pack(pady=5)

Label(root, text="2. Browse CSV and Run").pack()
Button(root, text="🛠️  Browse CSV and Run Metadata Update", width=35, command=update_metadata_sorted).pack(pady=10)

# Start GUI loop
root.mainloop()
