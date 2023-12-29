import json

class File:
    def __init__(self, filePath) -> None:
        """Init a file instance."""
        self.filePath = filePath


    def save(self, data):
        """Write data in the json file."""
        try:
            with open(self.filePath, "+w") as f:
                json.dump(data, f, sort_keys=True, indent=4, ensure_ascii=False)
        except Exception as error:
            print(f"An error has been encountered while trying to save in json file. This is the error: {error.args[1]}")
        
        f.close()


    def open(self) -> []:
        """Load data from the json file."""
        try:
            with open(self.filePath, '+r') as f:
                existing_data = json.load(f)
        except Exception as error:
            print(f"An error has been encountered while trying to open json file. This is the error: {error.args[1]}")
            existing_data = []

        f.close()
            
        return existing_data