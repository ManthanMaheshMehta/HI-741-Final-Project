import pandas as pd  # for reading and analyzing CSV data
import os             # for handling file paths

class StatisticsManager:
    def __init__(self, filepath='./data/Patient_data.csv'):
        self.filepath = filepath           # path to the patient data CSV file
        self.data = None                   # this will hold the loaded data
        self.load_data()                   # loading data immediately when the class is instantiated

    def load_data(self):
        try:
            self.data = pd.read_csv(self.filepath)
        except FileNotFoundError:
            print("Error: Patient data file not found.")
            self.data = pd.DataFrame()  # using an empty DataFrame to avoid crashes

    def generate_summary_statistics(self, output_path='./output/statistics.txt'):
        if self.data.empty:
            print("No data available to generate statistics.")
            return

        # total number of unique patients
        total_patients = self.data['Patient_ID'].nunique()

        # total number of visits 
        total_visits = len(self.data)

        # average age of patients
        avg_age = self.data['Age'].mean()

        # count by gender
        gender_dist = self.data['Gender'].value_counts()

        # count by race
        race_dist = self.data['Race'].value_counts()

        # count by insurance type
        insurance_dist = self.data['Insurance'].value_counts()

        # making sure the output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # writing statistics to a text file
        with open(output_path, 'w') as f:
            f.write("--- Summary Statistics ---\n")
            f.write(f"Total unique patients: {total_patients}\n")
            f.write(f"Total number of visits: {total_visits}\n")
            f.write(f"Average age: {avg_age:.2f}\n\n")

            f.write("--- Gender Distribution ---\n")
            f.write(gender_dist.to_string())
            f.write("\n\n")

            f.write("--- Race Distribution ---\n")
            f.write(race_dist.to_string())
            f.write("\n\n")

            f.write("--- Insurance Distribution ---\n")
            f.write(insurance_dist.to_string())
            f.write("\n")

        print("Statistics file created at:", output_path)
