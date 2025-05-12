# Import necessary modules,edit for version control commit
import os                          # for file and directory handling
from datetime import datetime      # for timestamping log entries

# defining a Logger class to record user logins and actions
class Logger:
    def __init__(self, filepath='./output/usage_log.txt'):
        self.filepath = filepath      # path where the log file will be saved
        self.logs = []                # temporary list to store log entries
        self.username = None          # storing the username of the current session
        self.role = None              # storing the role of the current user
        self.login_time = None        # storing login time

        # creating the directory if it doesn't exist
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)

    def log_login(self, username, role=None, success=True):
        self.username = username
        self.role = role if success else "N/A"
        self.login_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        status = "SUCCESS" if success else "FAILED"

        # creating the login log entry
        entry = f"[{self.login_time}] LOGIN {status} | Username: {username} | Role: {self.role}"
        self.logs.append(entry)  # adding it to the log list

    def log_action(self, action):
        # only log actions if a user is logged in
        if self.username and self.role:
            time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            entry = f"[{time_now}] ACTION | Username: {self.username} | Role: {self.role} | Action: {action}"
            self.logs.append(entry)  # appends action entry to logs

    def write_logs(self):
        # writing all log entries to the file and clear the log buffer
        with open(self.filepath, 'a') as f:
            for entry in self.logs:
                f.write(entry + '\n')
