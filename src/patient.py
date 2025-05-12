import pandas as pd
import datetime
import random

class Patient:
    def __init__(self, patient_file='./data/Patient_data.csv'):
        self.patient_file = patient_file
        try:
            self.df = pd.read_csv(patient_file)
            if 'Visit_time' in self.df.columns:
                self.df['Visit_time'] = pd.to_datetime(self.df['Visit_time'], errors='coerce')
        except FileNotFoundError:
            self.df = pd.DataFrame()

    def save_data(self, output_path='./output/updated_patients.csv'):
        df_copy = self.df.copy()
        if 'Visit_time' in df_copy.columns:
            df_copy['Visit_time'] = df_copy['Visit_time'].dt.strftime("%Y-%m-%d")
        df_copy.to_csv(output_path, index=False)

    def retrieve_patient(self, patient_id):
        patient_visits = self.df[self.df['Patient_ID'] == int(patient_id)]
        if patient_visits.empty:
            return None
        latest = patient_visits.sort_values(by='Visit_time', ascending=False).iloc[0]
        return latest.to_dict()

    def remove_patient(self, patient_id):
        if int(patient_id) not in self.df['Patient_ID'].values:
            return False
        self.df = self.df[self.df['Patient_ID'] != int(patient_id)]
        return True

    def count_visits_on_date(self, date_str):
        try:
            target_date = pd.to_datetime(date_str, format="%Y-%m-%d", errors='coerce').date()
            return (self.df['Visit_time'].dt.date == target_date).sum()
        except Exception as e:
            print("Date error:", e)
            return 0

    def add_patient_visit(self, patient_data):
        self.df = pd.concat([self.df, pd.DataFrame([patient_data])], ignore_index=True)

    def generate_unique_visit_id(self):
        return random.randint(100000, 999999)
