class Logger:
    def __init__(self, log_file_path):
        self.log_file_path = log_file_path

    def log(self, message):
        with open(self.log_file_path, 'a') as file:
            file.write(message + "\n")
