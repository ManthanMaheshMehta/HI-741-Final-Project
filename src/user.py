import pandas as pd  # importing pandas for reading the CSV file

class User:
    # Constructor: Stores username, password, and role when a User object is created
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

    # static method to validate login credentials
    @staticmethod
    def authenticate(username_input, password_input, filepath='./data/Credentials.csv'):
        try:
            # loading the credentials file into a pandas DataFrame
            df = pd.read_csv(filepath)

            
            df['username'] = df['username'].astype(str).str.strip()
            df['password'] = df['password'].astype(str).str.strip()
            df['role'] = df['role'].astype(str).str.strip()

            # Strip whitespace from input
            username_input = username_input.strip()
            password_input = password_input.strip()

            # filtering the DataFrame to find a matching username and password 
            match = df[(df['username'] == username_input) & (df['password'] == password_input)]

            # if a match is found, a user object with the corresponding role will be created and returned
            if not match.empty:
                role = match.iloc[0]['role']
                return User(username_input, password_input, role)
            else:
                # if no match is found, return none, this is for invalid credentials
                return None

        # to handle errors such as file not found or wrong format
        except Exception as e:
            print("Error loading credentials:", e)
            return None
