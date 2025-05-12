# importing necessary modules
import tkinter as tk                            # standard python GUI library
from tkinter import messagebox                  # To show popup alerts/messages
from src.user import User                       
from src.logger import Logger                   
from src.patient import Patient                 
from src.clinical_note import ClinicalNote      
import datetime                                 # for formatting date
import pandas as pd                             # added for DataFrame operations

# defining the UIManager class that controls the user interface
class UIManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Clinical Data Warehouse Login")
        self.logger = Logger()
        self.user = None
        self.build_login_screen()
        self.root.mainloop()

    def build_login_screen(self):
        self.clear_window()
        tk.Label(self.root, text="Username:").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(self.root, text="Password:").grid(row=1, column=0, padx=10, pady=10)
        self.username_entry = tk.Entry(self.root)
        self.password_entry = tk.Entry(self.root, show="*")
        self.username_entry.grid(row=0, column=1)
        self.password_entry.grid(row=1, column=1)
        login_button = tk.Button(self.root, text="Login", command=self.handle_login)
        login_button.grid(row=2, column=0, columnspan=2, pady=10)

    def handle_login(self):
        username = self.username_entry.get().strip()            
        password = self.password_entry.get().strip()            
        user = User.authenticate(username, password)
        if user:
            self.user = user
            self.logger.log_login(username, user.role, success=True)
            messagebox.showinfo("Login Success", f"Welcome, {user.role}!")
            self.show_main_menu()
        else:
            self.logger.log_login(username, success=False)
            messagebox.showerror("Login Failed", "Invalid credentials.")
        self.logger.write_logs()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_main_menu(self):
        self.clear_window()
        role = self.user.role
        tk.Label(self.root, text=f"Logged in as: {self.user.username} ({role})", font=("Arial", 12)).pack(pady=10)
        if role == "admin":
            tk.Button(self.root, text="Count Visits", command=self.count_visits_ui).pack(pady=5)
        elif role == "management":
            tk.Button(self.root, text="Generate Key Statistics", command=self.generate_statistics_ui).pack(pady=5)
        elif role in ["nurse", "clinician"]:
            tk.Button(self.root, text="Retrieve Patient", command=self.retrieve_patient_ui).pack(pady=5)
            tk.Button(self.root, text="Add Patient", command=self.add_patient_ui).pack(pady=5)
            tk.Button(self.root, text="Remove Patient", command=self.remove_patient_ui).pack(pady=5)
            tk.Button(self.root, text="Count Visits", command=self.count_visits_ui).pack(pady=5)
            tk.Button(self.root, text="View Note", command=self.view_note_ui).pack(pady=5)
        tk.Button(self.root, text="Exit", command=self.root.destroy).pack(pady=10)

    def retrieve_patient_ui(self):
        self.clear_window()
        tk.Label(self.root, text="Enter Patient ID:").pack(pady=5)
        patient_id_entry = tk.Entry(self.root)
        patient_id_entry.pack(pady=5)
        def submit():
            patient_id = patient_id_entry.get().strip()
            patient_handler = Patient()
            result = patient_handler.retrieve_patient(patient_id)
            if result:
                info = "\n".join([f"{key}: {value}" for key, value in result.items()])
                messagebox.showinfo("Patient Information", info)
                self.logger.log_action("Retrieve Patient")
            else:
                messagebox.showerror("Not Found", "No patient found with that ID.")
            self.show_main_menu()
        tk.Button(self.root, text="Submit", command=submit).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.show_main_menu).pack(pady=5)

    def add_patient_ui(self):
        self.clear_window()
        tk.Label(self.root, text="Add Patient Visit", font=("Arial", 12)).pack(pady=10)
        fields = {
            "Patient_ID": tk.Entry(self.root),
            "Visit_time (YYYY-MM-DD)": tk.Entry(self.root),
            "Visit_department": tk.Entry(self.root),
            "Gender": tk.Entry(self.root),
            "Race": tk.Entry(self.root),
            "Age": tk.Entry(self.root),
            "Ethnicity": tk.Entry(self.root),
            "Insurance": tk.Entry(self.root),
            "Zip_code": tk.Entry(self.root),
            "Chief_complaint": tk.Entry(self.root),
            "Note_ID": tk.Entry(self.root),
            "Note_type": tk.Entry(self.root),
            "Note_text": tk.Entry(self.root)
        }
        for label, entry in fields.items():
            tk.Label(self.root, text=label).pack()
            entry.pack()
        def submit():
            patient_handler = Patient()
            note_handler = ClinicalNote()
            try:
                patient_id = fields["Patient_ID"].get().strip()
                visit_time_str = fields["Visit_time (YYYY-MM-DD)"].get().strip()
                visit_time_formatted = datetime.datetime.strptime(visit_time_str, "%Y-%m-%d").date()
                visit_id = patient_handler.generate_unique_visit_id()
                patient_data = {
                    "Patient_ID": int(patient_id),
                    "Visit_ID": visit_id,
                    "Visit_time": visit_time_formatted,
                    "Visit_department": fields["Visit_department"].get().strip(),
                    "Gender": fields["Gender"].get().strip(),
                    "Race": fields["Race"].get().strip(),
                    "Age": int(fields["Age"].get().strip()),
                    "Ethnicity": fields["Ethnicity"].get().strip(),
                    "Insurance": fields["Insurance"].get().strip(),
                    "Zip_code": fields["Zip_code"].get().strip(),
                    "Chief_complaint": fields["Chief_complaint"].get().strip(),
                    "Note_ID": fields["Note_ID"].get().strip()
                }
                note_data = {
                    "Note_ID": fields["Note_ID"].get().strip(),
                    "Note_type": fields["Note_type"].get().strip(),
                    "Note_text": fields["Note_text"].get().strip()
                }
                patient_handler.add_patient_visit(patient_data)
                note_handler.note_df = pd.concat([note_handler.note_df, pd.DataFrame([note_data])], ignore_index=True)
                patient_handler.save_data()
                note_handler.note_df.to_csv("./data/Notes.csv", index=False)
                self.logger.log_action("Add Patient")
                messagebox.showinfo("Success", "Patient visit added successfully.")
                self.show_main_menu()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add patient visit:\n{str(e)}")
        tk.Button(self.root, text="Submit", command=submit).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.show_main_menu).pack(pady=5)

    def remove_patient_ui(self):
        self.clear_window()
        tk.Label(self.root, text="Enter Patient ID to Remove:").pack(pady=5)
        patient_id_entry = tk.Entry(self.root)
        patient_id_entry.pack(pady=5)
        def submit():
            patient_id = patient_id_entry.get().strip()
            patient_handler = Patient()
            removed = patient_handler.remove_patient(patient_id)
            if removed:
                patient_handler.save_data()
                self.logger.log_action("Remove Patient")
                messagebox.showinfo("Success", f"Patient {patient_id} removed successfully.")
            else:
                messagebox.showerror("Not Found", f"No patient found with ID {patient_id}.")
            self.show_main_menu()
        tk.Button(self.root, text="Submit", command=submit).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.show_main_menu).pack(pady=5)

    def count_visits_ui(self):
        self.clear_window()
        tk.Label(self.root, text="Enter Date (YYYY-MM-DD):").pack(pady=5)
        date_entry = tk.Entry(self.root)
        date_entry.pack(pady=5)
        def submit():
            patient_handler = Patient()
            date_str = date_entry.get().strip()
            try:
                count = patient_handler.count_visits_on_date(date_str)
                messagebox.showinfo("Visit Count", f"Total visits on {date_str}: {count}")
                self.logger.log_action(f"Count Visits on {date_str}")
            except Exception as e:
                messagebox.showerror("Error", f"Invalid date or operation failed:\n{str(e)}")
            self.show_main_menu()
        tk.Button(self.root, text="Submit", command=submit).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.show_main_menu).pack(pady=5)

    def view_note_ui(self):
        self.clear_window()
        tk.Label(self.root, text="Enter Patient ID:").pack(pady=5)
        patient_id_entry = tk.Entry(self.root)
        patient_id_entry.pack(pady=5)
        tk.Label(self.root, text="Enter Visit Date (YYYY-MM-DD):").pack(pady=5)
        date_entry = tk.Entry(self.root)
        date_entry.pack(pady=5)
        def submit():
            note_handler = ClinicalNote()
            patient_id = patient_id_entry.get().strip()
            date_str = date_entry.get().strip()
            try:
                note_text = note_handler.get_note_by_patient_and_date(patient_id, date_str)
                if note_text:
                    messagebox.showinfo("Clinical Note", note_text)
                    self.logger.log_action(f"View Note for {patient_id} on {date_str}")
                else:
                    messagebox.showerror("Not Found", "No note found for this patient on the given date.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.show_main_menu()
        tk.Button(self.root, text="Submit", command=submit).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.show_main_menu).pack(pady=5)

    def generate_statistics_ui(self):
        self.clear_window()
        tk.Label(self.root, text="Generate Key Statistics", font=("Arial", 12)).pack(pady=10)
        def submit():
            try:
                from src.statistics import StatisticsManager
                stats_handler = StatisticsManager()
                stats_handler.generate_summary_statistics(output_path='./output/statistics.txt')
                messagebox.showinfo("Success", "Statistics have been generated and saved to output/statistics.txt")
                self.logger.log_action("Generate Key Statistics")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to generate statistics:\n{str(e)}")
            self.show_main_menu()
        tk.Button(self.root, text="Generate", command=submit).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.show_main_menu).pack(pady=5)

if __name__ == "__main__":
    UIManager()
