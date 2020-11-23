import os
from pathlib import Path
from .bmw_file import BMWFile


class BMWData1CountFile(BMWFile):
    def __init__(self, filename):
        """
        Handle the BMW backup file
        """
        super().__init__(filename)

    def save(self, destination, encrypt=True):
        """
        Count all the sub-folders in the backup and create
        the data_1 file. Exclude _Playlists folder
        """
        # Create directories if necessary
        path, _ = os.path.split(destination)
        Path(path).mkdir(parents=True, exist_ok=True)

        if encrypt:
            root, _ = os.path.split(destination)

            if not os.path.exists(root):
                print(f"Folder {root} does not exist")
                return

            folders = [item.name for item in os.scandir(root) if item.is_dir() and item.name != "_Playlists"]

            with open(destination, "w") as destination_file:
                destination_file.write(f"{len(folders)}")

            return

        with open(self._filename, "rb") as source_file:
            with open(destination, "wb") as destination_file:
                destination_file.write(source_file.read())
