import os
from pathlib import Path
from .bmw_file import BMWFile


class BMWBackupFile(BMWFile):
    def __init__(self, filename):
        """
        Handle the BMW backup file
        """
        super().__init__(filename)

    def save(self, destination, encrypt=True):
        """
        Create a copy of the file if we're decrypting
        Otherwise, calculate all the values
        """
        # Create directories if necessary
        path, _ = os.path.split(destination)
        Path(path).mkdir(parents=True, exist_ok=True)

        contents = "NBTV2"
        if os.path.exists(self._filename):
            with open(self._filename, "r") as source_file:
                contents = source_file.read()

        with open(destination, "w") as destination_file:
            destination_file.write(contents)
