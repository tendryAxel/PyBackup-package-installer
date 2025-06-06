import os
import shutil
import uuid


def create_folder(folder: str) -> str:
    os.makedirs(folder, exist_ok=True)
    return folder


class TestParameters:
    def __init__(self, folder: str) -> None:
        self.TMP_FOLDER = folder


class TestContext:
    def __init__(self, folder: str = "./test"):
        self.params = TestParameters(folder + str(uuid.uuid4()))

    def __enter__(self):
        create_folder(self.params.TMP_FOLDER)
        return self.params

    def __exit__(self, exc_type, exc_val, exc_tb):
        shutil.rmtree(self.params.TMP_FOLDER)
