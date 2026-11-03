import tkinter as tk
from tkinter import ttk, messagebox

# ==========================================
# MAIN WINDOW
# ==========================================

root = tk.Tk()
root.title("Hospital Management System")
root.geometry("1100x700")
root.minsize(950, 600)
root.configure(bg="#eef2f7")

# ==========================================
# COLORS
# ==========================================

BG_COLOR = "#eef2f7"
HEADER_COLOR = "#173b57"
BUTTON_COLOR = "#2471a3"
GREEN_COLOR = "#239b56"
RED_COLOR = "#c0392b"
WHITE = "#ffffff"

# ==========================================
# HEADER
# ==========================================

header = tk.Frame(root, bg=HEADER_COLOR, height=80)
header.pack(fill="x")

tk.Label(
    header,
    text="HOSPITAL MANAGEMENT SYSTEM",
    font=("Arial", 22, "bold"),
    fg=WHITE,
    bg=HEADER_COLOR
).pack(pady=(12, 2))

tk.Label(
    header,
    text="Patient Management Dashboard",
    font=("Arial", 11),
    fg=WHITE,
    bg=HEADER_COLOR
).pack()

# ==========================================
# PATIENT FORM
# ==========================================

form_frame = tk.LabelFrame(
    root,
    text="Patient Registration",
    font=("Arial", 13, "bold"),
    bg=WHITE,
    padx=15,
    pady=15
)
form_frame.pack(fill="x", padx=20, pady=15)

patient_id = tk.StringVar()
patient_name = tk.StringVar()
age = tk.StringVar()
gender = tk.StringVar()
contact = tk.StringVar()
disease = tk.StringVar()

# Patient ID
tk.Label(form_frame, text="Patient ID:", bg=WHITE).grid(
    row=0, column=0, padx=10, pady=10, sticky="w"
)

id_entry = tk.Entry(
    form_frame, textvariable=patient_id, width=25
)
id_entry.grid(row=0, column=1, padx=10, pady=10)

# Patient Name
tk.Label(form_frame, text="Patient Name:", bg=WHITE).grid(
    row=0, column=2, padx=10, pady=10, sticky="w"
)

name_entry = tk.Entry(
    form_frame, textvariable=patient_name, width=25
)
name_entry.grid(row=0, column=3, padx=10, pady=10)

# Age
tk.Label(form_frame, text="Age:", bg=WHITE).grid(
    row=1, column=0, padx=10, pady=10, sticky="w"
)

age_entry = tk.Entry(
    form_frame, textvariable=age, width=25
)
age_entry.grid(row=1, column=1, padx=10, pady=10)

# Gender
tk.Label(form_frame, text="Gender:", bg=WHITE).grid(
    row=1, column=2, padx=10, pady=10, sticky="w"
)

gender_box = ttk.Combobox(
    form_frame,
    textvariable=gender,
    values=["Male", "Female", "Other"],
    state="readonly",
    width=22
)
gender_box.grid(row=1, column=3, padx=10, pady=10)

# Contact
tk.Label(form_frame, text="Contact Number:", bg=WHITE).grid(
    row=2, column=0, padx=10, pady=10, sticky="w"
)

contact_entry = tk.Entry(
    form_frame, textvariable=contact, width=25
)
contact_entry.grid(row=2, column=1, padx=10, pady=10)

# Disease
tk.Label(form_frame, text="Disease:", bg=WHITE).grid(
    row=2, column=2, padx=10, pady=10, sticky="w"
)

disease_entry = tk.Entry(
    form_frame, textvariable=disease, width=25
)
disease_entry.grid(row=2, column=3, padx=10, pady=10)

# ==========================================
# PATIENT TABLE
# ==========================================

table_frame = tk.LabelFrame(
    root,
    text="Patient Records",
    font=("Arial", 13, "bold"),
    bg=WHITE,
    padx=10,
    pady=10
)
table_frame.pack(fill="both", expand=True, padx=20, pady=10)

columns = ("ID", "Name", "Age", "Gender", "Contact", "Disease")

tree = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    selectmode="browse"
)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=130, anchor="center")

scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=tree.yview
)

tree.configure(yscrollcommand=scrollbar.set)

tree.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# ==========================================
# HELPER FUNCTIONS
# ==========================================

def clear_fields():
    """Clear the form and reset patient ID."""

    id_entry.config(state="normal")

    patient_id.set("")
    patient_name.set("")
    age.set("")
    gender.set("")
    contact.set("")
    disease.set("")

    tree.selection_remove(tree.selection())
    id_entry.focus_set()


def validate_input():
    """Validate patient information."""

    pid = patient_id.get().strip()
    name = patient_name.get().strip()
    patient_age = age.get().strip()
    patient_gender = gender.get().strip()
    phone = contact.get().strip()
    patient_disease = disease.get().strip()

    if not all([
        pid, name, patient_age,
        patient_gender, phone, patient_disease
    ]):
        messagebox.showwarning(
            "Validation Error",
            "Please fill in all fields."
        )
        return None

    if not patient_age.isdigit():
        messagebox.showerror(
            "Invalid Age",
            "Age must be a whole number."
        )
        return None

    if not 0 <= int(patient_age) <= 130:
        messagebox.showerror(
            "Invalid Age",
            "Enter an age between 0 and 130."
        )
        return None

    if not phone.isdigit() or not 7 <= len(phone) <= 15:
        messagebox.showerror(
            "Invalid Contact",
            "Contact number must contain 7 to 15 digits."
        )
        return None

    return (
        pid,
        name,
        int(patient_age),
        patient_gender,
        phone,
        patient_disease
    )


def find_patient(pid):
    """Find a patient using patient ID."""

    for item in tree.get_children():
        values = tree.item(item, "values")

        if values[0] == pid:
            return item

    return None

# ==========================================
# ADD PATIENT
# ==========================================

def add_patient():

    data = validate_input()

    if data is None:
        return

    if find_patient(data[0]):
        messagebox.showerror(
            "Duplicate ID",
            "Patient ID already exists."
        )
        return

    tree.insert("", "end", values=data)

    messagebox.showinfo(
        "Success",
        "Patient registered successfully!"
    )

    clear_fields()

# ==========================================
# SELECT PATIENT FROM TABLE
# ==========================================

def select_patient(event=None):
    """Display the selected patient's details in the form."""

    selected = tree.selection()

    if not selected:
        return

    values = tree.item(selected[0], "values")

    # Allow the ID to be updated before changing its state.
    id_entry.config(state="normal")

    patient_id.set(values[0])
    patient_name.set(values[1])
    age.set(values[2])
    gender.set(values[3])
    contact.set(values[4])
    disease.set(values[5])

    # Keep the selected patient's ID read-only.
    id_entry.config(state="readonly")


# Bind table selection event
tree.bind("<<TreeviewSelect>>", select_patient)

# ==========================================
# UPDATE PATIENT
# ==========================================

def update_patient():

    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "Selection Required",
            "Select a patient from the table first."
        )
        return

    data = validate_input()

    if data is None:
        return

    item = selected[0]

    # Ensure the ID remains unchanged.
    old_values = tree.item(item, "values")

    if data[0] != old_values[0]:
        messagebox.showerror(
            "Invalid ID",
            "The selected patient's ID cannot be changed."
        )
        return

    tree.item(item, values=data)

    messagebox.showinfo(
        "Success",
        "Patient details updated successfully!"
    )

    clear_fields()

# ==========================================
# DELETE PATIENT
# ==========================================

def delete_patient():

    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "Selection Required",
            "Select a patient to delete."
        )
        return

    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this patient?"
    )

    if confirm:
        tree.delete(selected[0])
        clear_fields()

        messagebox.showinfo(
            "Success",
            "Patient record deleted successfully!"
        )

# ==========================================
# SEARCH PATIENT
# ==========================================

def search_patient(event=None):

    query = search_var.get().strip().lower()

    if not query:
        messagebox.showwarning(
            "Search",
            "Enter a patient ID or name."
        )
        return

    for item in tree.get_children():

        values = tree.item(item, "values")

        pid = str(values[0]).lower()
        name = str(values[1]).lower()

        if query in pid or query in name:

            tree.selection_set(item)
            tree.focus(item)
            tree.see(item)

            # The selection event loads the patient details.
            return

    messagebox.showinfo(
        "Search Result",
        "No matching patient found."
    )


def show_all_patients():

    search_var.set("")
    tree.selection_remove(tree.selection())


# ==========================================
# ACTION BUTTONS
# ==========================================

button_frame = tk.Frame(root, bg=BG_COLOR)
button_frame.pack(fill="x", padx=20, pady=5)

tk.Button(
    button_frame,
    text="Add Patient",
    command=add_patient,
    bg=GREEN_COLOR,
    fg=WHITE,
    width=15
).pack(side="left", padx=5)

tk.Button(
    button_frame,
    text="Update Patient",
    command=update_patient,
    bg=BUTTON_COLOR,
    fg=WHITE,
    width=15
).pack(side="left", padx=5)

tk.Button(
    button_frame,
    text="Delete Patient",
    command=delete_patient,
    bg=RED_COLOR,
    fg=WHITE,
    width=15
).pack(side="left", padx=5)

tk.Button(
    button_frame,
    text="Clear Fields",
    command=clear_fields,
    width=15
).pack(side="left", padx=5)

# ==========================================
# SEARCH SECTION
# ==========================================

search_frame = tk.Frame(root, bg=BG_COLOR)
search_frame.pack(fill="x", padx=20, pady=(5, 15))

tk.Label(
    search_frame,
    text="Search Patient:",
    bg=BG_COLOR,
    font=("Arial", 10, "bold")
).pack(side="left", padx=5)

search_var = tk.StringVar()

search_entry = tk.Entry(
    search_frame,
    textvariable=search_var,
    width=30
)
search_entry.pack(side="left", padx=5)

tk.Button(
    search_frame,
    text="Search",
    command=search_patient,
    bg=BUTTON_COLOR,
    fg=WHITE,
    width=12
).pack(side="left", padx=5)

tk.Button(
    search_frame,
    text="Show All",
    command=show_all_patients,
    width=12
).pack(side="left", padx=5)

# Press Enter to search
search_entry.bind("<Return>", search_patient)

# ==========================================
# START APPLICATION
# ==========================================

root.mainloop()

