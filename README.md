#  Clinical Data Warehouse - HI 741 Final Project
This project is a Clinical Data Warehouse system developed for HI 741 (Spring 2025) at UWM. It provides an interactive user interface (UI) built with Tkinter, allowing different types of users (admin, management, nurse, clinician) to log in, manage patient records, and generate key usage statistics.

The system simulates real-world hospital workflows such as:
- Adding, retrieving, and removing patient visit records
- Viewing clinical notes
- Counting visits on specific dates
- Generating descriptive summaries from patient data

##  Installation Instructions

###  Prerequisites

- Python 3.8 or higher  
- Git (optional for cloning)
- Recommended: Anaconda or a virtual environment manager

### Step-by-Step Setup

1. Clone the GitHub repository:

   git clone https://github.com/ManthanMaheshMehta/HI-741-Final-Project
   
   cd HI-741-Final-Project
   
2.Install required packages:
pip install -r requirements.txt

3How to Run the Program:
Make sure you are inside the root project folder
Run the main Python file using this command:
python main.py

A login window will appear. Use the credentials from ./data/Credentials.csv to log in and explore role-based features.

 Project Structure:
 - `main.py`: Entry point of the program
- `README.md`: Project documentation
- `requirements.txt`: Python dependencies
- `UML_Diagram.png`: Class design structure
- `data/`
  - `Credentials.csv`
  - `Patient_data.csv`
  - `Notes.csv`
- `output/`
  - `updated_patients.csv`
  - `usage_log.txt`
  - `statistics.txt`
- `src/`
  - `ui.py`
  - `user.py`
  - `logger.py`
  - `patient.py`
  - `clinical_note.py`
  - `statistics.py`

Required Python Packages:
Listed in requirements.txt:
pandas

Other modules used (tkinter, os, datetime, random) are part of the Python standard library and do not require installation.

User Roles & Access:
 Role            Access Level                        

 admin         - Count visits only,                    
 nurse         -Full patient access and modification 
 clinician     - Full patient access and modification 
 management    - Generate key statistics only         

The UI changes based on user role after login. Unauthorized actions are disabled.

UML Diagram:
Refer to UML_Diagram.png for class structure and relationships.

Output Files:
usage_log.txt: Tracks login attempts, actions, and timestamps

updated_patients.csv: Contains modified patient data after add/remove actions

statistics.txt: Stores key summary statistics generated via the management panel

 Important Notes:
 Patient and note information is linked via Note_ID

All data is de-identified for privacy

Make sure to close any open CSV files before running the program to avoid PermissionError issues

 -Repository Link
Access the full project here:
https://github.com/ManthanMaheshMehta/HI-741-Final-Project

Tested On
Python 3.11 (via Anaconda)
Windows 10
Tkinter GUI
GitHub repository structure validated
