import csv
from src.adapter import adapter
from src.logger import logger

class LocalCSV(adapter.Adapter):
    def __init__(self):
        pass

    def loadById(self, src_name, id):
        file_name = f"test_data/{src_name}.csv"
        try: 
            with open(file_name, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['id'] == str(id):
                        return row

        except FileNotFoundError:
            logger.Logger.log(f"Error: The file '{file_name}' does not exist.")
            return None

        return None