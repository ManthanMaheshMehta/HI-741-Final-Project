import pandas as pd           # for reading and manipulating CSV files 
import datetime               # for handling and formatting dates

# defining a class to manage clinical notes
class ClinicalNote:

    # Constructor: initializes file paths and loads data from the provided CSVs
    def __init__(self, patient_file='./data/Patient_data.csv', note_file='./data/Notes.csv'):
        self.patient_file = patient_file
        self.note_file = note_file

        # Load patient data
        try:
            self.patient_df = pd.read_csv(patient_file)
            if 'Visit_time' in self.patient_df.columns:
                self.patient_df['Visit_time'] = pd.to_datetime(self.patient_df['Visit_time'], errors='coerce')
        except FileNotFoundError:
            self.patient_df = pd.DataFrame()

        # Load clinical notes
        try:
            self.note_df = pd.read_csv(note_file)
        except FileNotFoundError:
            self.note_df = pd.DataFrame()

    # Method to retrieve notes for a patient on a specific date
    def get_notes(self, patient_id, date_str):
        try:
            visit_date = pd.to_datetime(date_str, format="%Y-%m-%d", errors='coerce').date()
        except Exception:
            return None

        try:
            patient_id = int(patient_id)
        except ValueError:
            return None

        
        self.patient_df['Visit_time'] = pd.to_datetime(self.patient_df['Visit_time'], errors='coerce')

        # Filter for matching patient and visit date
        filtered_visits = self.patient_df[
            (self.patient_df['Patient_ID'] == patient_id) &
            (self.patient_df['Visit_time'].dt.date == visit_date)
        ]

        if filtered_visits.empty:
            return None

        note_ids = filtered_visits['Note_ID'].tolist()
        notes = self.note_df[self.note_df['Note_ID'].isin(note_ids)]

        if notes.empty:
            return None

        return notes[['Note_ID', 'Note_type', 'Note_text']].to_dict(orient='records')

    # Retrieve just the note text for UI display
    def get_note_by_patient_and_date(self, patient_id, visit_date):
        try:
            notes = self.get_notes(patient_id, visit_date)
            if notes:
                return notes[0]['Note_text']  # Return the first matching note
            return None
        except Exception as e:
            print(f"Error in get_note_by_patient_and_date: {e}")
            return None
