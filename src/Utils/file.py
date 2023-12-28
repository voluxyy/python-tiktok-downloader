import json

class File:
    def saveData(file_path, data):
        try:
            with open(file_path, "+w") as f:
                json.dump(data, f, sort_keys=True, indent=4, ensure_ascii=False)
        except Exception as error:
            print(f"An error has been encountered while trying to save in json file. This is the error: {error.args[1]}")


    def openJson(file_path) -> []:
        try:
            with open(file_path, '+r') as f:
                existing_data = json.load(f)
        except Exception as error:
            print(f"An error has been encountered while trying to open json file. This is the error: {error.args[1]}")
            existing_data = []
            
        return existing_data