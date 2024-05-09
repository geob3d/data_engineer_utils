import json
import os
from typing import Optional


class FileSupport:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def create_file_directory(self):
        if not os.path.exists(self.file_path):
            os.makedirs(self.file_path)
        else:
            print("Path Alredy Exists")

    def create_file(self, db_obj_code: Optional[str] = None):
        with open(self.file_path, "w+") as f:
            if db_obj_code is None:
                pass
            else:
                f.write(db_obj_code)

    def load_json_file(self):
        # project_root = os.path.dirname(os.path.dirname(__file__))
        # filename = os.path.join(project_root, json_file)
        with open(self.file_path, "r") as myfile:
            data = myfile.read()
        # parse file
        obj = json.loads(data)
        return obj
