import os
from pathlib import Path
from .inverter import Inverter


class BMWFile(Inverter):
    def __init__(
            self,
            filename,
            decrypted_extension=None,
            encrypted_extension=None,
            encrypted=False,
            encrypt_length=None
    ):
        self._filename = filename
        self._decrypted_extension = decrypted_extension
        self._encrypted_extension = encrypted_extension
        self._encrypted = encrypted
        self._encrypt_length = encrypt_length

    def __str__(self):
        return f"{self._filename}: encrypted={self._encrypted}"

    def save(self, destination, encrypt=True):
        with open(self._filename, "rb") as source_file:
            contents = source_file.read()

        # Does the full path exist?
        path, file = os.path.split(destination)
        file_name, extension = os.path.splitext(file)

        # Create directories if necessary
        Path(path).mkdir(parents=True, exist_ok=True)

        if encrypt and self._encrypted_extension is not None:
            extension = self._encrypted_extension
        if not encrypt and self._decrypted_extension is not None:
            extension = self._decrypted_extension

        with open(
            os.path.join(path, f"{file_name}{extension}"),
            "wb"
        ) as destination_file:
            if self._encrypted != encrypt:
                contents = self.invert(contents, self._encrypt_length)

            destination_file.write(contents)
