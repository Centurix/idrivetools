import os
from pathlib import Path
from .bmw_file import BMWFile
from datetime import datetime

NBT_VERSION = "NBTevo_E15413A"

file_template = """
{file_count}
{data_1_sum}
{media_file_size}
{today}
{version}"""


class BMWInfoFile(BMWFile):
    def __init__(self, filename):
        """
        Handle the BMW backup file
        """
        super().__init__(filename)

    def file_stats(self, backup_root):
        file_count = 0
        file_size = 0

        for root, folders, files in os.walk(backup_root):
            for file in files:
                _, extension = os.path.splitext(file)
                if extension.upper().startswith(".BR"):
                    file_count += 1
                    file_size += os.path.getsize(os.path.join(root, file))

        return file_count, file_size

    def calculate_data_1_sum(self, filename):
        """
        The data_1 file sits alongside the info file
        """
        checksum = 0

        data_1_filename = filename.replace("info", "data_1")
        if os.path.exists(data_1_filename):
            with open(data_1_filename, "r") as data_1_file:
                usb_lines = data_1_file.readlines()

            for line in usb_lines:
                for char in line:
                    checksum += ord(char) & 0xFF

        return checksum

    def save(self, destination, encrypt=True):
        """
        Create a copy of the file if we're decrypting
        Otherwise, calculate all the values
        """
        # Create directories if necessary
        path, _ = os.path.split(destination)
        Path(path).mkdir(parents=True, exist_ok=True)

        if encrypt:
            # We're building a backup, creating this file from scratch
            backup_root, _ = os.path.split(destination)
            with open(destination, "w") as destination_file:
                file_count, media_file_size = self.file_stats(backup_root)
                data_1_sum = self.calculate_data_1_sum(destination)
                today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                destination_file.write(file_template.format(
                    file_count=file_count,
                    data_1_sum=data_1_sum,
                    media_file_size=media_file_size,
                    today=today,
                    version=NBT_VERSION
                ))

            return

        with open(self._filename, "rb") as source_file:
            with open(destination, "wb") as destination_file:
                destination_file.write(source_file.read())
